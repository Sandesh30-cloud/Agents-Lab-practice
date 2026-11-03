# Task 2: book_slot's arguments in Pydantic
#
# 1. Write a Pydantic model BookSlotArgs with book_slot's
#    seven arguments, all text and all required:
#      technician_id, date, slot, job, area, customer_name,
#      phone
#    slot may only be morning, afternoon or evening. Give
#    every field a description, and forbid unknown keys.
#
# 2. Make BOOK_SLOT_TOOL: a tool description named book_slot,
#    with a one-sentence description, whose parameters are
#    BookSlotArgs's JSON Schema.
#
# 3. When the file is run (python3 booking_args.py), send
#    lab-chat a system message (GharFix's booking assistant,
#    today is 2026-10-22) and the user's message, exactly:
#
#      Book T29 for a door lock change in Indiranagar on 27
#      Oct, afternoon. I am Kavya Iyer, phone 9900112233.
#      (one line, as in the task)
#
#    with BOOK_SLOT_TOOL as the only tool. Validate the
#    call's arguments with BookSlotArgs, book with
#    gharfix.book_slot and those arguments, and print:
#
#      <booking ID> <status>
#
# Careful: the model's arguments are JSON text. Validate
# them before you book anything.
#
# Stuck? Press "What do I do next?" under this task. Write
# your code below.
from typing import Literal

from openai import OpenAI
from pydantic import BaseModel, ConfigDict, Field

import gharfix


class BookSlotArgs(BaseModel):
    model_config = ConfigDict(extra="forbid")
    technician_id: str = Field(description="A technician's id, like T07")
    date: str = Field(description="The date, YYYY-MM-DD")
    slot: Literal["morning", "afternoon", "evening"] = Field(description="morning (9-12), afternoon (13-16) or evening (17-20)")
    job: str = Field(description="The job's id on the rate card, like leak-fix")
    area: str = Field(description="The customer's area in Bengaluru")
    customer_name: str = Field(description="The customer's full name")
    phone: str = Field(description="The customer's 10-digit phone number")


BOOK_SLOT_TOOL = {
    "type": "function",
    "function": {
        "name": "book_slot",
        "description": "Reserve a free slot of a technician for a job at the customer's area.",
        "parameters": BookSlotArgs.model_json_schema(),
    },
}

if __name__ == "__main__":
    client = OpenAI()
    response = client.chat.completions.create(
        model="lab-chat",
        messages=[
            {"role": "system", "content": "You are GharFix's booking assistant. Today is 2026-10-22."},
            {"role": "user", "content": "Book T29 for a door lock change in Indiranagar on 27 Oct, afternoon. I am Kavya Iyer, phone 9900112233."},
        ],
        tools=[BOOK_SLOT_TOOL],
    )
    call = response.choices[0].message.tool_calls[0]
    args = BookSlotArgs.model_validate_json(call.function.arguments)
    booking = gharfix.book_slot(**args.model_dump())
    print(booking["booking_id"], booking["status"])
