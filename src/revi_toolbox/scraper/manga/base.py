from typing import List, Protocol

from revi_toolbox.scraper.manga.schemas import MangaChapter, MangaOverview


class MangaScraperRunner(Protocol):
    def scrape_overview(self, slug: str) -> MangaOverview:
        pass
    
    def scrape_chapters(self, slug: str, latest_only: bool = True) -> List[MangaChapter]:
        pass