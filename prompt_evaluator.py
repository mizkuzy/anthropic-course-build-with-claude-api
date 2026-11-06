# Eval pipeline для модуля Prompt engineering techniques.
# Основа — notebook студента (jaygaha/Building-with-the-Claude-API,
# 003-Prompt-engineering/001_prompting.ipynb). Отличия: structured outputs
# вместо prefill и temperature, наши helpers, экранирование HTML в отчёте.

import concurrent.futures
import html
import json
from statistics import mean
from textwrap import dedent

from helpers import add_user_message


def chat_json(client, model, messages, schema, system=None):
    """Запрос с structured outputs: возвращает JSON по схеме"""
    params = {
        "model": model,
        "max_tokens": 2000,
        "messages": messages,
        "output_config": {
            "format": {"type": "json_schema", "schema": schema}
        },
    }
    if system:
        params["system"] = system

    response = client.messages.create(**params)
    text = next(
        block.text for block in response.content if block.type == "text"
    )
    return json.loads(text)


GRADE_SCHEMA = {
    "type": "object",
    "properties": {
        "strengths": {"type": "array", "items": {"type": "string"}},
        "weaknesses": {"type": "array", "items": {"type": "string"}},
        "reasoning": {"type": "string"},
        "score": {"type": "integer"},
    },
    "required": ["strengths", "weaknesses", "reasoning", "score"],
    "additionalProperties": False,
}


