from __future__ import annotations

import enum
from urllib.parse import parse_qsl, urlparse
from . import scrap

URL = scrap.URL.geturl()
DB = "/boeapps/database/"

class Endpoint(enum.Enum):
    index = "index.asp"
    topic = "BankStats.asp"
    category = "CategoryIndex.asp"
    column = "FromShowColumns.asp"


def build_cache(params):
    all_categories = _get_all()

    # these items are the same as items from `all` except from `Travel`
    # parameter. Let's ignore them, as I don't see what `Travel` does.
    # categories = _get_categories()
    # sectors = _get_sectors()
    # countries = _get_countries()

    for category, params in all_categories.items():
        columns = _list_columns(dict(params))



def _get_all():
    return _get_category({"CategId": "allcats", "CategName": "Combined A to Z"})

def _get_categories():
    return _get_category({"CategId": "6", "CategName": "INSTRUMENTS"})

def _get_sectors():
    return _get_category({"CategId": "sectorcats", "CategName": "SECTOR"})

def _get_countries():
    return _get_category({"CategId": "9", "CategName": "COUNTRY"})

def _get_category(params):
    url = URL + DB + Endpoint.category.value
    page = scrap.get_page(url, params, use_proxy=True)
    links = page.dom.body.select(".page-section table tr td>.pagetext>a")
    mapping = {
        a.text: sorted(parse_qsl(urlparse(a['href']).query))
        for a in links
    }

    for key, params in mapping.items():
        assert len(dict(params)) == len(params), f"Repeating param for {key}: {params}"
    return mapping


def _list_columns(params):
    url = URL + DB + Endpoint.category.value
    page = scrap.get_page(url, params, use_proxy=True)
    items = page.dom.body.select(".page-content form table")
    breakpoint()
    pass
