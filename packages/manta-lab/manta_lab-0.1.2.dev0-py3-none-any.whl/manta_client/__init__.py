import manta_lab.base as manta_base
from manta_lab.tuning.interface.agent import Agent

Settings = manta_base.Settings
Config = manta_base.Config

from manta_lab import env, sdk, tuning, util

__version__ = "0.1.1.dev0"

init = sdk.init
setup = sdk.setup
login = sdk.login
finish = sdk.finish
Artifact = sdk.Artifact

tune = tuning.tune
agent = tuning.agent
controller = tuning.controller

# global vars
experiment = None
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
    "experiment",
    "config",
    "meta",
    "log",
    "save",
    "alarm",
    "use_artifact",
    "log_artifact",
]
