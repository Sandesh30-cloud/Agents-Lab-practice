# Task 1: the loop as a function
#
# Write run_agent(question). It:
#
#   1. starts a conversation: a system message (GharFix's
#      booking assistant, today is 2026-10-22) and the
#      question as the user's message
#   2. asks lab-chat, with tools=gharfix.TOOLS
#   3. while the model asks for tools: runs every call with
#      gharfix.FUNCTIONS, appends the model's own message
#      and one tool message per call (the result as JSON),
#      and asks again
#   4. when the first choice's finish_reason is "stop",
#      returns (the answer's text, the number of requests)
#
# Never more than 10 requests: if the tenth still asks for
# tools, return (None, 10).
#
# The check calls it with three of Meenakshi's jobs: a
# booking, a reschedule and a quote.
#
# Careful: make the conversation inside the function. Each
# question is a new run.
#
# Try it: print(run_agent("Please move GF850958 to 17 Nov
# evening."))
#
# Stuck? Press "What do I do next?" under this task. Write
# your code below.
import json

from openai import OpenAI

import gharfix

client = OpenAI()
SYSTEM = "You are GharFix's booking assistant in Bengaluru. Today is 2026-10-22. Use the tools."


def run_agent(question):
    messages = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": question}]
    requests = 0
    while requests < 10:
        response = client.chat.completions.create(model="lab-chat", messages=messages, tools=gharfix.TOOLS)
        requests += 1
        choice = response.choices[0]
        if choice.finish_reason == "stop":
            return choice.message.content, requests
        messages.append(choice.message)
        for call in choice.message.tool_calls:
            result = gharfix.FUNCTIONS[call.function.name](**json.loads(call.function.arguments))
            messages.append({"role": "tool", "tool_call_id": call.id, "content": json.dumps(result)})
    return None, requests


if __name__ == "__main__":
    answer, requests = run_agent("Book a carpenter in Sarjapur Road 24 Oct morning: a cupboard hinge came off. I am Sana Rao, phone 9603306969.")
    print(answer)
    print(f"Requests: {requests}")
