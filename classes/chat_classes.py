from pydantic import BaseModel
from enum import Enum
from typing import Literal

class UserMessage(BaseModel):
    role: Literal["user"]
    text: str | None = None
    image_url: str | None = None

class AssistantMessage(BaseModel):
    role: Literal["assistant"]
    text: str
    providers: list[tuple[str, float]] | None = None

class UserInput(BaseModel):
    conversacion: list[UserMessage | AssistantMessage]

class UrgencyLevel(str, Enum):
    CRITICO = "CRÍTICO"
    MODERADO = "MODERADO"
    NORMAL = "NORMAL"

class PriceRange(BaseModel):
    min: int
    max: int

class UserNeeds(BaseModel):
    user_expected_expertise: float = 0.0 # Valor entre 0 y 5
    user_price_range: PriceRange = PriceRange(min=0, max=0)
    category: str = ""
    subcategory: str = ""

class AIResponse(BaseModel):
    nivel_urgencia: UrgencyLevel
    es_emergencia: bool
    accion_inmediata: str | None = None # Solo proveer si la urgencia es crítica o moderada
    categoria_detectada: str | None = None # Es necesario poner las categorías disponibles
    pregunta_seguimiento: str | None = None # Solo proveer si el input del usuario es ambiguo
    resumen_diagnostico: str
    numero_emergencia: str | None = None
    pregunta_necesidades_usuario: str | None = None # Solo proveer si el input del usuario no es suficiente para entender sus necesidades (por ejemplo, si no se especifica un rango de precios o nivel de experiencia esperado)
    necesidades_usuario: UserNeeds # Este campo no será parte del output a devolver al usuario, sino que se usará internamente para el sistema de recomendación.
    proveedores_sugeridos: list[list[str],list[str]] | None = None # Lista de IDs de proveedores sugeridos, solo se proveerá después de hacer la recomendación basada en las necesidades del usuario.