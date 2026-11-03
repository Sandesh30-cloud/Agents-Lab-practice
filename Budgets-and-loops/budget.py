# Task 3: a budget in tokens and rupees
#
# Write a class Budget(max_tokens=None, max_rupees=None):
#
#   .tokens, .rupees   totals so far, starting at 0
#   .add(model, usage) adds one response's usage: its prompt
#                      and completion tokens to .tokens, and
#                      their price to .rupees
#   .over()            True when tokens are more than
#                      max_tokens, or rupees more than
#                      max_rupees (a limit of None is none)
#
# Prices come from the lab's model list (the same as
# lab models): each model has price_inr_per_million with
# input, cached_input and output. A response's cached
# prompt tokens (usage.prompt_tokens_details.cached_tokens)
# cost cached_input; the rest of its prompt tokens input.
#
# Then run_agent(question, model="lab-chat", budget=None):
# task 1's loop with at most 10 requests. After every
# request, add its usage to the budget. If the model
# answered, return (answer, "answered"); otherwise, if the
# budget is over, return (None, "budget") without running
# the calls. After 10 requests: (None, "max_steps").
#
# Careful: count the request that went over. It was sent,
# and it is paid for.
#
# Stuck? Press "What do I do next?" under this task. Write
# your code below.
import json

from openai import OpenAI

import gharfix

client = OpenAI()
SYSTEM = "You are GharFix's booking assistant in Bengaluru. Today is 2026-10-22. Use the tools."


class Budget:
    def __init__(self, max_tokens=None, max_rupees=None):
        self.max_tokens = max_tokens
        self.max_rupees = max_rupees
        self.tokens = 0
        self.rupees = 0.0
        self.prices = {m.id: m.price_inr_per_million for m in client.models.list().data if getattr(m, "price_inr_per_million", None)}

    def add(self, model, usage):
        price = self.prices[model]
        details = getattr(usage, "prompt_tokens_details", None)
        cached = (getattr(details, "cached_tokens", None) or 0) if details else 0
        self.tokens += usage.prompt_tokens + usage.completion_tokens
        self.rupees += ((usage.prompt_tokens - cached) * price["input"] + cached * price["cached_input"] + usage.completion_tokens * price["output"]) / 1_000_000

    def over(self):
        return (self.max_tokens is not None and self.tokens > self.max_tokens) or (self.max_rupees is not None and self.rupees > self.max_rupees)


def run_agent(question, model="lab-chat", budget=None):
    budget = budget or Budget()
    messages = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": question}]
    for _ in range(10):
        response = client.chat.completions.create(model=model, messages=messages, tools=gharfix.TOOLS)
        budget.add(model, response.usage)
        message = response.choices[0].message
        if response.choices[0].finish_reason == "stop":
            return message.content, "answered"
        if budget.over():
            return None, "budget"
        messages.append(message)
        for call in message.tool_calls:
            result = gharfix.FUNCTIONS[call.function.name](**json.loads(call.function.arguments))
            messages.append({"role": "tool", "tool_call_id": call.id, "content": json.dumps(result)})
    return None, "max_steps"


if __name__ == "__main__":
    b = Budget(max_rupees=1)
    print(run_agent("Is GF424921 confirmed?", model="lab-chat-loopy", budget=b))
    print(f"{b.tokens} tokens, ₹{b.rupees:.4f}")
