import re

from typing import List, Callable, Pattern, Tuple


class TrimmingStrategy:
    def __init__(self, strategies: List[Callable[[str], str]]):
        self._strategies = strategies

    def trim(self, val: str):
        replaced = val

        for strategy in self._strategies:
            replaced = strategy(replaced)
            assert replaced is not None, '{} did not return any value'.format(
                str(strategy))

        return replaced


class PythonStrip:
    def __call__(self, val: str):
        return val.strip()


class LowerCase:
    def __call__(self, val: str):
        return val.lower()


class SimpleReplace:
    def __init__(self, orig: str, to: str):
        self._orig = orig
        self._to = to

    def __call__(self, val: str):
        return val.replace(self._orig, self._to)


class NewlineToSpace(SimpleReplace):
    def __init__(self):
        super(NewlineToSpace, self).__init__('\n', ' ')


class RegexReplacement:
    def __init__(self, rules: List[Tuple[Pattern, str]], invert=False):
        self.rules = rules
        self.invert = invert

    def __call__(self, val: str):
        replaced = val
        for pattern, repl in self.rules:
            try:
                replaced = re.sub(pattern, repl, replaced)
            except re.error as err:
                print(pattern, repl)
                raise err
        return replaced
