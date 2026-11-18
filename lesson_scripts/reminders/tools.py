import json
from datetime import datetime

from anthropic.types import Message, ToolParam


def get_current_datetime(date_format="%Y-%m-%d %H:%M:%S"):
    if not date_format:
        raise ValueError("date_format cannot be empty")
    return datetime.now().strftime(date_format)


get_current_datetime_schema = ToolParam(
    {
        "name": "get_current_datetime",
        "description": (
            "Returns the current date and time formatted according to "
            "the specified format"
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "date_format": {
                    "type": "string",
                    "description": (
                        "A string specifying the format of the returned "
                        "datetime. Uses Python's strftime format codes."
                    ),
                    "default": "%Y-%m-%d %H:%M:%S",
                }
            },
            "required": [],
        },
    }
)


def run_tool(tool_name, tool_input):
    if tool_name == "get_current_datetime":
        return get_current_datetime(**tool_input)


def run_tools(message):
    tool_requests = [
        block for block in message.content if block.type == "tool_use"
    ]
    tool_result_blocks = []

    for tool_request in tool_requests:
        try:
            tool_output = run_tool(tool_request.name, tool_request.input)
            tool_result_block = {
                "type": "tool_result",
                "tool_use_id": tool_request.id,
                "content": json.dumps(tool_output),
                "is_error": False,
            }
        except Exception as e:
            tool_result_block = {
                "type": "tool_result",
                "tool_use_id": tool_request.id,
                "content": f"Error: {e}",
                "is_error": True,
            }
        tool_result_blocks.append(tool_result_block)

    return tool_result_blocks


def add_user_message(messages, message):
    # message — текст, список блоков или ответ Claude (Message)
    content = message.content if isinstance(message, Message) else message
    messages.append({"role": "user", "content": content})


def add_assistant_message(messages, message):
    # Сохраняем все блоки ответа: текст и tool use
    content = message.content if isinstance(message, Message) else message
    messages.append({"role": "assistant", "content": content})


def chat(client, model, messages, system=None, tools=None, thinking=None):
    params = {
        "model": model,
        "max_tokens": 1000,
        "messages": messages,
    }
    # API не принимает None, поэтому добавляем только заданные параметры
    if system:
        params["system"] = system
    if tools:
        params["tools"] = tools
    if thinking:
        params["thinking"] = thinking

    # Возвращаем весь ответ: в нём могут быть блоки tool use
    return client.messages.create(**params)


def text_from_message(message):
    return "\n".join(
        [block.text for block in message.content if block.type == "text"]
    )


def run_conversation(client, model, messages, tools, thinking=None):
    while True:
        response = chat(
            client, model, messages, tools=tools, thinking=thinking
        )
        add_assistant_message(messages, response)
        print(text_from_message(response))

        if response.stop_reason != "tool_use":
            break

        tool_results = run_tools(response)
        add_user_message(messages, tool_results)

    return messages
