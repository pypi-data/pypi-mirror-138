from pathlib import Path
"""
from lxml import etree
from jsonschema import validate

from md_citeproc.utils import Utilities
from md_citeproc.exceptions import CiteprocException
"""


class Validators:

    @staticmethod
    def _get_schemata_dir() -> Path:
        """Get base path of schemata dir"""
        """
        return Utilities.get_asset_dir() / "schemata"
        """
        raise NotImplementedError("Schemata validation is not implemented yet")

    @staticmethod
    def validate_csl(p: Path) -> bool:
        """Check syntax of a CSL file"""
        """
        schema = Validators._get_schemata_dir() / "csl.rng"
        with schema.open('r') as f:
            relaxng_doc = etree.parse(f)
        relaxng = etree.RelaxNG(relaxng_doc)
        with p.open('r') as f:
            csldoc = etree.parse(f)
        valid = relaxng.validate(csldoc)
        return valid
        """
        raise NotImplementedError("Schemata validation is not implemented yet")

    @staticmethod
    def validate_csljson(p: Path) -> bool:
        """Check syntax of a CSLJSON file"""
        """
        schema = Validators._get_schemata_dir() / "csl-data.json"
        with schema.open('r') as f:
            sdata = f.read()
        with p.open('r') as f:
            data = f.read()
        return validate(data, sdata)
        """
        raise NotImplementedError("Schemata validation is not implemented yet")
