import random
from typing import List, Collection, Optional, Union

import pydantic
import requests
from urljoin import url_path_join

from .nitter_parser import NitterParser
from .models.profiles import TwitterProfile

__all__ = ("Pnytter",)


class Pnytter(pydantic.BaseModel):

    nitter_instances: Union[List[pydantic.AnyHttpUrl], pydantic.AnyHttpUrl] = pydantic.Field(..., min_items=1)
    """List of the Nitter instances to use. Each instance must be given as the base URL of the Nitter server.
    At least one instance is required."""

    request_timeout: float = pydantic.Field(default=10, ge=0)
    """Timeout in seconds for HTTP requests."""

    @pydantic.validator("nitter_instances")
    def _nitter_instances_single_to_list(cls, v):
        if not isinstance(v, list):
            v = [v]
        return v

    def _get_random_nitter_instance(self) -> str:
        """Retrieve a random Nitter instance URL from the 'nitter_instances' list."""
        return random.choice(self.nitter_instances)

    def _raw_request(self, method: str, url: str, ignore_statuscodes: Collection[int]) -> str:
        """Method for performing an HTTP request, and returning the response body as string.
        This method can be overriden by the code that uses Pnytter, if required."""
        r = requests.request(
            method=method,
            url=url,
            timeout=self.request_timeout,
        )
        if r.status_code not in ignore_statuscodes:
            r.raise_for_status()
        return r.text

    def _request_nitter(self, endpoint: str, method: str = "GET", ignore_statuscodes: Optional[Collection[int]] = None) -> str:
        """Perform an HTTP request to Nitter, for the given endpoint.
        This method chooses a random Nitter instance to use for the request."""
        nitter_instance = self._get_random_nitter_instance()
        url = url_path_join(nitter_instance, endpoint)
        return self._raw_request(
            method=method,
            url=url,
            ignore_statuscodes=ignore_statuscodes or (),
        )

    def find_user(self, username: str) -> Optional[TwitterProfile]:
        """Get the information of a Twitter user, given its public username. If the profile does not exist, return None.
        :param username: Twitter profile username (example: "@jack")
        """
        html = self._request_nitter(
            endpoint=username,
            ignore_statuscodes=[404],
        )
        return NitterParser(html).get_profile()
