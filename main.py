from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"ServiGuia x Equipo de Cuatro"}