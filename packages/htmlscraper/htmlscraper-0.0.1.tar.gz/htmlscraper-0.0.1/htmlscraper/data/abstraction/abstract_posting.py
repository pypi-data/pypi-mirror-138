from abc import abstractmethod, ABCMeta

from bs4 import BeautifulSoup
from requests import Session

from ..user.author import Author


class PostingVisitor(metaclass=ABCMeta):

    def visit_content(self, soup: BeautifulSoup) -> None:
        return None

    def visit_comment(self, soup: BeautifulSoup) -> None:
        return None

    def visit_file(self, soup: BeautifulSoup) -> None:
        return None

    def visit_author_name(self, soup: BeautifulSoup) -> None:
        return None


class AbstractPosting:
    def __init__(self, session: Session, url: str, post_id: int, title: str, author: Author,
                 html_content: BeautifulSoup) -> None:
        self._session = session
        self._url = url
        self._post_id = post_id
        self._title = title
        self._author = author
        self._html_content = html_content

    def url(self) -> str:
        return self._url

    def post_id(self) -> int:
        return self._post_id

    def title(self) -> str:
        return self._title

    def author(self) -> Author:
        return self._author

    @abstractmethod
    def accept(self, visitor: PostingVisitor) -> None:
        pass

    def __repr__(self):
        return "Posting(id={}, title={}, author={})".format(self._post_id, self._title, self._author)
