from datetime import datetime, timedelta

from anthropic.types import ToolParam


def get_current_datetime(date_format="%Y-%m-%d %H:%M:%S"):
    if not date_format:
        raise ValueError("date_format cannot be empty")
    return datetime.now().strftime(date_format)


get_current_datetime_schema = ToolParam(
    {
        "name": "get_current_datetime",
        "description": (
            "Returns the current date and time "
            "formatted according to the specified format."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "date_format": {
                    "type": "string",
                    "description": (
                        "A string specifying the format "
                        "of the returned datetime. "
                        "Uses Python's strftime format codes."
                    ),
                    "default": "%Y-%m-%d %H:%M:%S",
                }
            },
            "required": [],
        },
    }
)


def add_duration_to_datetime(
    datetime_str, duration, unit, input_format="%Y-%m-%d %H:%M:%S"
):
    if not datetime_str:
        raise ValueError("datetime_str cannot be empty")
    # timedelta принимает days, hours и т. д.; месяцев и лет в нём нет
    if unit not in ("seconds", "minutes", "hours", "days", "weeks"):
        raise ValueError(f"Unsupported unit: {unit}")
    start = datetime.strptime(datetime_str, input_format)
    result = start + timedelta(**{unit: duration})
    # День недели — чтобы Claude мог ответить «какой это будет день»
    return result.strftime("%A, %Y-%m-%d %H:%M:%S")


add_duration_to_datetime_schema = ToolParam(
    {
        "name": "add_duration_to_datetime",
        "description": (
            "Adds a duration to a date and time. "
            "Returns the result with the day of the week, "
            "formatted as 'Weekday, YYYY-MM-DD HH:MM:SS'. "
            "Use it whenever you need a date in the future or the past, "
            "instead of calculating it yourself. "
            "A negative duration subtracts time. "
            "Months and years are not supported: convert them to days."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "datetime_str": {
                    "type": "string",
                    "description": (
                        "The starting date and time in input_format, "
                        "e.g. '2050-01-01 00:00:00'."
                    ),
                },
                "duration": {
                    "type": "number",
                    "description": "How many units to add. Can be negative.",
                },
                "unit": {
                    "type": "string",
                    "enum": ["seconds", "minutes", "hours", "days", "weeks"],
                    "description": "The unit of the duration.",
                },
                "input_format": {
                    "type": "string",
                    "description": (
                        "The format of datetime_str. "
                        "Uses Python's strptime format codes."
                    ),
                    "default": "%Y-%m-%d %H:%M:%S",
                },
            },
            "required": ["datetime_str", "duration", "unit"],
        },
    }
)


def set_reminder(content, timestamp):
    if not content:
        raise ValueError("content cannot be empty")
    if not timestamp:
        raise ValueError("timestamp cannot be empty")
    # Настоящей системы напоминаний нет, просто печатаем
    print(f"----\nReminder set for {timestamp}: {content}\n----")
    return f"Reminder set for {timestamp}"


set_reminder_schema = ToolParam(
    {
        "name": "set_reminder",
        "description": (
            "Sets a reminder for the user at the given date and time. "
            "Use it when the user asks to be reminded about something. "
            "The timestamp must be an exact date and time: "
            "if the user gives a relative time, "
            "calculate it first with add_duration_to_datetime. "
            "Returns a confirmation message."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": (
                        "What to remind the user about, "
                        "e.g. 'Doctor's appointment'."
                    ),
                },
                "timestamp": {
                    "type": "string",
                    "description": (
                        "When to remind, formatted as 'YYYY-MM-DD HH:MM:SS'."
                    ),
                },
            },
            "required": ["content", "timestamp"],
        },
    }
)


def run_tool(tool_name, tool_input):
    if tool_name == "get_current_datetime":
        return get_current_datetime(**tool_input)
    elif tool_name == "add_duration_to_datetime":
        return add_duration_to_datetime(**tool_input)
    elif tool_name == "set_reminder":
        return set_reminder(**tool_input)
