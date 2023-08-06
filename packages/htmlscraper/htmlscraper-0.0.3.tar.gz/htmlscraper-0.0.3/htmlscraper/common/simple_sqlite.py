import sqlite3
from typing import Generator, List, Tuple

from ..common.trimmers import get_trimmer
from ..data.abstraction.abstract_posting import AbstractPosting
from ..data.content.comment import Comment
from ..data.content.content import Content
from ..data.user.author import Author
from ..preprocessing.text_trimming import TrimmingStrategy

NAME_TABLE_AUTHOR = "author"
NAME_TABLE_PAGE = "page"
NAME_TABLE_POSTING = "posting"
NAME_TABLE_CONTENT = "content"
NAME_TABLE_COMMENT = "comment"

NAME_COLUMN_STR_ID = "str_id"
NAME_COLUMN_URL = "url"
NAME_COLUMN_POST_ID = "post_id"

QUERY_CREATE_TABLE_AUTHOR = '''
CREATE TABLE IF NOT EXISTS {} (
    id integer primary key autoincrement,
    {} text not null unique on conflict ignore
);
'''.format(NAME_TABLE_AUTHOR, NAME_COLUMN_STR_ID)
QUERY_CREATE_TABLE_PAGE = '''
CREATE TABLE IF NOT EXISTS {} (
    id integer primary key autoincrement,
    {} text not null unique on conflict ignore
);
'''.format(NAME_TABLE_PAGE, NAME_COLUMN_URL)
QUERY_CREATE_TABLE_POSTING = '''
CREATE TABLE IF NOT EXISTS {} (
    id integer primary key autoincrement,
    page_id integer not null,
    author_id integer not null,
    {} text not null,
    post_id integer not null unique on conflict ignore,
    title text not null,
    
    foreign key (page_id) references {} (id),
    foreign key (author_id) references {} (id)
);
'''.format(NAME_TABLE_POSTING, NAME_COLUMN_URL, NAME_TABLE_PAGE, NAME_TABLE_AUTHOR)
QUERY_CREATE_TABLE_CONTENT = '''
CREATE TABLE IF NOT EXISTS {} (
    id integer primary key autoincrement,
    posting_id integer not null unique,
    content text,
    
    foreign key (posting_id) references {} (id)
);
'''.format(NAME_TABLE_CONTENT, NAME_TABLE_POSTING)
QUERY_CREATE_TABLE_COMMENT = '''
CREATE TABLE IF NOT EXISTS {} (
    id integer primary key autoincrement,
    posting_id integer not null,
    author_id integer not null,
    unique_id integer not null unique,
    time text not null,
    content text,

    foreign key (posting_id) references {} (id),
    foreign key (author_id) references {} (id)
);
'''.format(NAME_TABLE_COMMENT, NAME_TABLE_POSTING, NAME_TABLE_AUTHOR)

QUERY_INSERT_COMMON = '''
INSERT OR IGNORE INTO {0} ({1}) VALUES (?)
 on conflict ({1}) do update set {1} = excluded.{1};
'''
QUERY_INSERT_AUTHOR = QUERY_INSERT_COMMON.format(NAME_TABLE_AUTHOR, 'str_id')
QUERY_INSERT_PAGE = QUERY_INSERT_COMMON.format(NAME_TABLE_PAGE, 'url')
QUERY_INSERT_POSTING = '''
INSERT OR ABORT INTO {0} (page_id, author_id, url, {1}, title) VALUES(
    (SELECT id FROM {2} WHERE {3}=?),
    (SELECT id FROM {4} WHERE {5}=?),
    ?,
    ?,
    ?
) on conflict (post_id) do nothing
'''.format(NAME_TABLE_POSTING, NAME_COLUMN_POST_ID,
           NAME_TABLE_PAGE, NAME_COLUMN_URL,
           NAME_TABLE_AUTHOR, NAME_COLUMN_STR_ID)
