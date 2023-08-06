from manta_lab import dtypes, env, tuning, util
from manta_lab.base import Config, Settings
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
from manta_lab.tuning.interface.agent import Agent

__version__ = "0.1.1.dev1"
__pypi_name__ = "manta-lab"

import manta_lab.sdk as sdk

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
config = Config()
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
