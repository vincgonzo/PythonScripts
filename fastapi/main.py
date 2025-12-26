# from openai import OpenAI 
import os
import logging
import uvicorn
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Any, Dict, List, Optional, Union
from fastapi import FastAPI
from logging.handlers import TimedRotatingFileHandler

from app.core.config import settings
load_dotenv()  


app = FastAPI(title=settings.PROJECT_NAME)

def log_to_cmd_and_rotate_file():
    rotating_file_handler = TimedRotatingFileHandler(
        filename=f"{os.getenv("ROOT_DIR")}/logs/fastlog.log", when="midnight", interval=1, backupCount=0
    )


    formatter = logging.Formatter('%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    cmd_handler = logging.StreamHandler()
    cmd_handler.setLevel(logging.INFO)
    cmd_handler.setFormatter(formatter)


    root = logging.getLogger()
    root.setLevel(logging.INFO)

    logging.info("Starting tool")

    rotating_file_handler.setLevel(logging.INFO)
    rotating_file_handler.setFormatter(formatter)

    root.addHandler(cmd_handler)
    root.addHandler(rotating_file_handler)

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



class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

@app.get("/")
async def homepage():
    return {"Hello": "Root of the World!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}

if __name__ == "__main__":
    log_to_cmd_and_rotate_file()
    uvicorn.run(app, host="localhost", port=8123, log_level="debug")