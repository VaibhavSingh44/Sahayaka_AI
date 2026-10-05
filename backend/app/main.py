import os

from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

base_dir = Path(__file__).resolve().parent.parent.parent
env_path = base_dir / '.env'

load_dotenv(dotenv_path=env_path)

api_key = os.getenv("My_API_Key")
model = os.getenv("My_Model")

if not api_key:
    raise ValueError("NVIDIA_API_KEY was not found in .env")

if not model:
    raise ValueError("NVIDIA_MODEL was not found in .env")

print("Model:", model)
print("API key loaded:", bool(api_key))

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key = api_key
)

question = input("Ask Sahayaka AI: ")

print("MODEL:", model)
print("QUESTION:", question)

# Generic chatbot system 

# response = client.chat.completions.create(
#     model = model,
#     messages = [
#         {
#             "role": "user",
#             "content": question
#         }
#     ]
# )


# Integrating System Prompt

from prompts import SYSTEM_PROMPT

response = client.chat.completions.create(
    model = model,
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": question
        }
    ]
)

answer = response.choices[0].message.content

print()
print("Sahayaka AI: ")
print(answer)

