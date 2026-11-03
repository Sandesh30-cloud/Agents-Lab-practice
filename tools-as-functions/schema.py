# Task 1: a tool description from a function
#
# Write tool_schema(fn). It returns fn's tool description,
# a dictionary shaped like one item of gharfix.TOOLS:
#
#   {"type": "function",
#    "function": {
#        "name": fn's name,
#        "description": the first line of fn's docstring,
#        "parameters": {
#            "type": "object",
#            "properties": {one per parameter: {"type": ...}},
#            "required": [the parameters with no default],
#            "additionalProperties": False}}}
#
# Types: str is "string", int "integer", float "number",
# bool "boolean", list "array", dict "object". A hint like
# str | None is the type of its non-None part.
#
# The check runs it on every function in gharfix.FUNCTIONS
# and compares it with gharfix.TOOLS (names, parameters,
# types, required), then on functions of its own.
#
# Careful: gharfix's hints are stored as text ('str | None'),
# not as types. Ask the typing module for the real ones.
#
# Try it: print(tool_schema(gharfix.check_slots))
#
# Stuck? Press "What do I do next?" under this task. Write
# your code below.
import inspect
import types
import typing

TYPES = {str: "string", int: "integer", float: "number", bool: "boolean", list: "array", dict: "object"}


def json_type(hint) -> str:
    if isinstance(hint, types.UnionType) or typing.get_origin(hint) is typing.Union:
        hint = next(h for h in typing.get_args(hint) if h is not type(None))
    return TYPES[typing.get_origin(hint) or hint]


def tool_schema(fn) -> dict:
    hints = typing.get_type_hints(fn)
    properties = {}
    required = []
    for name, param in inspect.signature(fn).parameters.items():
        properties[name] = {"type": json_type(hints[name])}
        if param.default is inspect.Parameter.empty:
            required.append(name)
    return {
        "type": "function",
        "function": {
            "name": fn.__name__,
            "description": inspect.getdoc(fn).splitlines()[0],
            "parameters": {"type": "object", "properties": properties, "required": required, "additionalProperties": False},
        },
    }


if __name__ == "__main__":
    import json

    import gharfix

    print(json.dumps(tool_schema(gharfix.check_slots), indent=2))
