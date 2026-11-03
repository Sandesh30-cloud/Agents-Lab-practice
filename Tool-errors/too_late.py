# Task 2: an error the customer hears about
#
# Run this request through the loop, with a system message
# (GharFix's booking assistant, today is 2026-10-22),
# gharfix.TOOLS, and your run_tool from run_tool.py for
# every call, exactly:
#
#   Please move my booking GF712358 to 2026-10-26 evening.
#
# GharFix refuses: the slot starts within 4 hours. Send
# that error back like any result, and print the model's
# final answer. Then look the booking up with
# gharfix.get_booking and print one line:
#
#   <booking ID> <date> <slot> <status>
#
# Careful: an error result is not the end of the run. The
# model still has to tell the customer.
#
# Stuck? Press "What do I do next?" under this task. Write
# your code below.
from openai import OpenAI

import gharfix
from run_tool import run_tool

client = OpenAI()
messages = [
    {"role": "system", "content": "You are GharFix's booking assistant in Bengaluru. Today is 2026-10-22. Use the tools."},
    {"role": "user", "content": "Please move my booking GF712358 to 2026-10-26 evening."},
]
for _ in range(10):
    response = client.chat.completions.create(model="lab-chat", messages=messages, tools=gharfix.TOOLS)
    message = response.choices[0].message
    if response.choices[0].finish_reason == "stop":
        print(message.content)
        break
    messages.append(message)
    for call in message.tool_calls:
        messages.append({"role": "tool", "tool_call_id": call.id, "content": run_tool(call.function.name, call.function.arguments)})

booking = gharfix.get_booking("GF712358")
print(booking["booking_id"], booking["date"], booking["slot"], booking["status"])
