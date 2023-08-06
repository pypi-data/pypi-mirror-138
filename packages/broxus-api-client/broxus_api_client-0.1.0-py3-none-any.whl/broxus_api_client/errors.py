from typing import Any

import pydantic


class HttpClientError(BaseException):
    def __init__(self, code: int, data: Any):
        self.code = code
        self.data = data

    @property
    def detail_str(self):
        if self.data is None:
            return "Unknown error"
        if isinstance(self.data, str):
            return self.data
        if isinstance(self.data, dict):
            return self.data.get('detail')
        if isinstance(self.data, pydantic.BaseModel):
            try:
                if isinstance(self.data.detail, pydantic.BaseModel):
                    return self.data.detail.json()
                if isinstance(self.data.detail, str):
                    return self.data.detail
            except AttributeError:
                return "Unknown error"

            return self.data.json()

    def __str__(self):
        return f"[Error {self.code}]: {self.detail_str}"
