# Task 1: a tool runner that never raises
#
# Write run_tool(name, arguments). name is the tool the
# model asked for, arguments the JSON text it wrote. It runs
# GharFix's function (gharfix.FUNCTIONS) and returns the
# result as JSON text, ready for a tool message.
#
# It must never raise. Each of these comes back as JSON text
# of an object with an "error" key (a sentence the model can
# act on):
#
#   - a name that is not a tool (say which name)
#   - arguments that are not valid JSON
#   - JSON that is not an object, like ["tap-repair"]
#   - arguments the function does not take, or is missing
#     (a TypeError: include its message, which names them)
#   - any other exception inside the function
#
# A function's own {"error": ...} result is a result like
# any other: send it back unchanged.
#
# Careful: catch what you expect, but a booking system can
# fail in ways you did not expect too.
#
# Try it: print(run_tool("get_price", '{"job": "tap-repair"}'))
#
# Stuck? Press "What do I do next?" under this task. Write
# your code below.
import json

import gharfix


def run_tool(name, arguments):
    fn = gharfix.FUNCTIONS.get(name)
    if fn is None:
        return json.dumps({"error": f"there is no tool named {name!r}; tools: {', '.join(gharfix.FUNCTIONS)}"})
    try:
        args = json.loads(arguments)
    except json.JSONDecodeError as e:
        return json.dumps({"error": f"the arguments are not valid JSON ({e}): send a JSON object"})
    if not isinstance(args, dict):
        return json.dumps({"error": "the arguments must be a JSON object, with one key per parameter"})
    try:
        result = fn(**args)
    except TypeError as e:
        return json.dumps({"error": f"wrong arguments: {e}"})
    except Exception as e:
        return json.dumps({"error": f"{name} failed: {type(e).__name__}: {e}"})
    return json.dumps(result)


if __name__ == "__main__":
    print(run_tool("get_quote", '{"job": "tap-repair"}'))
    print(run_tool("get_price", '{"job": "tap-repair"}'))
    print(run_tool("find_technicians", '{"service_name": "plumbing", "area": "Koramangala"}'))
