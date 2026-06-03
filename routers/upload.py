from __future__ import annotations

import os

import cloudinary
import cloudinary.uploader
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from starlette.concurrency import run_in_threadpool


router = APIRouter(tags=["upload"])

# Límite de tamaño (~10 MB) para las imágenes subidas.
MAX_FILE_SIZE = 10 * 1024 * 1024


def configure_cloudinary():
    """Configura el SDK de Cloudinary desde variables de entorno.

    Si existe CLOUDINARY_URL, el SDK la toma automáticamente. En caso
    contrario se usan CLOUDINARY_CLOUD_NAME / CLOUDINARY_API_KEY /
    CLOUDINARY_API_SECRET.
    """
    if os.getenv("CLOUDINARY_URL"):
        cloudinary.config(secure=True)
        return

    cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME")
    api_key = os.getenv("CLOUDINARY_API_KEY")
    api_secret = os.getenv("CLOUDINARY_API_SECRET")

    if not cloud_name or not api_key or not api_secret:
        raise RuntimeError("Las credenciales de Cloudinary no están configuradas")

    cloudinary.config(
        cloud_name=cloud_name,
        api_key=api_key,
        api_secret=api_secret,
        secure=True,
    )


@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    # 1. Validar que el archivo sea una imagen.
    if not file.content_type or not file.content_type.startswith("image/"):
        return JSONResponse(
            status_code=400,
            content={"error": "El archivo debe ser una imagen"},
        )

    # 2. Leer el contenido y validar el tamaño (~10 MB).
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        return JSONResponse(
            status_code=413,
            content={"error": "La imagen supera el tamaño máximo permitido (10 MB)"},
        )

    # 3. Configurar Cloudinary y subir la imagen.
    try:
        configure_cloudinary()
        result = await run_in_threadpool(
            cloudinary.uploader.upload,
            contents,
            folder="serviguia",
            resource_type="image",
        )
    except Exception as exc:
        return JSONResponse(
            status_code=500,
            content={"error": f"No se pudo subir la imagen: {exc}"},
        )
    finally:
        await file.close()

    return {"url": result["secure_url"]}
