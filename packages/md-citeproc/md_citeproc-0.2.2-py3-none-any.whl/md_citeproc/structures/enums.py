from enum import Enum


class NotationStyle(Enum):
    """The method of notation of citations in the input text"""
    INLINE = "inline"
    FOOTNOTE = "footnote"
    INLINE_FOOTNOTE = "inline_footnote"


class OutputStyle(Enum):
    """The method of rendering citations in the output"""
    INLINE = "inline"
    NUM_FOOTNOTES = "num_footnotes"


class CiteprocConfigDefaults(Enum):
    """Default configuration options for the extension"""
    BUILTIN = "builtin"
    AVAILABLE = "available"
