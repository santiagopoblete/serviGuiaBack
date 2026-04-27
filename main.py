import os
from dotenv import load_dotenv
from fastapi import FastAPI
from openai import OpenAI

from classes.chat_classes import UserInput
from classes.chat_classes import AIResponse
from functions.chat_functions import build_content, load_master_prompt

load_dotenv()


app = FastAPI()
client = OpenAI()
MASTER_PROMPT = load_master_prompt()

@app.get("/")
async def read_root():
    return {"ServiGuia x Equipo de Cuatro"}

@app.post("/chat")
async def user_question(input: UserInput):
    content = build_content(input)

    response = client.responses.parse(
        model="gpt-5-nano",
        instructions=MASTER_PROMPT,
        input=[
            {
                "role": "user",
                "content": content
            }
        ],
        text_format=AIResponse,
    )

    # TODO: Aquí se llamará a la función que se haga que devuelva la lista de proveedores a mostrar (NO LA LLAMADA A LA BASE DE DATOS,
    # TODO:  SINO YA DESPUES DE ESCOGER LAS RECOMENDACIONES DE PROVEEDORES) y se agregará a la respuesta del modelo (response.output_text).

    return response.output_parsed # TODO: Mientras se hace la función anterior, se devuelve la respuesta del modelo, pero debe regresar la lista de proveedores tambien.