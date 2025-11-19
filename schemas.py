"""
Database Schemas for Whiskers game site

Each Pydantic model corresponds to a MongoDB collection with the lowercase
class name as the collection name.
"""
from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime


class Devlogpost(BaseModel):
    """
    Collection: "devlogpost"
    A development log entry about progress, features, or updates.
    """
    title: str = Field(..., description="Post title")
    summary: Optional[str] = Field(None, description="Short summary for previews")
    content: str = Field(..., description="Full markdown or text content")
    cover_image: Optional[str] = Field(None, description="Optional image URL")
    tags: List[str] = Field(default_factory=list, description="Topic tags")
    published_at: Optional[datetime] = Field(None, description="Optional publish date")


class Milestone(BaseModel):
    """
    Collection: "milestone"
    Roadmap milestones for the project.
    """
    title: str = Field(..., description="Milestone title")
    description: Optional[str] = Field(None, description="What this milestone includes")
    status: str = Field("planned", description="planned | in_progress | done")
    target_date: Optional[datetime] = Field(None, description="Target completion date")


class Feedback(BaseModel):
    """
    Collection: "feedback"
    Visitor feedback or playtest notes.
    """
    name: Optional[str] = Field(None, description="Visitor name")
    email: Optional[str] = Field(None, description="Contact email")
    message: str = Field(..., description="Feedback message")
    topic: Optional[str] = Field(None, description="e.g., bug, idea, question")
