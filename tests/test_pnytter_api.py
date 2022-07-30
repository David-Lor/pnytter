import pytest

from pnytter.exceptions import NoNitterInstancesDefinedError


def test_pnytter_no_instances(pnytter):
    pnytter.nitter_instances = []
    with pytest.raises(NoNitterInstancesDefinedError):
        pnytter.find_user("jack")
