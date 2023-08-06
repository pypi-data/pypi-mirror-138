from abc import ABC


class wiki(ABC):
    def __init__(self) -> None:
        pass

    def _api_root(self, lang: str = "zh") -> str:
        return f"https://{lang}.wikipedia.org/w/api.php"

    def _query(self, url: str, para: str = "", options: str = "", lang: str = "zh") -> dict:
        import requests
        _query = f"?action=query&format=json&utf8=1{url}{para}{options}"
        _url = f"{self._api_root(lang = lang)}{_query}"
        _req = requests.get(_url)
        if _req.status_code == 200:
            _j = _req.json()
            return _j.get("query", {})
        return {}

    def _search_page(self, name: str, lang: str = "zh") -> list:
        _search = self._query(
            url="&list=search", para=f"&srsearch={name}", lang=lang).get("search", [])
        return _search

    def _get_name_by_pageid(self, pageid: int, selectlang: str = None, lang: str = "zh") -> list:
        _pages = self._query(url="&prop=langlinks",
                             para=f"&pageids={pageid}", lang=lang)
        _langs = _pages.get("pages", {}).get(
            str(pageid), {}).get("langlinks", [])
        _langs = {_l.get("lang"): _l.get("*") for _l in _langs}
        if selectlang is None:
            return _langs
        return _langs.get(selectlang, None)

    def search(self, name: str, year: str = "", fm_lang: str = "zh", lang: str = "en") -> dict:
        if year != "":
            _search = self._search_page(name=f"{name}+{year}", lang=fm_lang)
        else:
            _search = self._search_page(name=name, lang=fm_lang)
        for _s in _search:
            _pageid = _s.get("pageid", "")
            _name = self._get_name_by_pageid(
                pageid=_pageid, selectlang=lang, lang=fm_lang)
            return {"name": name, f"{lang}_name": _name, "pageid": _s.get("pageid")}
        return {}
