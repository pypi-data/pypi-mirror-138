from typing import Union, Optional
from markdown.extensions import Extension
from pathlib import Path
import jinja2

from md_citeproc.exceptions import CiteprocConfigException
from md_citeproc.utils import Utilities
from md_citeproc.structures import NotationStyle, OutputStyle, CiteprocWarning, CiteprocConfigDefaults
from md_citeproc.processors import InlinePreproc, InlineFootnotePreproc, FootnotePreproc


class CiteprocExtension(Extension):
    """
    Python Markdown extension
    Render CSL citations in Markdown documents using bibliographic data in CSLJSON
    and citation styles in CSL
    """

    config = {
        "csljson": ["", "JSON file containing bibliographic data in CSLJSON"],
        "cslfile": ["", "XML file containing citation style in CSL"],
        "uncited": ["", "List of uncited items to include into bibliography"],
        "locale": ["en-US", "Locale to use for conversion"],
        "localedir": [CiteprocConfigDefaults, "Directory containing CSL locales to use"],
        "notation": [NotationStyle.INLINE, "Notation style of references in Markdown text"],
        "output": [OutputStyle.INLINE, "Rendering style in rendered HTML"],
        "num_template": [CiteprocConfigDefaults.BUILTIN, "Jinja template to render enumerated footnote anchors"],
        "footnote_template": [CiteprocConfigDefaults.BUILTIN, "Jinja template to render footnote entries"],
        "inline_template": [CiteprocConfigDefaults.BUILTIN, "Jinja template to render inline references"],
        "footnotes_token": ["[FOOTNOTES]", "String in Markdown text to replace with footnotes"],
        "bibliography_token": ["[BIBLIOGRAPHY]", "String in Markdown text to replace with bibliography"],
        "citeproc_executable": [CiteprocConfigDefaults.AVAILABLE, "citeproc-cli executable/installation to use"],
        "strict": [False, "If true, throw errors instead of collecting warnings"]
    }

    def __init__(
        self,
        csljson: Optional[Union[Path, str]] = None,
        cslfile: Optional[Union[Path, str]] = None,
        uncited: Optional[list[str]] = None,
        locale: str = "en-US",
        localedir: Union[CiteprocConfigDefaults, Path, str] = CiteprocConfigDefaults.BUILTIN,
        notation: Union[NotationStyle, str] = NotationStyle.INLINE,
        output: Union[OutputStyle, str] = OutputStyle.NUM_FOOTNOTES,
        num_template: Union[CiteprocConfigDefaults, jinja2.Template, Path, str] = CiteprocConfigDefaults.BUILTIN,
        footnote_template: Union[CiteprocConfigDefaults, jinja2.Template, Path, str] = CiteprocConfigDefaults.BUILTIN,
        inline_template: Union[CiteprocConfigDefaults, jinja2.Template, Path, str] = CiteprocConfigDefaults.BUILTIN,
        footnotes_token: str = "[FOOTNOTES]",
        bibliography_token: str = "[BIBLIOGRAPHY]",
        citeproc_executable: Union[CiteprocConfigDefaults, Path, str] = CiteprocConfigDefaults.AVAILABLE,
        strict: bool = False
    ):
        super().__init__()

        # Set config

        # Essential data files
        self.setConfig("csljson", CiteprocExtension._string2path(csljson))
        cslfile_config = CiteprocExtension._string2path(cslfile)
        self.setConfig("cslfile", cslfile_config)

        # Set uncited items
        self.setConfig("uncited", CiteprocExtension._none_to_empty_list(uncited))

        # Set simply typed parameters
        self.setConfig("locale", locale)
        self.setConfig("footnotes_token", footnotes_token)
        self.setConfig("bibliography_token", bibliography_token)
        self.setConfig("strict", strict)

        # Set enum type parameters
        self.setConfig("notation", NotationStyle(notation))
        self.setConfig("output", OutputStyle(output))

        # Set Jinja templates
        self.setConfig(
            "num_template",
            CiteprocExtension._default_template_builder(num_template, "num.html")
        )
        self.setConfig(
            "footnote_template",
            CiteprocExtension._default_template_builder(footnote_template, "footnote.html")
        )
        self.setConfig(
            "inline_template",
            CiteprocExtension._default_template_builder(inline_template, "inline.html")
        )

        # Set and validate locale directory config
        if localedir != CiteprocConfigDefaults.BUILTIN:
            localedir = CiteprocExtension._string2path(localedir, directory=True)
        self.setConfig("localedir", localedir)

        # Set executable
        if citeproc_executable not in [CiteprocConfigDefaults.BUILTIN, CiteprocConfigDefaults.AVAILABLE]:
            citeproc_executable = CiteprocExtension._string2path(citeproc_executable)
        self.setConfig("citeproc_executable", citeproc_executable)

        if self.getConfig("notation") == NotationStyle.INLINE:
            self.preproc = InlinePreproc(self.getConfigs())
        elif self.getConfig("notation") == NotationStyle.INLINE_FOOTNOTE:
            self.preproc = InlineFootnotePreproc(self.getConfigs())
        elif self.getConfig("notation") == NotationStyle.FOOTNOTE:
            self.preproc = FootnotePreproc(self.getConfigs())
        else:
            raise CiteprocConfigException("Unknown notation style")

    def extendMarkdown(self, md):
        """Extend Python Markdown with CiteprocExtension"""
        md.preprocessors.register(self.preproc, name="CiteprocPreproc", priority=20)
        md.registerExtension(self)

    def get_warnings(self) -> list[CiteprocWarning]:
        return self.preproc.warnings

    @staticmethod
    def _none_to_empty_list(opt_ls: Optional[list]) -> list:
        """Create empty list from None, otherwise return list"""
        if opt_ls is None:
            return []
        return opt_ls

    @staticmethod
    def _default_template_builder(
            candidate: Union[CiteprocConfigDefaults, jinja2.Template, Path, str],
            default_filename: str
    ) -> jinja2.Template:
        """Build a jinja template according to type of candidate, use default_filename to get a default if necessary"""
        if isinstance(candidate, jinja2.Template):
            return candidate
        if isinstance(candidate, (Path, str)):
            tmplfile = Path(candidate)
            with tmplfile.open("r") as f:
                tmplstr = f.read()
            return jinja2.Template(tmplstr)
        if candidate == CiteprocConfigDefaults.BUILTIN:
            return Utilities.get_default_templates(default_filename)
        raise CiteprocConfigException("Unable to create jinja2.Template from config parameter")

    @staticmethod
    def _string2path(p: Optional[Union[Path, str]], directory: bool = False) -> Optional[Path]:
        """Cast str to Path, check if file exists"""
        if p is None:
            return None
        p = Path(p)
        if directory:
            if not p.is_dir():
                raise CiteprocConfigException("Directory not found: {}".format(str(p)))
        else:
            if not p.is_file():
                raise CiteprocConfigException("File not found: {}".format(str(p)))
        return p
