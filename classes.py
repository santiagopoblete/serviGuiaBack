from pydantic import BaseModel
from typing import Optional

class UserInput(BaseModel):
    text: str
    image_url: str

from pydantic import BaseModel, Field

class Worker(BaseModel):
    model_config = {"populate_by_name": True}

    id: str
    name: str                   = Field(alias="nombre")
    categories: list[str]       = Field(alias="categorias")
    global_rating: float        = Field(alias="calificacion_global")
    badges: list[str]           = Field(alias="insignias")
    available: bool             = Field(alias="disponible")
    price_from: int             = Field(alias="precio_desde")
    price_to: int               = Field(alias="precio_hasta")
    total_reviews: int

class WorkerUpdate(BaseModel):
    available: Optional[bool] = None
    global_rating: Optional[float] = None
    price_from: Optional[int] = None
    price_to: Optional[int] = None