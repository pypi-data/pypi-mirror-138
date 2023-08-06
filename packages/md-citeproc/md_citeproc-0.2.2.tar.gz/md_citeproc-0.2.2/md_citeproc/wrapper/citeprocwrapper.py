import os
import json
import tempfile
import uuid
import shutil
import subprocess
from pathlib import Path
from typing import Optional, Union
from collections import deque

from md_citeproc.structures import CiteprocConfigDefaults
from md_citeproc.exceptions import CiteprocBinaryException
from md_citeproc.wrapper import SysInfo
from importlib import resources


class CiteprocWrapper:
    """Assemble and run rendering command as subprocess"""

    REFERENCE_DATA_FILE = "all_references.json"
    CMD_NAME = "citeproc-cli"

    def __init__(self, config: dict):
        self.config = config
        self.conversion_id: uuid.UUID = uuid.uuid4()
        self.refpath: Optional[Path] = None

    def _get_unpack_dir(self) -> Path:
        """Get path to temporarily dump packaged assets"""
        unpack_dir = Path(tempfile.gettempdir()) / "md_citeproc_assets" / str(self.conversion_id)
        unpack_dir.mkdir(exist_ok=True, parents=True)
        return unpack_dir

    def _prepare_locales(self) -> Path:
        """If built-in locales are used, unpack them, return locale dir to use"""
        if isinstance(self.config["localedir"], Path):
            return self.config["localedir"]
        loc_dir = self._get_unpack_dir()
        loc_files = resources.contents("md_citeproc.assets.locales")
        for i in loc_files:
            if i.split(".")[-1] in ["xml", "json"]:
                data = resources.read_text("md_citeproc.assets.locales", i)
                with (loc_dir / i).open('w') as f:
                    f.write(data)
        return loc_dir

    @staticmethod
    def _get_path_list() -> list[Path]:
        """Find all paths in PATH"""
        env_path = os.environ.get('PATH')
        if env_path:
            return [Path(i) for i in env_path.split(os.pathsep)]
        return []

    @staticmethod
    def _get_installed_executable() -> Optional[Path]:
        """Loop through PATH to find an installed executable"""
        for i in CiteprocWrapper._get_path_list():
            if SysInfo().system == "win":
                for j in ["{}.exe".format(CiteprocWrapper.CMD_NAME), "{}.cmd".format(CiteprocWrapper.CMD_NAME)]:
                    if (i / j).is_file():
                        return i / j
            else:
                if (i / CiteprocWrapper.CMD_NAME).is_file():
                    return i / CiteprocWrapper.CMD_NAME
        return None

    @staticmethod
    def _get_bundled_bin_file_name() -> Optional[str]:
        """Get the filename of the bundled citeproc executable matching the arch/sys"""
        sysinfo = SysInfo()
        if sysinfo.arch == "x64":
            bins = resources.contents("md_citeproc.assets.binary")
            for i in bins:
                if i.startswith("citeproc-cli") and sysinfo.system in i:
                    return i
        return None

    def _prepare_bundled_bin(self) -> Path:
        """Unpack bundled binary, make executable, return path"""
        fname = CiteprocWrapper._get_bundled_bin_file_name()
        if fname is None:
            CiteprocWrapper._raise_bundled_not_found()
        bin_path = self._get_unpack_dir() / fname
        bin_data = resources.read_binary("md_citeproc.assets.binary", fname)
        with bin_path.open("wb") as f:
            f.write(bin_data)
        bin_path.chmod(0o770)
        return bin_path

    def _get_executable(self) -> Path:
        """Look for specified, installed or packaged executable, depending on config, return path"""
        # Executable was specified, just return it
        if isinstance(self.config["citeproc_executable"], Path):
            return self.config["citeproc_executable"]
        # Look for an installed citeproc-cli
        if self.config["citeproc_executable"] == CiteprocConfigDefaults.AVAILABLE:
            executable = self._get_installed_executable()
            if executable is not None:
                return executable
        # Look for a bundled executable
        return self._prepare_bundled_bin()

    def _dump_references(self, references: list[list[dict[str, str]]]) -> Path:
        """Dump all reference data to a json file, return path"""
        refpath = self._get_unpack_dir() / CiteprocWrapper.REFERENCE_DATA_FILE
        with refpath.open("w") as f:
            json.dump(references, f)
        return refpath

    def _cleanup(self):
        """Delete packaged assets after conversion"""
        shutil.rmtree(self._get_unpack_dir())

    def get_rendered(self, references: list[list[dict[str, str]]], bibliography: bool = False) -> Union[deque[str], dict]:
        cmd = [self._get_executable()]
        # Append fixed strings from config
        cmd.extend(["-d", str(self.config["csljson"])])
        cmd.extend(["-s", str(self.config["cslfile"])])
        cmd.extend(["-l", str(self.config["locale"])])
        # Append localedir to command
        cmd.extend(["-j", str(self._prepare_locales())])
        # If necessary, add uncited items
        if self.config["uncited"] is not None:
            uncited = "'{}'".format(json.dumps(self.config["uncited"]))
            cmd.extend(["-u", uncited])
        # Add reference data file
        cmd.extend(["-p", "'{}'".format(str(self._dump_references(references)))])
        # Add bibliography flag if necessary
        if bibliography:
            cmd.append("-b")
        # EXECUTE!
        complete = subprocess.run(cmd, capture_output=True)
        if complete.returncode != 0:
            raise CiteprocBinaryException(complete.stderr.decode())
        rendered = json.loads(complete.stdout.decode())
        # We're done here, delete all unpacked data files
        self._cleanup()
        # Return results
        if bibliography:
            return rendered
        return deque(rendered)

    @staticmethod
    def _raise_bundled_not_found():
        raise CiteprocBinaryException(
            "No installed or bundled executable found for this system/architecture.\n\
            Try installing citeproc-cli with 'npm install citeproc-cli' \
            and adding it to PATH"
        )
