import pydantic


NEString = pydantic.Field(..., min_length=1)


class BasePnytterModel(pydantic.BaseModel):
    class Config:
        anystr_strip_whitespace = True
