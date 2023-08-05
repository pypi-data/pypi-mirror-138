import manta_lab.base as manta_base
from manta_lab.tuning.interface.agent import Agent

Settings = manta_base.Settings
Config = manta_base.Config

from manta_lab import dtypes, env, sdk, tuning, util
from manta_lab.dtypes import (
    Audio,
    Graph,
    Histogram,
    Html,
    Image,
    Molecule,
    Object3D,
    Plotly,
    Table,
    Video,
)
from manta_lab.errors.term import (
    termcritical,
    termdeug,
    termerror,
    termlog,
    termsetup,
    termwarn,
)

__version__ = "0.1.1.dev0"
__pypi_name__ = "manta-lab"

init = sdk.init
setup = sdk.setup
login = sdk.login
finish = sdk.finish
Artifact = sdk.Artifact

tune = tuning.tune
agent = tuning.agent
controller = tuning.controller

# global vars
run = None
config = None
meta = None

# global functions
log = None
save = None
alarm = None
use_artifact = None
log_artifact = None

__all__ = [
    "__version__",
    "init",
    "setup",
    "login",
    "Settings",
    "Config",
    "run",
    "config",
    "meta",
    "log",
    "save",
    "alarm",
    "use_artifact",
    "log_artifact",
    "Audio",
    "Graph",
    "Histogram",
    "Html",
    "Image",
    "Molecule",
    "Object3D",
    "Plotly",
    "Table",
    "Video",
]
