from abc import ABC, abstractmethod
from typing import Union
from markdown.preprocessors import Preprocessor
from collections import deque
from jinja2 import Template
import re
import json

from md_citeproc.utils import Utilities
from md_citeproc.structures import \
    Citation, \
    FootnoteCitation, \
    InlineCitation, RePatterns, \
    OutputStyle, \
    CiteprocWarning
from md_citeproc.wrapper import CiteprocWrapper


class CiteprocPreproc(Preprocessor, ABC):
    """Preprocessor base class, implements methods common to all notation styles"""

    def __init__(self, config: dict):
        super().__init__()
        self.config: dict = config
        self.keyset: set = self._build_keyset()
        self.collections: dict[str, list[int]] = {"bibliography": [], "footnotes": []}
        self.in_code_block: bool = False
        self.citations: deque[Union[Citation, FootnoteCitation, InlineCitation]] = deque()
        self.warnings: list[CiteprocWarning] = []
        self.current_enumeration: int = 0
        self.serialized: list = []

    def _build_keyset(self) -> set:
        """Collect all citekeys for validation"""
        keyset = set()
        if not self._check_config_invalid():
            with self.config["csljson"].open() as f:
                jsondata = json.load(f)
            for i in jsondata:
                keyset.add(i["id"])
        return keyset

    @staticmethod
    def _count_backticks(partial_line: str) -> int:
        """Count backticks in a string to determine inline code tag presence"""
        ticks = re.finditer(r"`", partial_line)
        tick_counter = 0
        while True:
            m = next(ticks, None)
            if m is None:
                break
            if CiteprocPreproc._check_tick_valid(m, partial_line):
                tick_counter += 1
        return tick_counter

    @staticmethod
    def _check_tick_valid(match: re.Match, line) -> bool:
        """Check a backtick for escaping characters"""
        if CiteprocPreproc._count_escapes(match, line) % 2 == 0:
            return True
        return False

    @staticmethod
    def _count_escapes(match: re.Match, line, backslashes: int = 0) -> int:
        """Count escaping characters preceding a backtick"""
        pos = match.start() - (1 + backslashes)
        if line[pos] == "\\":
            backslashes += 1
            backslashes = CiteprocPreproc._count_escapes(match, line, backslashes)
        return backslashes

    @staticmethod
    def _check_inline_code(match: re.Match, line: str) -> bool:
        """Check if a match is wrapped in an inline code tag"""
        n_ticks = CiteprocPreproc._count_backticks(line[:match.start()])
        if n_ticks % 2 == 0:  # Not a inline code seq, not the correct number of openings
            return False
        n_ticks = CiteprocPreproc._count_backticks(line[match.end():])
        if n_ticks == 0:  # Not a inline code seq, no closer found
            return False
        return True

    def _check_code_block(self, line):
        """Check for block code marker to ignore ciations inside"""
        matches = re.findall(RePatterns.CODEBLOCK, line)
        if len(matches) > 0:
            self.in_code_block = not self.in_code_block

    def _check_collection_tokens(self, n_line: int, line: str):
        """Find tokens for data collections (bibliography and footnotes)"""
        if line == self.config["bibliography_token"]:
            self.collections["bibliography"].append(n_line)
        if (self.config["output"] == OutputStyle.NUM_FOOTNOTES) and (line == self.config["footnotes_token"]):
            self.collections["footnotes"].append(n_line)

    def _check_config_invalid(self) -> bool:
        """Check if a csljson and a csl file are in the config"""
        return (self.config["csljson"] is None) or (self.config["cslfile"] is None)

    @abstractmethod
    def _find_tokens(self, lines):
        """Find all citations and collection tokens, build citation stack"""
        pass

    def _append_citation(self, c: Citation):
        """Append citation to deque, increase enumeration"""
        self.current_enumeration += 1
        c.enumeration = self.current_enumeration
        self.citations.append(c)

    def _serialize_all_keys(self):
        """Get list of all citekeys with prefix and suffix to pass to citeproc-cli"""
        self.serialized = [i.serialize_keys() for i in self.citations if i.n_citekeys > 0]

    def _get_rendered(self):
        """Pass citekeys to citeproc, execute, merge results into citation list"""
        if not self._check_config_invalid():
            rendered_deque = CiteprocWrapper(self.config).get_rendered(self.serialized)
            # Merge-in all rendered citations
            for i in self.citations:
                if i.n_citekeys > 0:
                    i.rendered = rendered_deque.popleft()

    def _replace_footnotes(self, lines: list[str], fnstring: str) -> list[str]:
        """Replace footnote token with rendered footnotes"""
        for i in self.collections["footnotes"]:
            lines[i] = fnstring
        return lines

    @staticmethod
    def _assemble_bibliography(bibliography: dict) -> str:
        """Create a single string from citeproc-cli bibliography json output"""
        starter = bibliography[0].get("bibstart", "")
        finisher = bibliography[0].get("bibend", "")
        entries = "".join(bibliography[1])
        bibstring = "{}{}{}".format(starter, entries, finisher)
        return Utilities.merge_lines(bibstring)

    def _replace_bibliography(self, lines: list[str]) -> list[str]:
        """Replace bibliography token with rendered bibliography"""
        if not self._check_config_invalid():
            if len(self.collections["bibliography"]) > 0:
                bibliography = CiteprocWrapper(self.config).get_rendered(self.serialized, bibliography=True)
                bibstring = self._assemble_bibliography(bibliography)
                for i in self.collections["bibliography"]:
                    lines[i] = bibstring
        return lines

    def _replace_rendered(self, lines: list[str]) -> list[str]:
        """Replace all rendered citations"""
        fnstring: str = ""
        while True:
            try:
                i = self.citations.pop()
            except IndexError:
                break
            if self.config["output"] == OutputStyle.INLINE:
                tmpl: Template = self.config["inline_template"]
                replacement = Utilities.merge_lines(tmpl.render(content=i.rendered))
            else:
                tmpl: Template = self.config["num_template"]
                replacement = Utilities.merge_lines(tmpl.render(n=i.enumeration))
                fntmpl: Template = self.config["footnote_template"]
                fnstring = Utilities.merge_lines(fntmpl.render(n=i.enumeration, content=i.rendered)) + fnstring
            lines[i.line_no] = lines[i.line_no][:i.match.start()] + replacement + lines[i.line_no][i.match.end():]
        if self.config["output"] == OutputStyle.NUM_FOOTNOTES:
            lines = self._replace_footnotes(lines, fnstring)
        return lines

    def testable_render(self, lines: list[str]):
        self._find_tokens(lines)
        self._serialize_all_keys()
        self._get_rendered()

    def run(self, lines: list[str]) -> list[str]:
        # Retrieve all citations
        self._find_tokens(lines)
        # Pass to citeproc for rendering
        self._serialize_all_keys()
        self._get_rendered()
        # Replace bibliography placeholder if necessary
        lines = self._replace_bibliography(lines)
        # Replace all referenced citations
        lines = self._replace_rendered(lines)
        return lines
