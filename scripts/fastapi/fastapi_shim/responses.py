"""Lightweight response classes used by tests."""


class HTMLResponse(str):
    pass


class JSONResponse(dict):
    def __init__(self, content, status_code: int = 200):
        super().__init__(content)
        self.status_code = status_code
