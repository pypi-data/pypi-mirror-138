from pathlib import Path
import jinja2
from importlib import resources


class Utilities:
    """Static utilities for CiteprocExtension"""

    @staticmethod
    def get_asset_dir() -> Path:
        """
        Path to asset directory
        only used by updaters, since not based on importlib/resources
        """
        p = Path(__file__).parent / "assets"
        if not p.is_dir():
            raise ValueError("Asset directory not found at {}".format(str(p)))
        return p

    @staticmethod
    def citekey_trim(key: str) -> str:
        """split of '@' from citekey"""
        return key[1:]

    @staticmethod
    def merge_lines(s: str) -> str:
        """Remove all Linebreaks from a string"""
        return s.replace("\n", "").replace("\r", "")

    @staticmethod
    def get_default_templates(filename: str) -> jinja2.Template:
        """Get built-in template from file name"""
        tmplstr = resources.read_text("md_citeproc.assets.templates", filename)
        return jinja2.Template(tmplstr)
