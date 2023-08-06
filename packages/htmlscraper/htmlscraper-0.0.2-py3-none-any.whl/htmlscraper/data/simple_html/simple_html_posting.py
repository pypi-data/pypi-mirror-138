from abc import ABC

from bs4 import BeautifulSoup
from requests import Session

from ..abstraction.abstract_posting import AbstractPosting, PostingVisitor
from ..user.author import Author


class SimpleHTMLPosting(AbstractPosting, ABC):
    def __init__(self, session: Session, url: str, post_id: int, title: str, author: Author,
                 html: BeautifulSoup) -> None:
        super().__init__(session, url, post_id, title, author, html)

    def accept(self, visitor: PostingVisitor) -> None:
        visitor.visit_author_name(self._html_content)
        visitor.visit_content(self._html_content)
        visitor.visit_file(self._html_content)
        visitor.visit_comment(self._html_content)
