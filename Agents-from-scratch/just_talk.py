# Task 1: a model that can only talk
#
# Send lab-chat two messages:
#
#   1. a system message: it is GharFix's booking assistant,
#      and today is 2026-10-22
#   2. Meenakshi's request, as the user's message, exactly:
#      Book a plumber in Koramangala tomorrow morning, a pipe
#      is leaking under the sink. I am Ravi Kumar, phone
#      9876543210.
#      (one line, with single spaces, as in the task)
#
# Send no tools. Print only the text of the reply.
#
# Then read /workspace/data/bookings.json, count the bookings
# whose phone is 9876543210, and print:
#
#   Bookings found: N
#
# Careful: read the reply, then the count. Did the model do
# what it said?
#
# Run it in the terminal with: python3 just_talk.py
#
# Stuck? Press "What do I do next?" under this task. Write
# your code below.
import json
from pathlib import Path

from openai import OpenAI

REQUEST = "Book a plumber in Koramangala tomorrow morning, a pipe is leaking under the sink. I am Ravi Kumar, phone 9876543210."

client = OpenAI()
response = client.chat.completions.create(
    model="lab-chat",
    messages=[
        {"role": "system", "content": "You are GharFix's booking assistant. Today is 2026-10-22."},
        {"role": "user", "content": REQUEST},
    ],
)
print(response.choices[0].message.content)

bookings = json.loads(Path("/workspace/data/bookings.json").read_text(encoding="utf-8"))
found = [b for b in bookings if b["phone"] == "9876543210"]
print(f"Bookings found: {len(found)}")