class PromptEvaluator:
    def __init__(self, client, model, max_concurrent_tasks=3):
        self.client = client
        self.model = model
        self.max_concurrent_tasks = max_concurrent_tasks

    def _chat_json(self, prompt, schema, system=None):
        messages = []
        add_user_message(messages, prompt)
        return chat_json(
            self.client, self.model, messages, schema, system=system
        )

    def _run_parallel(self, func, items, label):
        """Запускает func для каждого item в нескольких потоках"""
        results = []
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=self.max_concurrent_tasks
        ) as executor:
            futures = [executor.submit(func, item) for item in items]
            for future in concurrent.futures.as_completed(futures):
                results.append(future.result())
                print(f"{label} {len(results)}/{len(items)}")
        return results

    def generate_unique_ideas(
        self, task_description, prompt_inputs_spec, num_cases
    ):
        """Придумывает num_cases разных сценариев для тестов"""
        inputs = "\n".join(
            f"{key}: {value}" for key, value in prompt_inputs_spec.items()
        )
        prompt = dedent(f"""
            Generate {num_cases} unique, diverse ideas for testing a prompt
            that accomplishes this task:

            <task_description>
            {task_description}
            </task_description>

            The prompt will receive the following inputs:
            <prompt_inputs>
            {inputs}
            </prompt_inputs>

            Each idea should represent a distinct scenario or example that
            tests different aspects of the task. Each idea is a brief
            description.

            Ensure each idea is:
            - Clearly distinct from the others
            - Relevant to the task description
            - Specific enough to guide generation of a full test case
            - Quick to solve without requiring extensive computation
            - Solvable with no more than 400 tokens of output

            Remember, only generate {num_cases} unique ideas.
        """)
        schema = {
            "type": "object",
            "properties": {
                "ideas": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["ideas"],
            "additionalProperties": False,
        }
        system = (
            "You are a test scenario designer specialized in creating "
            "diverse, unique testing scenarios."
        )
        return self._chat_json(prompt, schema, system)["ideas"]

    def generate_test_case(self, task_description, idea, prompt_inputs_spec):
        """Создаёт один тест: входные данные и критерии оценки"""
        inputs = "\n".join(
            f"{key}: {value}" for key, value in prompt_inputs_spec.items()
        )
        prompt = dedent(f"""
            Generate a single detailed test case for a prompt evaluation
            based on:

            <task_description>
            {task_description}
            </task_description>

            <specific_idea>
            {idea}
            </specific_idea>

            <prompt_inputs>
            {inputs}
            </prompt_inputs>

            Requirements:
            - Make the test case realistic and practically useful
            - solution_criteria: 1 to 4 measurable, concise criteria
            - The solution criteria should ONLY address the direct
              requirements of the task description and the prompt inputs
            - Avoid over-specifying criteria with requirements that go
              beyond the core task
            - The test case should be tailored to the specific idea
            - Solvable with no more than 400 tokens of output

            Example of good solution criteria for the task "Extract topics
            out of a passage of text": ["Includes all topics mentioned"].
            It is concise and doesn't ask for anything outside of the
            scope of the task description.
        """)
        schema = {
            "type": "object",
            "properties": {
                "prompt_inputs": {
                    "type": "object",
                    "properties": {
                        key: {"type": "string"} for key in prompt_inputs_spec
                    },
                    "required": list(prompt_inputs_spec),
                    "additionalProperties": False,
                },
                "solution_criteria": {
                    "type": "array",
                    "items": {"type": "string"},
                },
            },
            "required": ["prompt_inputs", "solution_criteria"],
            "additionalProperties": False,
        }
        system = (
            "You are a test case creator specializing in designing "
            "evaluation scenarios."
        )
        test_case = self._chat_json(prompt, schema, system)
        test_case["task_description"] = task_description
        test_case["scenario"] = idea
        return test_case

    def generate_dataset(
        self,
        task_description,
        prompt_inputs_spec,
        num_cases=1,
        output_file="dataset.json",
    ):
        """Генерирует dataset и сохраняет его в файл"""
        ideas = self.generate_unique_ideas(
            task_description, prompt_inputs_spec, num_cases
        )
        dataset = self._run_parallel(
            lambda idea: self.generate_test_case(
                task_description, idea, prompt_inputs_spec
            ),
            ideas,
            "Generated",
        )
        with open(output_file, "w") as f:
            json.dump(dataset, f, indent=2)
        return dataset

    def grade_output(self, test_case, output, extra_criteria=None):
        """Grader на модели: оценивает ответ по критериям теста"""
        inputs = json.dumps(test_case["prompt_inputs"], indent=2)
        criteria = "\n".join(test_case["solution_criteria"])

        extra_section = ""
        if extra_criteria:
            extra_section = dedent(f"""
                Mandatory Requirements - ANY VIOLATION MEANS AUTOMATIC
                FAILURE (score of 3 or lower):
                <extra_important_criteria>
                {extra_criteria}
                </extra_important_criteria>
            """)

        prompt = dedent(f"""
            Your task is to evaluate the following AI-generated solution
            with EXTREME RIGOR.

            Original task description:
            <task_description>
            {test_case["task_description"]}
            </task_description>

            Original task inputs:
            <task_inputs>
            {inputs}
            </task_inputs>

            Solution to Evaluate:
            <solution>
            {output}
            </solution>

            Criteria you should use to evaluate the solution:
            <criteria>
            {criteria}
            </criteria>

            {extra_section}

            Scoring Guidelines:
            * Score 1-3: Solution fails to meet one or more MANDATORY
              requirements
            * Score 4-6: Solution meets all mandatory requirements but has
              significant deficiencies in secondary criteria
            * Score 7-8: Solution meets all mandatory requirements and most
              secondary criteria, with minor issues
            * Score 9-10: Solution meets all mandatory and secondary
              criteria

            IMPORTANT SCORING INSTRUCTIONS:
            * Grade the output based ONLY on the listed criteria. Do not add
              your own extra requirements.
            * If a solution meets all of the mandatory and secondary
              criteria give it a 10
            * Don't complain that the solution "only" meets the criteria.
              Solutions shouldn't go above and beyond - they should meet
              the exact listed criteria.
            * ANY violation of a mandatory requirement MUST result in a
              score of 3 or lower
            * The full 1-10 scale should be utilized - don't hesitate to
              give low scores when warranted

            Provide "strengths" (1-3 items), "weaknesses" (1-3 items),
            "reasoning" (concise) and "score" (1-10).
        """)
        return self._chat_json(prompt, GRADE_SCHEMA)

    def run_test_case(self, test_case, run_prompt_function, extra_criteria):
        """Запускает prompt на одном тесте и оценивает ответ"""
        output = run_prompt_function(test_case["prompt_inputs"])
        grade = self.grade_output(test_case, output, extra_criteria)
        return {
            "output": output,
            "test_case": test_case,
            "score": grade["score"],
            "reasoning": grade["reasoning"],
        }

    def run_evaluation(
        self,
        run_prompt_function,
        dataset_file,
        extra_criteria=None,
        json_output_file="output.json",
        html_output_file="output.html",
    ):
        """Запускает eval на всём dataset, сохраняет JSON и HTML-отчёт"""
        with open(dataset_file, "r") as f:
            dataset = json.load(f)

        results = self._run_parallel(
            lambda test_case: self.run_test_case(
                test_case, run_prompt_function, extra_criteria
            ),
            dataset,
            "Graded",
        )

        average_score = mean(result["score"] for result in results)
        print(f"Average score: {average_score}")

        with open(json_output_file, "w") as f:
            json.dump(results, f, indent=2)
        with open(html_output_file, "w", encoding="utf-8") as f:
            f.write(build_report(results))

        return results


def build_report(results):
    """HTML-отчёт: средний балл и таблица по каждому тесту"""
    # Ответы Claude экранируем, иначе символ < может сломать таблицу
    e = html.escape
    scores = [result["score"] for result in results]
    average = mean(scores)
    pass_rate = 100 * len([s for s in scores if s >= 7]) / len(scores)

    rows = ""
    for result in results:
        test_case = result["test_case"]
        inputs = "<br>".join(
            f"<b>{e(key)}:</b> {e(str(value))}"
            for key, value in test_case["prompt_inputs"].items()
        )
        criteria = "<br>".join(
            f"• {e(c)}" for c in test_case["solution_criteria"]
        )
        rows += f"""
        <tr>
          <td>{e(test_case["scenario"])}</td>
          <td>{inputs}</td>
          <td>{criteria}</td>
          <td><pre>{e(result["output"])}</pre></td>
          <td class="score">{result["score"]}</td>
          <td>{e(result["reasoning"])}</td>
        </tr>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Prompt Evaluation Report</title>
<style>
  body {{ font-family: Arial, sans-serif; margin: 20px; color: #333; }}
  table {{ width: 100%; border-collapse: collapse; }}
  th {{ background: #4a4a4a; color: white; text-align: left;
        padding: 10px; }}
  td {{ padding: 10px; border-bottom: 1px solid #ddd;
        vertical-align: top; }}
  pre {{ white-space: pre-wrap; margin: 0; }}
  .score {{ font-weight: bold; }}
</style>
</head>
<body>
<h1>Prompt Evaluation Report</h1>
<p>Total test cases: {len(results)} · Average score: {average:.1f} / 10
 · Pass rate (≥7): {pass_rate:.1f}%</p>
<table>
  <tr><th>Scenario</th><th>Prompt Inputs</th><th>Solution Criteria</th>
      <th>Output</th><th>Score</th><th>Reasoning</th></tr>
  {rows}
</table>
</body>
</html>
"""
