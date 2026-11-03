# Task 4 (interview question): find the crash
#
# This agent books Meenakshi's plumber request. Run it with
# python3 fix_crash.py: it crashes before the booking, and
# the traceback says where.
#
# Fix run_agent(question, model) so that nothing a tool or
# the model does can crash it. The check calls it with:
#
#   - lab-chat and this booking request
#   - lab-chat-confused, which gets an argument wrong in its
#     first call
#   - lab-chat and a reschedule that GharFix refuses
#
# Each time it must return the model's final answer, and
# every problem must go back to the model as a tool result
# with an error key, never as an exception.
#
# Keep the function's name and parameters, the system
# message, and printing "tool error:" with the message for
# a result that is an error.
#
# Careful: there is more than one crash. Fix the first, then
# try it with model="lab-chat-confused".
#
# Stuck? Press "What do I do next?" under this task.
import json

from openai import OpenAI

import gharfix

client = OpenAI()


def run_call(call):
    fn = gharfix.FUNCTIONS.get(call.function.name)
    if fn is None:
        return {"error": f"there is no tool named {call.function.name!r}"}
    try:
        return fn(**json.loads(call.function.arguments))
    except (TypeError, ValueError) as e:
        return {"error": f"wrong arguments: {e}"}


def run_agent(question, model="lab-chat"):
    messages = [
        {"role": "system", "content": "You are GharFix's booking assistant in Bengaluru. Today is 2026-10-22. Use the tools."},
        {"role": "user", "content": question},
    ]
    for _ in range(10):
        response = client.chat.completions.create(model=model, messages=messages, tools=gharfix.TOOLS)
        message = response.choices[0].message
        if response.choices[0].finish_reason == "stop":
            return message.content
        messages.append(message)
        for call in message.tool_calls:
            result = run_call(call)
            if isinstance(result, dict) and result.get("error"):
                print("tool error:", result["error"])
            messages.append({"role": "tool", "tool_call_id": call.id, "content": json.dumps(result)})
    return None


if __name__ == "__main__":
    print(run_agent("Book a plumber in Koramangala 29 Oct evening: the bathroom drain is blocked. I am Rohan Nair, phone 9316315012."))
