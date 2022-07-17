from typing import List

import pydantic
import pytest

from pnytter import Pnytter


class PnytterTestsSettings(pydantic.BaseSettings):
    nitter_instances: List[pydantic.AnyUrl]

    class Config:
        env_prefix = "TEST_"
        env_file = "test.env"


@pytest.fixture
def pnytter():
    settings = PnytterTestsSettings()
    return Pnytter(
        nitter_instances=settings.nitter_instances,
    )
