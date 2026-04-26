from pydantic import BaseModel
from enum import Enum

class UserInput(BaseModel):
    text: str
    image_url: str

class UrgencyLevel(str, Enum):
    CRITICO = "CRÍTICO"
    MODERADO = "MODERADO"
    NORMAL = "NORMAL"

class AIResponse(BaseModel):
    nivel_urgencia: UrgencyLevel
    es_emergencia: bool
    accion_inmediata: str | None = None # Solo proveer si la urgencia es crítica o moderada
    categoria_detectada: str | None = None # Es necesario poner las categorías disponibles
    pregunta_seguimiento: str | None = None # Solo proveer si el input del usuario es ambiguo
    resumen_diagnostico: str
    numero_emergencia: str | None = None
    # proveedores_sugeridos será agregado después de correr el sistema de recomendación