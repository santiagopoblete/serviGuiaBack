import os
from dotenv import load_dotenv
from fastapi import FastAPI
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()

app = FastAPI()
client = OpenAI()

class UserInput(BaseModel):
    question: str

@app.get("/")
async def read_root():
    return {"ServiGuia x Equipo de Cuatro"}

@app.post("/chat")
async def user_question(input: UserInput):
    response = client.responses.create(
        model="gpt-5-nano",
        # instructions="Talk like a pirate.",
        input=input.question,
    )
    return response.output_text