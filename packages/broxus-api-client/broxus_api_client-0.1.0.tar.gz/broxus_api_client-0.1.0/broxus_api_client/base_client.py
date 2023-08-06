import logging
import typing
from typing import Type

import httpx
import pydantic
import ujson

from .errors import HttpClientError

ResponseModel = typing.TypeVar('ResponseModel')


class BaseClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.logger = logging.getLogger(__name__)

    async def make_request(
            self,
            method: str,
            path: str,
            *,
            body: typing.Union[dict, pydantic.BaseModel] = None,
            response_model: Type[ResponseModel] = None,
            **kwargs
    ) -> ResponseModel:
        self.logger.debug(f'{method.upper()} {path}')

        if body is None:
            request_content = kwargs.pop("content", None)
        else:
            request_content = (
                body.json(exclude_unset=True)
                if isinstance(body, pydantic.BaseModel)
                else ujson.dumps(body)
            )

        async with httpx.AsyncClient(base_url=self.base_url) as client:
            try:
                response = await client.request(method, path, content=request_content, **kwargs)
            except Exception as e:
                self.logger.error(f'Unable to make {method.upper()} request to {path}: {e}', exc_info=True)
                raise HttpClientError(0, f"{e.__class__.__name__}: {e}")

        try:
            response_json = response.json()
        except Exception as e:
            raise HttpClientError(response.status_code, str(e))

        if response.is_error:
            raise HttpClientError(response.status_code, response_json)

        # Raise error if request is not succeeded before trying to parse response
        response.raise_for_status()

        if bool(response_model):
            # noinspection PyTypeChecker
            return pydantic.parse_obj_as(response_model, response_json)

        return response_json

    async def get(self, path: str, *, response_model: Type[ResponseModel] = None, **kwargs) -> ResponseModel:
        return await self.make_request('GET', path, response_model=response_model, **kwargs)

    async def post(
            self,
            path: str,
            *,
            body: typing.Union[dict, pydantic.BaseModel],
            response_model: Type[ResponseModel] = None,
            **kwargs
    ) -> ResponseModel:
        return await self.make_request('POST', path, body=body, response_model=response_model, **kwargs)
