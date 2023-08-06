from abc import ABC


class tmdb(ABC):
    _img_root = "https://image.tmdb.org/t/p/w500"
    _api_root = "https://api.themoviedb.org/3"

    def __init__(self, apikey: str) -> None:
        self._apikey = apikey
        pass

    def _api(self, url: str, para: str = "", options: str = "", page: int = 1) -> list:
        import requests
        _query = f"?api_key={self._apikey}&page={page}{options}{para}"
        _url = f"{self._api_root}{url}{_query}"
        _req = requests.get(_url)
        if _req.status_code == 200:
            _j = _req.json()
            return _j.get("results", [])
        return []

    def _updimg(self, img: str) -> str:
        if img is None:
            return None
        if img[:4] == "http":
            return img
        return f"{self._img_root}{img}"

    def movies(self, title: str) -> dict:
        return self.search(query=title, type="movie")

    def tv(self, title: str) -> dict:
        return self.search(query=title, type="tv")

    def people(self, name: str) -> dict:
        return self.search(query=name, type="person")

    def search(self, query: str, type: str = "movie") -> dict:
        _cmd = f"/search/{type}"
        _para = f"&query={query}"
        _options = "&language=zh-TW&include_adult=true"
        try:
            _rtn = self._api(url=_cmd, para=_para, options=_options)[0]
        except:
            return {}
        for _img in ["poster_path", "backdrop_path", "profile_path"]:
            _rtn.update({_img: self._updimg(_rtn.get(_img))})
        return _rtn
