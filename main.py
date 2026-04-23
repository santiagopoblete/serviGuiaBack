from dotenv import load_dotenv
from fastapi import FastAPI
from openai import OpenAI

from classes import UserInput
from chat_functions import build_content

load_dotenv()


app = FastAPI()
client = OpenAI()

@app.get("/")
async def read_root():
    return {"ServiGuia x Equipo de Cuatro"}

@app.post("/chat")
async def user_question(input: UserInput):
    content = build_content(input)

    response = client.responses.create(
        model="gpt-5-nano",
        input=[
            # {
            #     "role": "system",
            #     "content": [
            #         {
            #             "type": "input_text",
            #             "text": "Eres un asistente virtual llamado ServiGuia ..." #! AQUÍ VA EL MASTER PROMPT
            #         }
            #      ]
            # },
            {
                "role": "user",
                "content": content
            }
        ],
    )

    # TODO: Aquí se llamará a la función que se haga que devuelva la lista de proveedores a mostrar (NO LA LLAMADA A LA BASE DE DATOS,
    # TODO:  SINO YA DESPUES DE ESCOGER LAS RECOMENDACIONES DE PROVEEDORES) y se agregará a la respuesta del modelo (response.output_text).

    return response.output_text # TODO: Mientras se hace la función anterior, se devuelve la respuesta del modelo, pero debe regresar la lista de proveedores.