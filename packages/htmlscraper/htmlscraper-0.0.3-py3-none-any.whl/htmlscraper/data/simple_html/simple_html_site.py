from abstraction.abstract_page import AbstractPage
from abstraction.abstract_site import AbstractSite
from requests import Session

from simple_html_page import SimpleHTMLPage


class SimpleHTMLSite(AbstractSite):
    def __init__(self, session: Session, url: str) -> None:
        """
        A simple html site.
        """
        super().__init__()

        self.session = session
        self.url = url

    def get_page(self, sub_url: str) -> AbstractPage:
        return SimpleHTMLPage(self.session, self.url + sub_url)
