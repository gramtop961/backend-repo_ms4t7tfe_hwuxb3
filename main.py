import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from bson.objectid import ObjectId

from database import db, create_document, get_documents
from schemas import Devlogpost, Milestone, Feedback

app = FastAPI(title="Whiskers Game Site API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Whiskers API running"}


@app.get("/test")
def test_database():
    """Quick status + list some collections if available"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:60]}"
        else:
            response["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:60]}"

    return response


# Helper to serialize Mongo ObjectId
class DevlogPostOut(BaseModel):
    id: str
    title: str
    summary: Optional[str]
    content: str
    cover_image: Optional[str]
    tags: List[str] = []
    published_at: Optional[str]


@app.post("/api/devlog", response_model=dict)
async def create_devlog(post: Devlogpost):
    inserted_id = create_document("devlogpost", post)
    return {"id": inserted_id}


@app.get("/api/devlog", response_model=List[DevlogPostOut])
async def list_devlog(limit: int = 20):
    docs = get_documents("devlogpost", {}, limit)
    out: List[DevlogPostOut] = []
    for d in docs:
        out.append(DevlogPostOut(
            id=str(d.get("_id")),
            title=d.get("title"),
            summary=d.get("summary"),
            content=d.get("content"),
            cover_image=d.get("cover_image"),
            tags=d.get("tags", []),
            published_at=(d.get("published_at").isoformat() if d.get("published_at") else None)
        ))
    return out


class MilestoneOut(BaseModel):
    id: str
    title: str
    description: Optional[str]
    status: str
    target_date: Optional[str]


@app.post("/api/milestones", response_model=dict)
async def create_milestone(milestone: Milestone):
    inserted_id = create_document("milestone", milestone)
    return {"id": inserted_id}


@app.get("/api/milestones", response_model=List[MilestoneOut])
async def list_milestones(limit: int = 50):
    docs = get_documents("milestone", {}, limit)
    out: List[MilestoneOut] = []
    for d in docs:
        out.append(MilestoneOut(
            id=str(d.get("_id")),
            title=d.get("title"),
            description=d.get("description"),
            status=d.get("status"),
            target_date=(d.get("target_date").isoformat() if d.get("target_date") else None)
        ))
    return out


@app.post("/api/feedback", response_model=dict)
async def create_feedback(feedback: Feedback):
    inserted_id = create_document("feedback", feedback)
    return {"id": inserted_id}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
