import re

from md_citeproc.structures import RePatterns, InlineCitation
from md_citeproc.processors import CiteprocPreproc


class InlinePreproc(CiteprocPreproc):
    """
    Preprocessor specific to inline notation
    Inline footnotes have the form [@citekey]
    Since markup is not very specific, matches without a citekey are ignored
    """

    def _find_tokens(self, lines):
        for n_line, line in enumerate(lines, start=0):
            self._check_code_block(line)
            if not self.in_code_block:
                self._check_collection_tokens(n_line, line)
                matches = re.finditer(RePatterns.INLINE_CONTAINER, line)
                while True:
                    m = next(matches, None)
                    if m is None:
                        break
                    if self._check_inline_code(m, line):
                        continue
                    # Are there any citekeys in the container match?
                    keys = re.findall(RePatterns.CITEKEY, m.group())
                    if len(keys) > 0:
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
