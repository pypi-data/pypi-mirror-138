import re

from md_citeproc.structures import RePatterns, InlineCitation
from md_citeproc.processors import CiteprocPreproc


class InlineFootnotePreproc(CiteprocPreproc):
    """
    Preprocessor specific to inline-footnotes notation
    Inline footnotes have the form [^@citekey]
    They differ from Inline Citations in the preceding '^' char
    making them more explicit and allowing for citations without a citekey
    """

    def _find_tokens(self, lines):
        for n_line, line in enumerate(lines, start=0):
            self._check_code_block(line)
            if not self.in_code_block:
                self._check_collection_tokens(n_line, line)
                matches = re.finditer(RePatterns.INLINE_FOOTNOTE, line)
                while True:
                    m = next(matches, None)
                    if m is None:
                        break
                    if self._check_inline_code(m, line):
                        continue
                    self._append_citation(InlineCitation(
                        line=line,
                        line_no=n_line,
                        match=m,
                        notation=self.config["notation"],
                        keyset=self.keyset,
                        warnings=self.warnings,
                        strict=self.config["strict"],
                        config_incomplete=self._check_config_invalid()
                    ))
