# Task 1: a cap with a stop reason
#
# Write run_agent(question, model="lab-chat", max_steps=6).
# It is chapter 3's loop (a system message saying today is
# 2026-10-22, the question, gharfix.TOOLS, every call run
# with gharfix.FUNCTIONS), asking the model it is given, and
# it returns a tuple (answer, stop reason):
#
#   (the answer's text, "answered")  when the model answers
#   (None, "max_steps")              when it has sent
#                                    max_steps requests and
#                                    the last still asked
#                                    for tools
#
# The check runs it with lab-chat, and with lab-chat-loopy
# (a model that never stops asking) and several caps.
#
# Careful: the cap counts requests sent, not tool calls run.
# With max_steps=4, exactly 4 requests.
#
# Stuck? Press "What do I do next?" under this task. Write
# your code below.
import json

from openai import OpenAI

import gharfix

client = OpenAI()
SYSTEM = "You are GharFix's booking assistant in Bengaluru. Today is 2026-10-22. Use the tools."


def run_agent(question, model="lab-chat", max_steps=6):
    messages = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": question}]
    for _ in range(max_steps):
        response = client.chat.completions.create(model=model, messages=messages, tools=gharfix.TOOLS)
        message = response.choices[0].message
        if response.choices[0].finish_reason == "stop":
            return message.content, "answered"
        messages.append(message)
        for call in message.tool_calls:
            result = gharfix.FUNCTIONS[call.function.name](**json.loads(call.function.arguments))
            messages.append({"role": "tool", "tool_call_id": call.id, "content": json.dumps(result)})
    return None, "max_steps"


if __name__ == "__main__":
    print(run_agent("Please move GF850958 to 17 Nov evening."))
    print(run_agent("Please move GF850958 to 17 Nov evening.", model="lab-chat-loopy", max_steps=4))
