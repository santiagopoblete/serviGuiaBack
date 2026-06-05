from dotenv import load_dotenv
from fastapi import FastAPI, Request
from openai import OpenAI

from slowapi import Limiter , _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded

from classes.chat_classes import UserInput, AIResponse
from functions.chat_functions import build_content, load_master_prompt
from functions.weight_functions import load_workers_from_db, output_workers

from fastapi.middleware.cors import CORSMiddleware


load_dotenv()

app = FastAPI()
client = OpenAI()
MASTER_PROMPT = load_master_prompt()

origins = [
  "http://localhost:3000"
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,        # use ["*"] only for testing
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

def real_ip(request: Request):
    return request.headers.get("X-Forwarded-For", request.client.host)

limiter = Limiter(key_func=real_ip)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)


@app.get("/")
async def read_root():
    return {"message": "ServiGuia x Equipo de Cuatro"}


@app.post("/chat")
@limiter.limit("5/minute")
async def user_question(request: Request, input: UserInput):
    content = build_content(input) # Construye la conversacion en el formato que OpenAI espera

    response = client.responses.parse(
        model="gpt-5-nano",
        instructions=MASTER_PROMPT,
        input=content,
        text_format=AIResponse,
    )

    if not response.output_parsed.es_emergencia and not (
        response.output_parsed.pregunta_seguimiento or
        response.output_parsed.pregunta_necesidades_usuario
    ):
        user_needs = response.output_parsed.necesidades_usuario

        workers = await load_workers_from_db()

        filtered = output_workers(
            workers,
            user_needs.category,
            user_needs.user_expected_expertise,
            (user_needs.user_price_range.min, user_needs.user_price_range.max)
        )

        response.output_parsed.proveedores_sugeridos = filtered
    else:
        response.output_parsed.proveedores_sugeridos = None

    return response.output_parsed