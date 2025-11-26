# from openai import OpenAI 
import os
from dotenv import load_dotenv
from fastapi import FastAPI
load_dotenv()  


# OpenAI.api_key = os.getenv("OPENAI_API_KEY")
# client = OpenAI()

# assistant = client.chat.completions.create(
#     model="gpt-3.5-turbo",
#     messages=[{
#         "role":"system", "content": "Your helpful assistant",
#         "role":"user", "content": "write a haiku about ai"
#     }],
# )

# print(completions.choices)