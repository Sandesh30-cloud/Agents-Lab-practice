# Task 2: a repeat guard
#
# Write run_agent(question, model="lab-chat", max_steps=6),
# task 1's loop with a guard. Keep every call the run has
# made: its tool name and its arguments.
#
# When a reply asks for a call the run already made (the
# same tool with the same arguments; spaces and key order in
# the JSON do not count), do not run anything from that
# reply. Send the conversation so far once more, without
# that reply, with tool_choice="none", and return
#
#   (that answer's text, "repeated")
#
# Otherwise as task 1: (answer, "answered"), or
# (None, "max_steps") after max_steps requests.
#
# Careful: the model's repeated reply must not go into the
# conversation. Its calls would have no results.
#
# Stuck? Press "What do I do next?" under this task. Write
# your code below.
import json

from openai import OpenAI

import gharfix

client = OpenAI()
SYSTEM = "You are GharFix's booking assistant in Bengaluru. Today is 2026-10-22. Use the tools."


def key(call):
    return call.function.name, json.dumps(json.loads(call.function.arguments), sort_keys=True)


def run_agent(question, model="lab-chat", max_steps=6):
    messages = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": question}]
    seen = set()
    for _ in range(max_steps):
        response = client.chat.completions.create(model=model, messages=messages, tools=gharfix.TOOLS)
        message = response.choices[0].message
        if response.choices[0].finish_reason == "stop":
            return message.content, "answered"
        if any(key(call) in seen for call in message.tool_calls):
            final = client.chat.completions.create(model=model, messages=messages, tools=gharfix.TOOLS, tool_choice="none")
            return final.choices[0].message.content, "repeated"
        messages.append(message)
        for call in message.tool_calls:
            seen.add(key(call))
            result = gharfix.FUNCTIONS[call.function.name](**json.loads(call.function.arguments))
            messages.append({"role": "tool", "tool_call_id": call.id, "content": json.dumps(result)})
    return None, "max_steps"


if __name__ == "__main__":
    print(run_agent("Please move GF850958 to 17 Nov evening.", model="lab-chat-loopy"))
