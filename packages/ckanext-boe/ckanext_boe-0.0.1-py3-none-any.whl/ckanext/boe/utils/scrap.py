from __future__ import annotations

import mimetypes
import logging
import tempfile
from typing import Any, Iterable, Optional
import enum
import uuid
import requests
from pathlib import Path

from pathlib import Path
from urllib.parse import urlparse, parse_qs, urlencode, parse_qsl

from markdownify import markdownify
from bs4 import BeautifulSoup


log = logging.getLogger(__name__)

tmp_root = Path(tempfile.gettempdir())
cache = tmp_root / "ckanext-pages"

proxies = dict(http='socks5://127.0.0.1:2001', https='socks5://127.0.0.1:2001')

if not cache.exists():
    log.debug("Create cache folder at %s", cache)
    cache.mkdir()

URL = urlparse("https://www.bankofengland.co.uk")


def download_into(url: str, dest: Path, params: dict[str, str], use_proxy: bool = False):
    resp = requests.get(url, stream=True, proxies=proxies if use_proxy else {}, params=params, headers={"user-agent": "python"})

    resp.raise_for_status()
    with dest.open("wb") as fp:
        for chunk in resp.iter_content(1024):
            fp.write(chunk)


def dig(root: str):
    parsed = urlparse(root)
    path = parsed.path
    params = parse_qsl(parsed.query)
    url = URL._replace(path=path).geturl()
    page = get_page(url, dict(params))

    if page.visited:
        return
    page.visit()
    yield page

    if page.type.is_(PageType.section):
        for link in page.sub_links():
            yield from dig(link)


def get_page(url: str, params: dict[str, str], use_proxy: bool = False):
    key = str([url, list(sorted(params.items()))])
    key = str(uuid.uuid3(uuid.NAMESPACE_URL, key))

    source = cache / key

    old = Page.lookup(source)
    if old:
        log.debug("Re-visiting %s", url)
        return old

    if not source.exists():
        log.debug("Create cache %s for %s", key, url)
        download_into(url, source, params, use_proxy)
    else:
        log.debug("Load cache %s for %s", key, url)

    return Page(source, url)


class PageType(enum.Flag):
    page = enum.auto()
    section = enum.auto()
    package = enum.auto()
    resource = enum.auto()

    def is_(self, type: PageType):
        return self & type


class Page:
    __cache = {}
    visited = False

    @classmethod
    def lookup(cls, source: Path):
        if source in cls.__cache:
            return cls.__cache[source]

    def __init__(self, source: Path, url: str):
        self.url = url
        with source.open("rb") as fp:
            self.dom = BeautifulSoup(fp)

        self.__cache[source] = self

    def visit(self):
        self.visited = True

    @property
    def type(self) -> PageType:
        type = PageType.page
        if self.has_sub_links():
            type |= PageType.section
        if self.has_package_data():
            type |= PageType.package
        return type

    def has_sub_links(self):
        return len(self.dom.select(".sub-links .sub-links-link")) > 0

    def sub_links(self) -> dict[str, str]:
        return {
            str(link["href"]): link.text
            for link in self.dom.select(".sub-links .sub-links-link")
        }

    def has_package_data(self) -> bool:
        # TODO: implement
        return bool(self.package_data())

    def package_data(self) -> Iterable[dict[str, Any]]:
        content = self.dom.select(".page-section .content-block")
        for block in content:
            data = self._block_to_dataset(block)
            if data:
                yield data

    def _block_to_dataset(self, block) -> Optional[dict[str, Any]]:
        import ckan.lib.munge as munge

        h2 = block.h2
        if not h2:
            return
        resources = self._resources_from_block(block)

        for media_block in self.dom.select(".page-section .content-block"):
            if block == media_block:
                continue
            resources.extend(self._media_resources_from_block(media_block))

        data = {
            "title": self.dom.body.h1.text + " - " + h2.text,
            "notes": markdownify("".join(map(str, block.select("h2 ~ p")))),
            "url": self.url,
            "resources": resources,
        }

        data["name"] = munge.munge_title_to_name(data["title"])
        return data

    def _media_resources_from_block(self, block):
        links = [a for a in block.select('a[href*="/media/"]')]
        resources = []
        for link in links:
            resource = self._link_into_resource(link)
            resource["description"] = markdownify(str(block))
            resources.append(resource)

        return resources


    def _resources_from_block(self, block):
        links = [a for a in block.select(f'a[href^="{URL.geturl()}"]')]

        resources = []
        for link in links:
            resource = self._link_into_resource(link)
            resources.append(resource)
            url = urlparse(resource["url"])
            if url.path.startswith("/boeapps/database"):
                qs = parse_qs(url.query)

                if "html.x" in qs:
                    qs["csv.x"] = qs.pop("html.x")
                qs["CSVF"] = ["CN"]

                resources.append(
                    {
                        "name": resource["name"],
                        "url": url._replace(
                            scheme=URL.scheme,
                            netloc=URL.netloc,
                            path=url.path.replace("/database/", "/iadb/"),
                            query=urlencode(qs, True),
                        ).geturl(),
                        "format": "CSV",
                    }
                )
        return resources


    def _link_into_resource(self, link):
            import ckan.plugins.toolkit as tk
            href = link["href"]
            assert isinstance(href, str)
            url = urlparse(href)
            mime, _enc = mimetypes.guess_type(url.path)
            if mime:
                fmt = tk.h.unified_resource_format(mime)
            else:
                if url.path.endswith(".asp"):
                    fmt = "URL"
                else:
                    fmt = tk.h.unified_resource_format("application/octet-stream")

            return {
                "name": link.text,
                "url": url._replace(scheme=URL.scheme, netloc=URL.netloc).geturl(),
                "format": fmt,
            }
