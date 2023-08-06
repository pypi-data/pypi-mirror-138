import platform


class SysInfo:
    """Get infos about OS/architecture in standardized form"""

    @property
    def system(self):
        system = platform.system()
        if system == "Windows":
            return "win"
        if system == "Darwin":
            return "macos"
        if system == "Linux":
            return "linux"
        return system

    @property
    def arch(self):
        arch = platform.machine()
        if arch in ["x86_64", "amd64", "x64"]:
            return "x64"
        return arch
