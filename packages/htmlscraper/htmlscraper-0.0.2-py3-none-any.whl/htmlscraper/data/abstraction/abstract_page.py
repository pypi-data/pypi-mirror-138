from abc import ABCMeta, abstractmethod
from typing import Generator

from requests import Session

from ..abstraction.abstract_posting import AbstractPosting


class AbstractPage(metaclass=ABCMeta):
    def __init__(self, url: str, session: Session) -> None:
        self._url = url
        self._session = session

    @abstractmethod
    def posting_generator(self) -> Generator[AbstractPosting, None, None]:
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
