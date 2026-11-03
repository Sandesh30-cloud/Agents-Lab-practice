# Task 2: results in any order
#
# Send lab-chat the same kind of system message, the user's
# message, exactly:
#
#   Cancel GF424921 and GF186543 please.
#
# and tools=gharfix.TOOLS. The model asks for cancel_booking
# twice in one reply. Run the calls LAST FIRST (the reply's
# last call first), and as you run each one, print:
#
#   <call id> <booking ID> refund <refund>
#
# from the call's result, and append its tool message. Then
# send the second request and print only the text of the
# model's final answer.
#
# Careful: the tool messages go back in the order you ran
# the calls. What tells the model which result is which?
#
# Stuck? Press "What do I do next?" under this task. Write
# your code below.
import json

from openai import OpenAI

import gharfix

client = OpenAI()
messages = [
    {"role": "system", "content": "You are GharFix's booking assistant in Bengaluru. Today is 2026-10-22. Use the tools."},
    {"role": "user", "content": "Cancel GF424921 and GF186543 please."},
]
response = client.chat.completions.create(model="lab-chat", messages=messages, tools=gharfix.TOOLS)
message = response.choices[0].message
messages.append(message)
for call in reversed(message.tool_calls):
    result = gharfix.FUNCTIONS[call.function.name](**json.loads(call.function.arguments))
    print(call.id, result["booking_id"], "refund", result["refund"])
    messages.append({"role": "tool", "tool_call_id": call.id, "content": json.dumps(result)})
final = client.chat.completions.create(model="lab-chat", messages=messages, tools=gharfix.TOOLS)
print(final.choices[0].message.content)
