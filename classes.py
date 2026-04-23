from pydantic import BaseModel

class UserInput(BaseModel):
    text: str
    image_url: str