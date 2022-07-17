import random
from typing import List, Optional

import pydantic
import requests

from .nitter_parser import NitterParser
from .models.profiles import TwitterProfile

__all__ = ("Pnytter",)


class Pnytter(pydantic.BaseModel):

    nitter_instances: List[pydantic.AnyUrl] = pydantic.Field(..., min_items=1)
    """List of the Nitter instances to use. Each instance must be given as the base URL of the Nitter server.
    At least one instance is required."""

    request_timeout: float = pydantic.Field(default=10, ge=0)
    """Timeout in seconds for HTTP requests."""

    def _get_random_nitter_instance(self) -> str:
        """Retrieve a random Nitter instance URL from the 'nitter_instances' list."""
        return random.choice(self.nitter_instances)

    def _raw_request(self, method: str, url: str) -> str:
        """Method for performing an HTTP request, and returning the response body as string.
        This method can be overriden by the code that uses Pnytter, if required."""
        r = requests.request(
            method=method,
            url=url,
            timeout=self.request_timeout,
        )
        r.raise_for_status()
        return r.text

    def _request_nitter(self, endpoint: str, method: str = "GET") -> str:
        """Perform an HTTP request to Nitter, for the given endpoint.
        This method chooses a random Nitter instance to use for the request."""
        nitter_instance = self._get_random_nitter_instance()
        url = f"{nitter_instance}/{endpoint}"  # TODO safe urljoin
        return self._raw_request(
            method=method,
            url=url,
        )

    def find_user(self, username: str) -> Optional[TwitterProfile]:
        html = self._request_nitter(
            endpoint=username
        )
        parser = NitterParser(html)
        return parser.get_profile()
