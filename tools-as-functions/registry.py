# Task 3: a registry of tools
#
# Write a class Registry:
#
#   @registry.tool       a decorator: records the function
#                        under its name, with its description
#                        from tool_schema (from schema.py),
#                        and returns the function unchanged
#   registry.schemas()   the recorded descriptions, in the
#                        order the tools were added
#   registry.run(name, arguments)
#                        runs the named function with the
#                        arguments (JSON text) and returns
#                        the result as JSON text
#
# Then a module-level registry with two tools of your own,
# get_quote(job) and find_technicians(service, area), each
# with a docstring written for the model, each returning
# what gharfix's function of the same name returns.
#
# When the file is run, send lab-chat a system message
# (GharFix's booking assistant, today is 2026-10-22) and the
# user's message, exactly:
#
#   How much is a geyser repair, and who can come to Hebbal?
#
# with registry.schemas() as the tools. Run every call with
# registry.run, send the results back, and print only the
# text of the model's final answer.
#
# Careful: a decorator that forgets to return the function
# leaves None behind under the function's name.
#
# Stuck? Press "What do I do next?" under this task. Write
# your code below.
import json

from openai import OpenAI

import gharfix
from schema import tool_schema


class Registry:
    def __init__(self):
        self.functions = {}
        self.tools = []

    def tool(self, fn):
        self.functions[fn.__name__] = fn
        self.tools.append(tool_schema(fn))
        return fn

    def schemas(self) -> list[dict]:
        return self.tools

    def run(self, name: str, arguments: str) -> str:
        result = self.functions[name](**json.loads(arguments))
        return json.dumps(result)


registry = Registry()


@registry.tool
def get_quote(job: str) -> dict:
    """Get the price of a job from GharFix's rate card, like tap-repair or fan-repair."""
    return gharfix.get_quote(job)


@registry.tool
def find_technicians(service: str, area: str) -> list[dict] | dict:
    """Find technicians who do a service (plumbing, electrical, carpentry or ac) in an area of Bengaluru."""
    return gharfix.find_technicians(service, area)


if __name__ == "__main__":
    client = OpenAI()
    messages = [
        {"role": "system", "content": "You are GharFix's booking assistant. Today is 2026-10-22."},
        {"role": "user", "content": "How much is a geyser repair, and who can come to Hebbal?"},
    ]
    response = client.chat.completions.create(model="lab-chat", messages=messages, tools=registry.schemas())
    message = response.choices[0].message
    messages.append(message)
    for call in message.tool_calls:
        messages.append({"role": "tool", "tool_call_id": call.id, "content": registry.run(call.function.name, call.function.arguments)})
    final = client.chat.completions.create(model="lab-chat", messages=messages, tools=registry.schemas())
    print(final.choices[0].message.content)
