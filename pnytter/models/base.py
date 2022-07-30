import re

import pydantic


NEString = pydantic.Field(..., min_length=1)
PosInt = pydantic.Field(..., ge=0)


class BasePnytterModel(pydantic.BaseModel):
    class Config:
        anystr_strip_whitespace = True


class BasePnytterStats(BasePnytterModel):

    @pydantic.validator("*", pre=True, allow_reuse=True)
    def _clear_numeric_string(cls, v):
        """Clear all non-numeric characters from all the attributes, if given as string."""
        if isinstance(v, str):
            v = re.sub("[^0-9]", "", v)
        return v
