import tempfile
import uuid
import shutil
from pathlib import Path
from git import Repo

from md_citeproc.utils import Utilities


REPO_URL = "https://github.com/citation-style-language/locales.git"


def create_tmp_path() -> Path:
    p = Path(tempfile.gettempdir()) / ("locales_" + str(uuid.uuid4()))
    p.mkdir()
    return p


def clone_repo(p: Path):
    Repo.clone_from(REPO_URL, p)


def update_locales(repo: Path):
    target = Utilities.get_asset_dir() / "locales"
    for i in target.iterdir():
        i.unlink()
    for i in repo.iterdir():
        if i.suffix in [".xml", ".json"]:
            print("Copying {} to {}".format(i.name, target))
            shutil.copy2(i, target, follow_symlinks=False)


def cleanup(repo: Path):
    shutil.rmtree(repo)


if __name__ == "__main__":
    req = input("Do you want to update the bundled CSL locales from GitHub? [y/n]").lower()
    if req != "y":
        print("Quitting...")
        exit(0)
    rp = create_tmp_path()
    clone_repo(rp)
    update_locales(rp)
    cleanup(rp)
    print("SUCCESS!")
