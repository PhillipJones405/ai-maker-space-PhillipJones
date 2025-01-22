# tests.py

import asyncio
from app import get_llm_response  # Import the reusable function

# List of test questions
questions = [
    "Explain the concept of object-oriented programming in simple terms to a complete beginner."
    ,"Read the following paragraph and provide a concise summary of the key points…"
    ,"Write a short, imaginative story (100–150 words) about a robot finding friendship in an unexpected place."
    ,"If a store sells apples in packs of 4 and oranges in packs of 3, how many packs of each do I need to buy to get exactly 12 apples and 9 oranges?"
    ,"Rewrite the following paragraph in a professional, formal tone…"
]


async def run_test():
    for question in questions:
        print(f"Question: {question}")
        response = await get_llm_response(question)
        print(f"Answer: {response}")
        print("-" * 50)


if __name__ == "__main__":
    asyncio.run(run_test())
