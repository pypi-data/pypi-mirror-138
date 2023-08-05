# Published at https://pypi.org/project/acryl-datahub/.
__package_name__ = "acryl-datahub"
__version__ = "0.8.26.1"


def is_dev_mode() -> bool:
    return __version__.endswith("dev0")


def nice_version_name() -> str:
    if is_dev_mode():
        return "unavailable (installed in develop mode)"
    return __version__
