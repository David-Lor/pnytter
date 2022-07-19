from bs4 import BeautifulSoup


class BaseNitterParser:
    def __init__(self, html: str):
        """
        :param html: Nitter HTML source to parse
        """
        self.soup = BeautifulSoup(html, "html")
