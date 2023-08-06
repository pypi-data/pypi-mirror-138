import re
from jinja2 import Template

from md_citeproc.utils import Utilities
from md_citeproc.exceptions import CiteprocException
from md_citeproc.structures import RePatterns, FootnoteCitation, FootnoteUse, CiteprocWarning
from md_citeproc.processors import CiteprocPreproc


class FootnotePreproc(CiteprocPreproc):
    """Preprocessor for explicit footnote notation"""

    def __init__(self, config: dict):
        super().__init__(config)
        self.marker_dict: dict[str, FootnoteCitation] = {}

    def _find_footnotes(self, lines):
        """Find the actual footnotes containing the content of a citation"""
        for n_line, line in enumerate(lines, start=0):
            self._check_code_block(line)
            if not self.in_code_block:
                self._check_collection_tokens(n_line, line)
                match = re.search(RePatterns.FOOTNOTE, line)
                if match is not None:
                    c = FootnoteCitation(
                        line=line,
                        line_no=n_line,
                        match=match,
                        keyset=self.keyset,
                        warnings=self.warnings,
                        strict=self.config["strict"],
                        config_incomplete=self._check_config_invalid()
                    )
                    if self.marker_dict.get(c.marker, None) is not None:
                        # Footnote marker already present; this is a problem
                        raise CiteprocException("Footnote with marker {} found multiple times".format(c.marker))
                    # self.citations.append(c)
                    self._append_citation(c)
                    self.marker_dict[c.marker] = c

    def _find_anchors(self, lines):
        """
        Find the anchors where the footnotes are used in the text
        Ignore the anchor and emit a warning if anchor has no matching footnote
        """
        for n_line, line in enumerate(lines, start=0):
            self._check_code_block(line)
            if not self.in_code_block:
                matches = re.finditer(RePatterns.FOOTNOTE_ANCHOR, line)
                while True:
                    m = next(matches, None)
                    if m is None:
                        break
                    if self._check_inline_code(m, line):
                        continue
                    marker = FootnoteCitation.extract_marker(m)
                    c = self.marker_dict.get(marker, None)
                    if c is None:
                        # No footnote is matching the anchor, disregard!
                        warn = CiteprocWarning.from_marker(marker)
                        if self.config["strict"]:
                            raise warn.raise_()
                        self.warnings.append(warn)
                        continue
                    c.uses.append(FootnoteUse(line_no=n_line, match=m, referes=c))

    def _find_tokens(self, lines):
        self._find_footnotes(lines)
        self.in_code_block = False
        self._find_anchors(lines)

    def _get_ordered_uses(self) -> list[FootnoteUse]:
        """Get reverse-ordered list of all citation uses"""
        uses = []
        for i in self.citations:
            uses.extend(i.uses)
        uses.sort(key=lambda x: (x.line_no, x.match.start()), reverse=True)
        return uses

    def _replace_rendered(self, lines: list[str]) -> list[str]:
        uses = self._get_ordered_uses()
        for i in uses:
            tmpl: Template = self.config["num_template"]
            replacement = Utilities.merge_lines(tmpl.render(n=i.referes.enumeration))
            lines[i.line_no] = lines[i.line_no][:i.match.start()] + replacement + lines[i.line_no][i.match.end():]
        while True:
            try:
                i = self.citations.pop()
            except IndexError:
                break
            fntmpl: Template = self.config["footnote_template"]
            fn = Utilities.merge_lines(fntmpl.render(n=i.enumeration, content=i.rendered))
            lines[i.line_no] = fn
        return lines
