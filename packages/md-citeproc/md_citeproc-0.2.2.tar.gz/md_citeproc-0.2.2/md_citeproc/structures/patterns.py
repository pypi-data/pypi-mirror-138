import re
from dataclasses import dataclass


@dataclass(frozen=True)
class RePatterns:
    """Regex patterns to match citekeys, citations and footnotes in various forms"""
    CITEKEY: re.Pattern = re.compile(r"(?<=[\[;\^ ])@[A-Za-z0-9]+")  # Citekey starting with '@' and consisting of alpha-numerical characters; to exclude e-mail addresses, must be preceded with a '[' or ' '
    CONTAINED_KEY: re.Pattern = re.compile(r"(^|(?<=[\[;\^ ]))@[A-Za-z0-9]+")
    INLINE_CONTAINER: re.Pattern = re.compile(r"(?<!^)\[.*?\]")  # Container for inline citations: everything between square brackets that is not at the start of a line - unspecific and needs suffix processing
    INLINE_FOOTNOTE: re.Pattern = re.compile(r"(?<!^)\[\^.*?\]")
    FOOTNOTE_ANCHOR: re.Pattern = re.compile(r"(?<!^)\[\^[A-Za-z0-9]+\]")  # Anchor in text for footnote syntax - [^something] - must not be at the start of a line
    FOOTNOTE: re.Pattern = re.compile(r"^\[\^[A-Za-z0-9]+\]")  # Reference for footnote - same syntax but must be at the start of a line
    CODEBLOCK: re.Pattern = re.compile(r"^`{3}")
    SEPARATOR: str = ";"  # One container can contain multiple citations - separator string
