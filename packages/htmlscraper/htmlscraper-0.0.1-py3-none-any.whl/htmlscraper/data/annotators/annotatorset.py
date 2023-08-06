import re
from abc import ABC
from typing import List, Optional, Set


class Annotator(ABC):
    def __init__(self, label: str):
        self._label = label

    def label(self) -> str:
        return self._label

    def __call__(self, text: str) -> Optional[List]:
        pass


class AnnotatorSet:
    def __init__(self, annotators: List[Annotator]):
        self._annotators = annotators

    def labels(self) -> Set[str]:
        labels = set()

        for annotator in self._annotators:
            labels.add(annotator.label())

        return labels

    def annotate(self, text: str) -> List[List]:
        '''

        :param text:
        :return: List of [start, end, label]
        '''
        annotations = []

        for annotator in self._annotators:
            info = annotator(text)
            if info is None:
                continue

            for each in info:
                assert len(each) == 3
                annotations.append(each)

        return annotations


class RegexAnnotator(Annotator):
    def __init__(self, pattern: re.Pattern, label: str):
        super().__init__(label)
        self._pattern = pattern

    def __call__(self, text: str) -> Optional[List]:
        labels = []
        for m in re.finditer(self._pattern, text):
            labels.append([m.start(), m.end(), self._label])
        return labels


class WordAnnotator(Annotator):
    def __init__(self, targets: List[str], label: str):
        super(WordAnnotator, self).__init__(label)
        self._targets = set()
        for target in targets:
            assert target is not None and len(target) > 1
            self._targets.add(target)

    def __call__(self, text: str) -> Optional[List]:
        labels = []
        for m in re.finditer(r'\S+', text):
            if m.group(0) not in self._targets:
                continue

            labels.append([m.start(), m.end(), self._label])
        return labels
