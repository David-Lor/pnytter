from typing import Optional

from bs4 import BeautifulSoup


class BaseNitterParser:
    def __init__(self, parser: str, html: str):
        """
        :param parser: BeautifulSoup parser to use
        :param html: Nitter HTML source to parse
        """
        self.soup = BeautifulSoup(html, parser)

    def _get_error(self) -> Optional[str]:
        div = self.soup.find("div", class_="error-panel")
        if div:
            return div.text
