# Task 1: two questions, two tools
#
# Send lab-chat a system message (GharFix's booking
# assistant, today is 2026-10-22), the user's message,
# exactly:
#
#   How much is an AC service, and who can come to
#   Whitefield?
#   (one line, as in the task)
#
# and tools=gharfix.TOOLS. The model asks for two tools in
# one reply. For every call in that reply, in order, print
# one line:
#
#   <call id> <tool name> <arguments as the model wrote them>
#
# run it with gharfix's function, and append its tool
# message. Then send the second request and print only the
# text of the model's final answer.
#
# Careful: all the tool messages go after the one assistant
# message that asked for them, before the next request.
#
# Stuck? Press "What do I do next?" under this task. Write
# your code below.
import json

from openai import OpenAI

import gharfix

client = OpenAI()
messages = [
    {"role": "system", "content": "You are GharFix's booking assistant in Bengaluru. Today is 2026-10-22. Use the tools."},
    {"role": "user", "content": "How much is an AC service, and who can come to Whitefield?"},
]
response = client.chat.completions.create(model="lab-chat", messages=messages, tools=gharfix.TOOLS)
message = response.choices[0].message
messages.append(message)
for call in message.tool_calls:
    print(call.id, call.function.name, call.function.arguments)
    result = gharfix.FUNCTIONS[call.function.name](**json.loads(call.function.arguments))
    messages.append({"role": "tool", "tool_call_id": call.id, "content": json.dumps(result)})
final = client.chat.completions.create(model="lab-chat", messages=messages, tools=gharfix.TOOLS)
print(final.choices[0].message.content)
