# tests/test_smoke_openai.py

from openai import OpenAI
from pydantic import BaseModel


class SmokeResponse(BaseModel):
    status: str


def test_openai_parse():
    client = OpenAI()

    response = client.responses.parse(
        model="gpt-5-nano",
        input="Return status='ok'",
        text_format=SmokeResponse,
    )

    assert response.output_parsed.status.lower() == "ok"