from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel


class MangaOverview(BaseModel):
    code: str
    title: str
    author: List[str]
    genres: List[str]
    total_chapters: int
    total_views: int
    is_complete: bool
    last_updated: datetime


class MangaChapter(BaseModel):
    code: str
    chapter_title: str
    chapter_url: str
    updated_at: datetime
