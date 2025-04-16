from typing import List
from datetime import datetime

import requests
from lxml.etree import (
    HTMLParser,
    _Element,
    fromstring,
)

from revi_toolbox.scraper.utility import clean_str, etree_xpath, etree_xpath_first
from revi_toolbox.scraper.manga.schemas import MangaOverview, MangaChapter


class MangabatsScraperRunner:
    BASE_URL: str = "https://www.mangabats.com/manga/{slug}"


    # Public
    def scrape_overview(self, slug: str) -> MangaOverview:
        manga_page = self.__get_manga_page(slug)
        overview = self.__parse_overview(manga_page, slug)

        return overview


    def scrape_chapters(self, slug: str, latest_only: bool = True) -> List[MangaChapter]:
        manga_page = self.__get_manga_page(slug)
        chapters = self.__parse_chapters(manga_page, slug, latest_only)

        return chapters


    # Private
    def __get_manga_page(self, slug: str) -> _Element:
        # Fetch Manga Page
        manga_url = self.BASE_URL.format(slug=slug)
        req = requests.get(manga_url)
        req.raise_for_status()

        # Parse Manga Page content
        raw_content = req.content
        page_content = fromstring(raw_content, HTMLParser())
        return page_content


    def __parse_chapters(self, page: _Element, slug: str, latest_only: bool = True) -> List[MangaChapter]:
        # Parse Chapter List
        chapter_list = etree_xpath(page, "//div[@class='chapter-list']/div[@class='row']")
        
        mc_list: List[MangaChapter] = []
        for ch in chapter_list:
            # Parse - Chapter Columns
            ch_cols = etree_xpath(ch, "./span")
            
            chapter_title = etree_xpath_first(ch_cols[0], "./a")
            updated_at =  ch_cols[2]
            
            # Validate Model
            mc = MangaChapter(
                code = slug,
                chapter_title = chapter_title.text,
                chapter_url = chapter_title.get("href"),
                updated_at = datetime.strptime(
                    str(updated_at.get("title")),
                    "%b-%d-%Y %H:%M"
                )
            )
            mc_list.append(mc)
        
        if latest_only:
            mc_list = [max(mc_list, key=lambda d: d.updated_at)]
        return mc_list



    def __parse_overview(self, page: _Element, slug: str) -> MangaOverview:
        # Parse - Info Section
        info_rows = etree_xpath(page, "//ul[@class='manga-info-text']/li")
        title = etree_xpath_first(info_rows[0], "./h1")
        authors = etree_xpath(info_rows[1], "./a")
        status = info_rows[2]
        last_updated = info_rows[3]
        total_views = info_rows[5]
        genres = etree_xpath(info_rows[6], "./a")
        
        # Parse - Chapter List
        chapter_list = etree_xpath(page, "//div[@class='chapter-list']/div[@class='row']")

        # Validate Model
        mo = MangaOverview(
            code = slug,
            title = title.text,
            authors = [clean_str(a.text) for a in authors],
            genres = [clean_str(g.text) for g in genres],
            total_chapters = len(chapter_list),
            total_views = int(
                str(total_views.text).replace("View : ", "").replace(",", "")
            ),
            is_completed = (status.text == "Status : Completed"),
            last_updated = datetime.strptime(
                str(last_updated.text).replace("Last updated : ", ""),
                "%b-%d-%Y %H:%M:%S %p"
            )
        )
        return mo
        