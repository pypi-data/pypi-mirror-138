import re

from md_citeproc.structures import Citation, NotationStyle


class InlineCitation(Citation):
    """
    Citation class specific to inline notation
    Inline citations have the form [@citekey]
    One citation can contain multiple SingleReferences
    """

    def __init__(
        self, line: str, line_no: int, match: re.Match, notation: NotationStyle, keyset: set, warnings: list, strict: bool, config_incomplete: bool
    ):
        self.notation: NotationStyle = notation
        super().__init__(line, line_no, match, keyset, warnings, strict, config_incomplete)

    def _get_content(self) -> str:
        if self.notation == NotationStyle.INLINE:
            loffset = 1
        else:
            loffset = 2
        matchtext = self.match.group()
        return matchtext[loffset:-1]