QUERY_INSERT_CONTENT = '''
INSERT OR ABORT INTO {0} (posting_id, content) VALUES(
    (SELECT id FROM {1} WHERE {2}=?),
    ?
) on conflict (posting_id) do nothing
'''.format(NAME_TABLE_CONTENT,
           NAME_TABLE_POSTING, NAME_COLUMN_POST_ID)
QUERY_INSERT_COMMENT = '''
INSERT OR IGNORE INTO {0} (posting_id, author_id, unique_id, time, content) VALUES(
    (SELECT id FROM {1} WHERE {2}=?),
    (SELECT id FROM {3} WHERE {4}=?),
    ?,
    ?,
    ?
) on conflict (unique_id) do nothing
'''.format(NAME_TABLE_COMMENT,
           NAME_TABLE_POSTING, NAME_COLUMN_POST_ID,
           NAME_TABLE_AUTHOR, NAME_COLUMN_STR_ID)

QUERY_SELECT_SINGLE_COLUMN = '''
SELECT {} FROM {}
'''


def prepare_connection(file_path: str) -> sqlite3.Connection:
    try:
        conn = sqlite3.connect(file_path, check_same_thread=False)
        conn.isolation_level = None

        conn.execute(QUERY_CREATE_TABLE_AUTHOR)
        conn.execute(QUERY_CREATE_TABLE_PAGE)
        conn.execute(QUERY_CREATE_TABLE_POSTING)
        conn.execute(QUERY_CREATE_TABLE_CONTENT)
        conn.execute(QUERY_CREATE_TABLE_COMMENT)

        return conn
    except Exception as ex:
        print("prepare_connection:", ex)
        raise ex


def store_author(conn: sqlite3.Connection, author: Author) -> int:
    try:
        cursor = conn.execute(QUERY_INSERT_AUTHOR, (author.str_id(),))

        if cursor.lastrowid > 0:
            return cursor.lastrowid
        else:
            raise Exception("row id is 0. Probably a conflict.")
    except Exception as ex:
        print("store_author:", ex)
        raise ex


def store_page(conn: sqlite3.Connection, url: str) -> int:
    try:
        cursor = conn.execute(QUERY_INSERT_PAGE, (url,))

        if cursor.lastrowid:
            return cursor.lastrowid
        else:
            raise Exception("row id is 0. Probably a conflict.")
    except Exception as ex:
        print("store_page:", ex)
        raise ex


def store_posting(conn: sqlite3.Connection, page_url, posting: AbstractPosting) -> None:
    try:
        conn.execute(QUERY_INSERT_POSTING,
                     (page_url, posting.author().str_id(), posting.url(), posting.post_id(), posting.title()))
    except Exception as ex:
        print("store_posting:", ex)
        raise ex


def store_content(conn: sqlite3.Connection, posting: AbstractPosting, content: Content) -> None:
    try:
        conn.execute(QUERY_INSERT_CONTENT,
                     (posting.post_id(), content.content()))
    except Exception as ex:
        print("store_content:", ex)
        raise ex


def store_comment(conn: sqlite3.Connection,
                  posting: AbstractPosting,
                  *comments: Comment) -> None:
    try:
        for comment in comments:
            store_author(conn, comment.author())
            conn.execute(QUERY_INSERT_COMMENT, (posting.post_id(),
                                                comment.author().str_id(),
                                                comment.unique_id(),
                                                comment.time(),
                                                comment.content()))
    except Exception as ex:
        print("store_comment:", ex)
        raise ex


def dump_column(conn: sqlite3.Connection,
                trimmer: TrimmingStrategy,
                table_col_tups: List[Tuple[str, str]]) -> Generator[str, None, None]:
    for table, column in table_col_tups:
        for tup in conn.execute(QUERY_SELECT_SINGLE_COLUMN.format(column, table)):
            yield trimmer.trim(tup[0])


def generator_set(db_paths: List[str], trimmer: TrimmingStrategy = get_trimmer('mixed')):
    for db_path in db_paths:
        with prepare_connection(db_path) as conn:
            yield from dump_column(conn, trimmer, [('content', 'content'),
                                                   ('posting', 'title')])
