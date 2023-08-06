import pydantic
import ujson


class _BaseModel(pydantic.BaseModel):
    class Config:
        json_dumps = ujson.dumps
        json_loads = ujson.loads
        allow_population_by_field_name = True
