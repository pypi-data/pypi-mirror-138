from abc import ABC, abstractmethod
import re
from typing import Optional

from md_citeproc.utils import Utilities
from md_citeproc.structures import RePatterns, SingleReference, KeyReference, PlainReference, CiteprocWarning


class Citation(ABC):
    """
    Base class for citation entries, implementation details dependent of type
    One entry can contain multiple citekeys/single references
    """

    def __init__(self, line: str, line_no: int, match: re.Match, keyset: set, warnings: list, strict: bool, config_incomplete: bool):
        self.keyset = keyset
        self.line: str = line
        self.line_no: int = line_no
        self.match: re.Match = match
        self.content = self._get_content()
        self.references: list[SingleReference] = []
        self._rendered: Optional[str] = None
        self.warnings = warnings
        self.strict = strict
        self.enumeration: Optional[int] = None
        self.config_incomplete = config_incomplete
        self._split_references()

    @abstractmethod
    def _get_content(self) -> str:
        """
        Isolate pure content of citation, strip-off all markers and markup
        :return: str, content of the citation
        """
        pass

    def _split_references(self):
        """
        Split full text content of a citation in separate parts containing only one citekey
        According to standard these parts are split by ';'
        If citekey is not found in keyset, save reference as plain text and issue warning
        :return: list of all contained references, citekeys singled out
        """
        keymatch = re.search(RePatterns.CONTAINED_KEY, self.content)
        if (keymatch is None) or self.config_incomplete:
            # No citekey found at all - return full content as plain text
            self._append_reference(PlainReference(content=self.content))
            return
        current_pre = self.content[:keymatch.start()]
        remaining = self.content[keymatch.end():]
        while True:
            trimmed_key = Utilities.citekey_trim(keymatch.group())
            next_match = re.search(RePatterns.CONTAINED_KEY, remaining)
            if next_match is None:
                # No more citekeys left, append last reference and return
                self._append_reference(KeyReference(citekey=trimmed_key, prefix=current_pre, suffix=remaining))
                return
            # More citekeys to come; split off prefix and suffix
            inbetween = remaining[:next_match.start()]
            inbetween_split = inbetween.split(RePatterns.SEPARATOR)
            current_post = inbetween_split[0]
            # Check if split encountered a separator string - used to rebuild on validation failure
            sep_present = (len(inbetween_split) > 1)
            # Splitting done, append reference and restart loop
            self._append_reference(
                KeyReference(citekey=trimmed_key, prefix=current_pre, suffix=current_post, sep_present=sep_present)
            )
            keymatch = next_match
            current_pre = RePatterns.SEPARATOR.join(inbetween_split[1:])
            remaining = remaining[keymatch.end():]

    def _append_reference(self, ref: SingleReference):
        """
        Append singled-out references to self.references and merge if possible
        Result is always a single PlainReference or a list of KeyReference
        :param ref: SingleReference from _split_references
        :return: None
        """
        if isinstance(ref, KeyReference):
            if not ref.validate_key(self.keyset):
                warn = CiteprocWarning.from_citekey(ref.citekey)
                if self.strict:
                    warn.raise_()
                self.warnings.append(warn)
                ref = PlainReference.from_invalid(ref)
        if len(self.references) == 0 or (self.references[-1].has_key and ref.has_key):
            self.references.append(ref)
        elif (not self.references[-1].has_key) and ref.has_key:
            ref.left_merge(self.references.pop())
            self.references.append(ref)
        else:
            self.references[-1].right_merge(ref)

    @property
    def n_citekeys(self) -> int:
        """
        Count number of valid citekeys in citation
        :return: int, number of citekeys
        """
        return len([i.citekey for i in self.references if i.has_key])

    def serialize_keys(self) -> Optional[list[dict[str, str]]]:
        """
        ct. https://github.com/Juris-M/citeproc-js/blob/master/attic/citeproc-doc.rst
        Convert citation to a list of one dictionary for each key reference
        suitable for json-dumping to pass to citeproc-cli
        :return: list containing one dictionary for each key reference or None
        """
        if self.n_citekeys == 0:
            return None
        refs = []
        for i in self.references:
            if isinstance(i, KeyReference):
                elem = {"id": i.citekey}
                if i.prefix != "":
                    elem.update({"prefix": i.prefix})
                if i.suffix != "":
                    elem.update({"suffix": i.suffix})
                refs.append(elem)
        return refs

    @property
    def rendered(self) -> str:
        if self._rendered is None:
            return self.content
        return self._rendered

    @rendered.setter
    def rendered(self, s: str):
        self._rendered = s
