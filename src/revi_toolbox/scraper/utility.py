import re
from typing import List, Optional

from lxml.etree import _Element


def clean_str(s: str) -> str:
    _s = re.sub(r'^[ \n\t]+', "", s)
    _s = re.sub(r'[ \n\t]+$', "", _s)
    _s = re.sub(r'[ ]+', " ", _s)
    return _s


def etree_xpath(el: _Element, xpath_query: str) -> List[_Element]:
    results: List[_Element] = el.xpath(xpath_query)
    return results

def etree_xpath_first(el: _Element, xpath_query: str) -> Optional[_Element]:
    results = etree_xpath(el, xpath_query)
    if (results):
        return results[0]
