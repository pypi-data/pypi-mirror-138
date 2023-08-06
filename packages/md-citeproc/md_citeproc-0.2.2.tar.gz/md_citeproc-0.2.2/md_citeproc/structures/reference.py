from abc import ABC, abstractmethod
from typing import Optional

from md_citeproc.structures import RePatterns


class SingleReference(ABC):
    """
    Base class containing either a plain text citation
    or a validated-as-present reference containing a single citekey
    """

    @property
    @abstractmethod
    def has_key(self) -> bool:
        """Check if a valid citekey is present in the reference"""
        pass

    @property
    @abstractmethod
    def content(self) -> str:
        """Get plain text of the reference; stripped of markup, nothing rendered"""
        pass

    @property
    @abstractmethod
    def citekey(self) -> Optional[str]:
        """return citekey, None if none is present"""
        pass

    @abstractmethod
    def validate_key(self, keyset: set) -> Optional[bool]:
        """Validate the citekey as present in keyset"""
        pass

    @abstractmethod
    def right_merge(self, ref: "SingleReference"):
        """Merge a plain text reference into the end of content or suffix"""
        pass


class KeyReference(SingleReference):
    """Single reference containing one single validated citekey with a pre- and a suffix"""

    def __init__(self, citekey: str, prefix: str = "", suffix: str = "", sep_present: bool = False):
        self.citekey = citekey
        self.prefix = prefix
        self.suffix = suffix
        self.sep_present = sep_present

    @property
    def has_key(self) -> bool:
        return True

    @property
    def content(self) -> str:
        c = self.prefix + "@" + self.citekey + self.suffix
        if self.sep_present:
            c += RePatterns.SEPARATOR
        return c

    @property
    def citekey(self) -> str:
        return self._citekey

    @citekey.setter
    def citekey(self, key: str):
        self._citekey = self._trim_citekey(key)

    @staticmethod
    def _trim_citekey(citekey: Optional[str]) -> Optional[str]:
        """Remove all markup (incl. preceding '@') and white space from a citekey"""
        if citekey is None:
            return None
        while not citekey[0].isalnum():
            citekey = citekey[1:]
        return citekey.strip()

    def validate_key(self, keyset: set) -> Optional[bool]:
        return self.citekey in keyset

    def left_merge(self, ref: SingleReference):
        """Merge a plain text reference into the start of the prefix"""
        self.prefix = ref.content + self.prefix

    def right_merge(self, ref: SingleReference):
        self.suffix += ref.content


class PlainReference(SingleReference):
    """Single reference containing no valid citekey, just some plain text"""

    def __init__(self, content: str):
        self.content = content

    @classmethod
    def from_invalid(cls, ref: KeyReference):
        """Create a plain text reference from an invalid key reference"""
        return cls(content=ref.content)

    @property
    def has_key(self) -> bool:
        return False

    @property
    def content(self) -> str:
        return self._content

    @content.setter
    def content(self, c: str):
        self._content = c

    @property
    def citekey(self):
        return None

    def validate_key(self, keyset: set) -> Optional[bool]:
        return None

    def right_merge(self, ref: SingleReference):
        self.content += ref.content
