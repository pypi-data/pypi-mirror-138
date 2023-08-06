import uuid
import shutil
import subprocess
import tempfile
from pathlib import Path

from md_citeproc.utils import Utilities


def get_temp_dirs() -> (Path, Path):
    identifier = str(uuid.uuid4())
    install_dir = Path(tempfile.gettempdir()) / ("npm_install_" + identifier)
    install_dir.mkdir()
    build_dir = Path(tempfile.gettempdir()) / ("npm_build_" + identifier)
    return install_dir, build_dir


def get_from_npm(install_dir: Path):
    subprocess.run(["npm", "i", "citeproc-cli"], cwd=install_dir)


def isolate_package(install_dir: Path, build_dir: Path):
    package = install_dir / "node_modules" / "citeproc-cli"
    shutil.copytree(package, build_dir)


def build_binaries(build_dir: Path):
    subprocess.run(["npm", "install", "."], cwd=build_dir)
    subprocess.run(["npm", "install", "--only=dev", "."], cwd=build_dir)
    subprocess.run(["./node_modules/.bin/pkg", "."], cwd=build_dir)


def update_binaries(build_dir: Path):
    bindir = Utilities.get_asset_dir() / "binary"
    distdir = build_dir / "dist"
    shutil.copytree(distdir, bindir, dirs_exist_ok=True)


def cleanup(install_dir: Path, build_dir: Path):
    shutil.rmtree(install_dir)
    shutil.rmtree(build_dir)


if __name__ == "__main__":
    req = input("Do you want update citeproc-cli from npm and rebuild bundled binaries? [y/n]").lower()
    if req != "y":
        print("Quitting...")
        exit(0)
    inst, build = get_temp_dirs()
    get_from_npm(inst)
    isolate_package(inst, build)
    build_binaries(build)
    update_binaries(build)
    cleanup(inst, build)
    print("SUCCESS!")
