from fastapi import APIRouter, HTTPException
from app.database import get_db
from app.models import Worker, WorkerUpdate
from typing import Optional

router = APIRouter(prefix="/workers", tags=["workers"])

@router.get("/")
async def list_workers(
    category: Optional[str] = None,
    available: Optional[bool] = None,
    min_rating: Optional[float] = None,
):
    db = get_db()
    filters = {}

    if category:
        filters["categories"] = category
    if available is not None:
        filters["available"] = available
    if min_rating:
        filters["global_rating"] = {"$gte": min_rating}

    workers = await db.workers.find(filters).to_list(100)
    for worker in workers:
        worker["_id"] = str(worker["_id"])
    return workers


@router.get("/{worker_id}")
async def get_worker(worker_id: str):
    db = get_db()
    worker = await db.workers.find_one({"id": worker_id})
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    worker["_id"] = str(worker["_id"])
    return worker


@router.post("/", status_code=201)
async def create_worker(worker: Worker):
    db = get_db()
    existing = await db.workers.find_one({"id": worker.id})
    if existing:
        raise HTTPException(status_code=400, detail="ID already exists")
    await db.workers.insert_one(worker.model_dump())
    return {"message": "Worker created", "id": worker.id}


@router.patch("/{worker_id}")
async def update_worker(worker_id: str, data: WorkerUpdate):
    db = get_db()
    changes = {k: v for k, v in data.model_dump().items() if v is not None}
    if not changes:
        raise HTTPException(status_code=400, detail="Nothing to update")
    result = await db.workers.update_one(
        {"id": worker_id}, {"$set": changes}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Worker not found")
    return {"message": "Updated successfully"}


@router.delete("/{worker_id}")
async def delete_worker(worker_id: str):
    db = get_db()
    result = await db.workers.delete_one({"id": worker_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Worker not found")
    return {"message": "Deleted successfully"}