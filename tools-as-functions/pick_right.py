# Task 4 (interview question): two tools the model confuses
#
# This offers lab-chat two tools and prints which one the
# model picks for each of six customer messages:
#
#   gf_lookup  will run gharfix.get_booking
#   gf_close   will run gharfix.cancel_booking
#
# Run it with python3 pick_right.py. Five of the six lines
# are wrong: the model picks the wrong tool, or answers from
# its training without any tool.
#
# Rewrite the two descriptions (and the booking_id
# parameter's description) so that the model picks gf_lookup
# for the three questions about a booking's status, and
# gf_close for the three cancellations.
#
# Keep the two names, the one required parameter booking_id,
# the six messages and what the program prints.
#
# Careful: the model never sees your code, only these
# descriptions. Could a new colleague tell the tools apart
# from them?
#
# Stuck? Press "What do I do next?" under this task.

from openai import OpenAI

client = OpenAI()

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "gf_lookup",
            "description": "Check the status of a booking: is it confirmed, and when is the technician coming.",
            "parameters": {
                "type": "object",
                "properties": {"booking_id": {"type": "string", "description": "The booking ID: GF and 6 digits"}},
                "required": ["booking_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "gf_close",
            "description": "Cancel a booking when the customer asks to cancel it; the refund follows the policy.",
            "parameters": {
                "type": "object",
                "properties": {"booking_id": {"type": "string", "description": "The booking ID: GF and 6 digits"}},
                "required": ["booking_id"],
            },
        },
    },
]

MESSAGES = [
    "Is my booking GF424921 confirmed?",
    "Please cancel GF186543.",
    "When is the technician coming for GF318075?",
    "I want to cancel booking GF990001, plans changed.",
    "GF894117 ka status kya hai?",
    "GF825369 cancel maadi please",
]


def picked(text):
    response = client.chat.completions.create(
        model="lab-chat",
        messages=[
            {"role": "system", "content": "You are GharFix's booking assistant. Today is 2026-10-22."},
            {"role": "user", "content": text},
        ],
        tools=TOOLS,
    )
    message = response.choices[0].message
    if message.tool_calls:
        return message.tool_calls[0].function.name
    return "no tool: " + message.content


if __name__ == "__main__":
    for text in MESSAGES:
        print(f"{text} -> {picked(text)}")
