# Task 4 (interview question): the loop that runs forever
#
# Vikram's team added a repeat guard to this agent, and it
# still never finishes with lab-chat-loopy, a model that asks
# for the same call after every result. Run it with
# python3 fix_forever.py and stop it with Ctrl+C after a few
# seconds; then run lab steps.
#
# Fix run_agent(question, model) so that it always ends:
#
#   - when the model asks for a call this run already made
#     (the same tool with the same arguments), do not run it:
#     send the conversation once more with tool_choice="none"
#     and return that answer
#   - never send more than 6 requests in the loop; if it
#     gets there, end the same way, with tool_choice="none"
#
# Keep the function's name and parameters, the system
# message, the question and the two answers it prints.
#
# Careful: look at what the guard compares. Is it ever the
# same twice?
#
# Stuck? Press "What do I do next?" under this task.

import json

from openai import OpenAI

import gharfix

client = OpenAI()


def run_agent(question, model="lab-chat"):
    messages = [
        {"role": "system", "content": "You are GharFix's booking assistant in Bengaluru. Today is 2026-10-22. Use the tools."},
        {"role": "user", "content": question},
    ]
    seen = set()
    for _ in range(6):
        response = client.chat.completions.create(model=model, messages=messages, tools=gharfix.TOOLS)
        message = response.choices[0].message
        if response.choices[0].finish_reason == "stop":
            return message.content
        if any((call.function.name, call.function.arguments) in seen for call in message.tool_calls):
            break
        messages.append(message)
        for call in message.tool_calls:
            seen.add((call.function.name, call.function.arguments))
            result = gharfix.FUNCTIONS[call.function.name](**json.loads(call.function.arguments))
            messages.append({"role": "tool", "tool_call_id": call.id, "content": json.dumps(result)})
    final = client.chat.completions.create(model=model, messages=messages, tools=gharfix.TOOLS, tool_choice="none")
    return final.choices[0].message.content


print(run_agent("When is the technician coming for GF894117?"))
print(run_agent("When is the technician coming for GF894117?", model="lab-chat-loopy"))
