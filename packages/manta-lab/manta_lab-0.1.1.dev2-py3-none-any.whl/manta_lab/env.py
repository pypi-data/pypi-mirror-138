import os
import platform
from distutils.util import strtobool

# env keys
HTTP_TIMEOUT = "MANTA_HTTP_TIMEOUT"
BASE_DIR = "MANTA_BASE_DIR"
CACHE_DIR = "MANTA_CACHE_DIR"
API_KEY = "MANTA_API_KEY"
MANTA_DIR = "MANTA_DIR"

# run & tuning keys
EXPERIMENT_ID = "MANTA_EXPERIMENT_ID"
TUNE_ID = "MANTA_SWEEP_ID"
TUNE_PARAM_PATH = "MANTA_SWEEP_PARAM_PATH"
AGENT_MAX_INITIAL_FAILURES = "MANTA_AGENT_MAX_INITIAL_FAILURES"
AGENT_DISABLE_FLAPPING = "MANTA_AGENT_DISABLE_FLAPPING"

# meta related
HOST = "MANTA_HOST"
PROGRAM = "MANTA_PROGRAM"
DISABLE_GIT = "MANTA_DISABLE_GIT"
SAVE_CODE = "MANTA_SAVE_CODE"

# cli
ENTITY = "MANTA_ENTITY"

#
SYS_PLATFORM = platform.system()


def env_as_bool(key, env=None):
    env = env or os.environ
    val = env.get(key, None)
    try:
        val = bool(strtobool(val))
        return val
    except (AttributeError, ValueError):
        return None


def get_http_timeout(default=10, env=None):
    env = env or os.environ
    val = int(env.get(HTTP_TIMEOUT, default))
    return val


def get_manta_sysdir(env=None):
    default_dir = os.path.expanduser(os.path.join("~", ".manta"))
    env = env or os.environ
    path = env.get(BASE_DIR, default_dir)
    return path


def get_manta_credential_path():
    return os.path.expanduser("~/.manta/credential")


def get_manta_cache_dir(env=None):
    default_dir = os.path.expanduser(os.path.join("~", ".cache", "manta"))
    env = env or os.environ
    path = env.get(CACHE_DIR, default_dir)
    return path


def get_manta_dir(env=None):
    if env is None:
        env = os.environ
    return env.get(MANTA_DIR, None)


def get_agent_max_initial_failures(default=None, env=None):
    if env is None:
        env = os.environ
    val = env.get(AGENT_MAX_INITIAL_FAILURES, default)
    try:
        val = int(val)
    except ValueError:
        val = default
    return val


def enable_save_code(env=None):
    return env_as_bool(SAVE_CODE) or False


def disable_git(env=None):
    return env_as_bool(DISABLE_GIT) or False


def get_cuda_version():
    version = None
    try:
        if os.path.exists("/usr/local/cuda/version.txt"):
            with open("/usr/local/cuda/version.txt") as f:
                version = f.read().split(" ")[-1].strip()
    except Exception:
        pass
    return version
