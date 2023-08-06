from abc import ABCMeta, abstractmethod
from typing import Generator

from requests import Session

from ..abstraction.abstract_posting import AbstractPosting


class AbstractPage(metaclass=ABCMeta):
    def __init__(self, url: str, session: Session) -> None:
        """
        Abstract class representing a page, which is a collection of postings.
        The definition of the posting may vary from site to site.
        :param url: url of the page
        :param session: requests.Session
        """

        self._url = url
        self._session = session

    @abstractmethod
    def posting_generator(self) -> Generator[AbstractPosting, None, None]:
        """
        Create a generator that yields postings in the page. The postings
        usually means the list of posts on the page, such as a thread or a board, but
        if the page is in different format, it may yield other things.
        """
        pass

    @abstractmethod
    def next_page(self) -> str:
        """
        Get next page url
        :return: url; None if no more pages
        """
        pass

    def url(self):
        return self._url
