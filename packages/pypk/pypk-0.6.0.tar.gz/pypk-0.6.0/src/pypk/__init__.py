from . import config, core, main  # noqa: F401

try:
    from .version import version
except ImportError:
    __version__ = "0.0.0"
else:
    __version__ = version
    del version
