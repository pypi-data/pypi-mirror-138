from typing import Optional

from md_citeproc.exceptions import CiteprocStrictException


class CiteprocWarning:
    """Warnings for missing citekeys and markers without footnotes"""

    def __init__(self, content: str, citekey: Optional[str] = None, marker: Optional[str] = None):
        self.content: str = content
        self.citekey = citekey
        self.marker = marker

    @classmethod
    def from_citekey(cls, key: str):
        """Warning for missing citekey"""
        return cls("Missing citekey: {}".format(key), citekey=key)

    @classmethod
    def from_marker(cls, mark: str):
        """Warning for citekey marker without corresponding footnote"""
        return cls("Marker with no corresponding footnote: {}".format(mark), marker=mark)

    def __str__(self) -> str:
        return "WARNING: {}".format(self.content)

    def raise_(self):
        """Strict mode: Raise warning as exception"""
        raise CiteprocStrictException(self.content)
