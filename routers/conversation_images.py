from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Optional

import cloudinary
import cloudinary.uploader
from cloudinary import CloudinaryImage
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pymongo.errors import PyMongoError
from starlette.concurrency import run_in_threadpool

from database import get_db


router = APIRouter(prefix="/conversations", tags=["conversation-images"])


def configure_cloudinary():
    cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME")
    api_key = os.getenv("CLOUDINARY_API_KEY")
    api_secret = os.getenv("CLOUDINARY_API_SECRET")

    if not cloud_name or not api_key or not api_secret:
        raise HTTPException(
            status_code=500,
            detail="Cloudinary credentials are not configured",
        )

    cloudinary.config(
        cloud_name=cloud_name,
        api_key=api_key,
        api_secret=api_secret,
        secure=True,
    )


@router.post("/{conversation_id}/images", status_code=201)
async def upload_conversation_image(
    conversation_id: str,
    image: UploadFile = File(...),
    user_id: Optional[str] = Form(default=None),
    message_id: Optional[str] = Form(default=None),
):
    if not image.content_type or not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="The uploaded file must be an image")

    configure_cloudinary()

    try:
        upload_result = await run_in_threadpool(
            cloudinary.uploader.upload,
            image.file,
            folder=f"serviguia/conversations/{conversation_id}",
            resource_type="image",
            use_filename=True,
            unique_filename=True,
            overwrite=False,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Could not upload image to Cloudinary: {exc}",
        ) from exc
    finally:
        await image.close()

    now = datetime.now(timezone.utc)
    optimized_url = CloudinaryImage(upload_result["public_id"]).build_url(
        fetch_format="auto",
        quality="auto",
        secure=True,
    )
    image_document = {
        "conversation_id": conversation_id,
        "message_id": message_id,
        "user_id": user_id,
        "public_id": upload_result["public_id"],
        "secure_url": upload_result["secure_url"],
        "optimized_url": optimized_url,
        "format": upload_result.get("format"),
        "bytes": upload_result.get("bytes"),
        "width": upload_result.get("width"),
        "height": upload_result.get("height"),
        "created_at": now,
    }

    db = get_db()
    try:
        insert_result = await db.conversation_images.insert_one(image_document)
    except PyMongoError as exc:
        await run_in_threadpool(
            cloudinary.uploader.destroy,
            upload_result["public_id"],
            resource_type="image",
        )
        raise HTTPException(
            status_code=503,
            detail=f"Image uploaded to Cloudinary, but could not be saved in MongoDB: {exc}",
        ) from exc

    return {
        "id": str(insert_result.inserted_id),
        "conversation_id": conversation_id,
        "message_id": message_id,
        "user_id": user_id,
        "public_id": image_document["public_id"],
        "secure_url": image_document["secure_url"],
        "optimized_url": image_document["optimized_url"],
        "format": image_document["format"],
        "bytes": image_document["bytes"],
        "width": image_document["width"],
        "height": image_document["height"],
        "created_at": now.isoformat(),
    }


@router.get("/{conversation_id}/images")
async def list_conversation_images(conversation_id: str):
    db = get_db()
    try:
        images = await db.conversation_images.find(
            {"conversation_id": conversation_id}
        ).sort("created_at", 1).to_list(1000)
    except PyMongoError as exc:
        raise HTTPException(
            status_code=503,
            detail=f"Could not read conversation images from MongoDB: {exc}",
        ) from exc

    for image in images:
        image["id"] = str(image.pop("_id"))
        if isinstance(image.get("created_at"), datetime):
            image["created_at"] = image["created_at"].isoformat()

    return images
