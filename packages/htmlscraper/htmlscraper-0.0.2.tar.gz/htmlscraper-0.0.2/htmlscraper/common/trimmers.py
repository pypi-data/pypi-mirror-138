import re

from ..preprocessing.text_trimming import TrimmingStrategy, NewlineToSpace, SimpleReplace, RegexReplacement, PythonStrip, \
    LowerCase

DEFAULT_TRIMMER = TrimmingStrategy([
    NewlineToSpace(),
    SimpleReplace(' ', ''),
    RegexReplacement(
        [(re.compile(r'[^가-힣a-zA-Z0-9~!@#$%^&*()\-+=:;"\'<,>.?/\n\s]'), '')]),
    RegexReplacement([
        (re.compile(r'\?+'), '?'),
        (re.compile(r'!+'), '!'),
        (re.compile(r'http.*'), ''),
        (re.compile(r'[0-9]{3}-[0-9]{3}-[0-9]{4}'), ''),
        (re.compile(r'.*@.*'), ''),
        (re.compile(r'[0-9]+'), ''),

        (re.compile(r'\s+'), ' '),
    ]),
    PythonStrip(),
    LowerCase(),
])

INFERENCE_TRIMMER = TrimmingStrategy([
    RegexReplacement([
        (re.compile(r'\s+'), ' '),
    ]),
    PythonStrip(),
    LowerCase(),
])


def get_trimmer(lang='mixed'):
    repl = None
    if lang == 'mixed':
        repl = r'[^가-힣a-zA-Z0-9~!@#$%^&*()\-+=:;"\'<,>.?/\n\s]'
    elif lang == 'ko':
        repl = r'[^가-힣0-9~!@#$%^&*()\-+=:;"\'<,>.?/\n\s]'
    elif lang == 'en':
        repl = r'[^a-zA-Z0-9~!@#$%^&*()\-+=:;"\'<,>.?/\n\s]'
    else:
        assert True, lang

    return TrimmingStrategy([
        NewlineToSpace(),
        SimpleReplace(' ', ''),
        RegexReplacement([(re.compile(repl), '')]),
        RegexReplacement([
            (re.compile(r'\?+'), '?'),
            (re.compile(r'!+'), '!'),
            (re.compile(r'http.*'), ''),
            (re.compile(r'[0-9]{3}-[0-9]{3}-[0-9]{4}'), ''),
            (re.compile(r'.*@.*'), ''),
            (re.compile(r'[0-9]+'), ''),

            (re.compile(r'\s+'), ' '),
        ]),
        PythonStrip(),
        LowerCase(),
    ])
