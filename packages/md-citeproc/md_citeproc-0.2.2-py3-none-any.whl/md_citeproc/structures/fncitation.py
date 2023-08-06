import re

from md_citeproc.structures import Citation


class FootnoteUse:
    """Anchor referencing a footnote in the text"""

    def __init__(self, line_no: int, match: re.Match, referes: "FootnoteCitation"):
        self.line_no: int = line_no
        self.match: re.Match = match
        self.referes: "FootnoteCitation" = referes


class FootnoteCitation(Citation):
    """
    Citation class specific to footnote notation
    A footnote citation can contain multiple citekeys and mutiple anchors,
    where the footnote is referenced in the text.
    """

    def __init__(self, line: str, line_no: int, match: re.Match, keyset: set, warnings: list, strict: bool, config_incomplete: bool):
        super().__init__(line, line_no, match, keyset, warnings, strict, config_incomplete)
        self.marker: str = FootnoteCitation.extract_marker(self.match)
        self.uses: list[FootnoteUse] = []

    def _get_content(self) -> str:
        stripped = self.line[self.match.end():]
        while stripped[0] in [' ', ':']:
            stripped = stripped[1:]
        return stripped

    @staticmethod
    def extract_marker(match: re.Match) -> str:
        """
        Extract alphanumeric string marker from a footnote, i.e. '1' in [^1]
        @:param match: regex match of a footnote
        @:returns str, marker of the footnote
        """
        marker = match.group()
        return marker[2:-1]
