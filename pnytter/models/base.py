import pydantic


NEString = pydantic.Field(..., min_length=1)
PosInt = pydantic.Field(..., ge=0)


class BasePnytterModel(pydantic.BaseModel):
    class Config:
        anystr_strip_whitespace = True
