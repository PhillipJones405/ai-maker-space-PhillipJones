# app.py

import os
from openai import AsyncOpenAI  # importing openai for API usage
import chainlit as cl  # importing chainlit for our app
from chainlit.prompt import Prompt, PromptMessage  # importing prompt tools
from chainlit.playground.providers import ChatOpenAI  # importing ChatOpenAI tools
from dotenv import load_dotenv

load_dotenv()

# ChatOpenAI Templates
system_template = """
You are a highly knowledgeable and helpful assistant with expertise in a wide range of topics.
Your responses should always be detailed, clear, and well-structured, and you should strive to explain concepts in a way that is easy to understand.
Speak in a pleasant and professional tone, and provide examples or analogies where appropriate.
If the question is open-ended, consider multiple perspectives or approaches in your response.
"""


user_template = """
{input}
Please think through your response step by step, and provide examples or references to support your answer where possible.
Focus on being clear, concise, and engaging.
"""

# LLM settings
def get_default_settings():
    return {
        "model": "gpt-3.5-turbo",
        "temperature": 0.3,
        "max_tokens": 800,
        "top_p": 1,
        "frequency_penalty": 0.2,
        "presence_penalty": 0,
    }

# Create prompt object
def create_prompt(input_text):
    return Prompt(
        provider=ChatOpenAI.id,
        messages=[
            PromptMessage(
                role="system",
                template=system_template,
                formatted=system_template,
            ),
            PromptMessage(
                role="user",
                template=user_template,
                formatted=user_template.format(input=input_text),
            ),
        ],
        inputs={"input": input_text},
        settings=get_default_settings(),
    )

# LLM interaction function
async def get_llm_response(input_text):
    client = AsyncOpenAI()
    prompt = create_prompt(input_text)

    response = ""
    async for stream_resp in await client.chat.completions.create(
        messages=[m.to_openai() for m in prompt.messages],
        stream=True,
        **prompt.settings,
    ):
        token = stream_resp.choices[0].delta.content
        if token:
            response += token

    return response


@cl.on_chat_start
async def start_chat():
    cl.user_session.set("settings", get_default_settings())


@cl.on_message
async def main(message: cl.Message):
    response = await get_llm_response(message.content)
    msg = cl.Message(content=response)
    await msg.send()
