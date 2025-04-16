from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel


class MangaOverview(BaseModel):
    code: str
    title: str
    authors: List[str]
    genres: List[str]
    total_chapters: int
    total_views: int
    is_completed: bool
    last_updated: datetime


class MangaChapter(BaseModel):
    code: str
    chapter_title: str
    chapter_url: str
    updated_at: datetime
