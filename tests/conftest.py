from typing import List, Union

import pydantic
import pytest

from pnytter import Pnytter


class PnytterTestsSettings(pydantic.BaseSettings):
    nitter_instances: Union[List[pydantic.AnyHttpUrl], pydantic.AnyHttpUrl]
    beautifulsoup_parser: str = "lxml"

    class Config:
        env_prefix = "TEST_"
        env_file = "test.env"


@pytest.fixture
def pnytter():
    settings = PnytterTestsSettings()
    return Pnytter(
        nitter_instances=settings.nitter_instances,
        beautifulsoup_parser=settings.beautifulsoup_parser,
    )
