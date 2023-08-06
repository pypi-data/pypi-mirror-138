import getpass
import os
import stat
import sys
import textwrap
from urllib.parse import urlparse

import requests

import manta_lab as ml

LOGIN_CHOICE_NEW = "Create Manta-Lab account"
LOGIN_CHOICE_EXISTS = "Use existing Manta-Lab account"
LOGIN_CHOICES = [
    LOGIN_CHOICE_NEW,
    LOGIN_CHOICE_EXISTS,
]


def _prompt_choices(
    choices,
):
    # TODO: more beautiful prompt
    for i, c in enumerate(choices):
        print(f"({i+1}) {c}")

    idx = -1
    while idx < 0 or idx > len(choices) - 1:
        # TODO: do we need input timeout?
        choice = input("MantaLab: Enter your choice: ")
        if not choice:
            continue
        idx = -1
        try:
            idx = int(choice) - 1
        except ValueError:
            pass
        if idx < 0 or idx > len(choices) - 1:
            print("Invalid choice")
    result = choices[idx]
    print("You chose '%s'" % result)

    return result


def prompt_api_key(settings, api=None) -> str:  # noqa: C901
    """Prompt for api key."""
    input_callback = getpass.getpass
    api = api or ml.api.MantaAPI(settings)
    jupyter = False  # TODO: settings._jupyter or False
    base_url = settings.base_url

    choices = [choice for choice in LOGIN_CHOICES]

    if jupyter and "google.colab" in sys.modules:
        # TODO: colab support
        key = ml.jupyter.attempt_colab_login(base_url)
        if key is not None:
            write_key(settings, key, api=api)
            return key

    # TODO: add forced choice by execution environment
    # TODO: need awsome choice display
    result = _prompt_choices(choices)

    api_ask = "MantaLab: Paste an API key from your profile and hit enter, or press ctrl+c to quit: "

    if result == LOGIN_CHOICE_NEW:
        print(f"Create an account here: {base_url}/authorize?signup=true")
    elif result == LOGIN_CHOICE_EXISTS:
        print(f"You can find your API key in your browser here: {base_url}/authorize")

    key = input_callback(api_ask).strip()
    write_key(settings, key, api=api)
    return key


def write_netrc(host, entity, key):
    try:
        normalized_host = urlparse(host).netloc.split(":")[0]
        if normalized_host != "localhost" and "." not in normalized_host:
            print("Host must be a url in the form https://some.address.com, received {}".format(host))
            return None
        print("Appending key for {} to your netrc file: {}".format(normalized_host, os.path.expanduser("~/.netrc")))
        machine_line = "machine %s" % normalized_host
        path = os.path.expanduser("~/.netrc")
        original_contents = None
        try:
            with open(path) as f:
                original_contents = f.read().strip().split("\n")
        except IOError:
            pass
        with open(path, "w") as f:
            if original_contents:
                # delete this machine from the file if it's already there.
                skip = 0
                for line in original_contents:
                    # we fix invalid netrc files with an empty host that we wrote before
                    # verifying host...
                    if line == "machine " or machine_line in line:
                        skip = 2
                    elif skip:
                        skip -= 1
                    else:
                        f.write("%s\n" % line)
            f.write(
                textwrap.dedent(
                    f"""\
            machine {normalized_host}
              login {entity}
              password {key}
            """
                )
            )
        os.chmod(os.path.expanduser("~/.netrc"), stat.S_IRUSR | stat.S_IWUSR)
        return True
    except IOError:
        print("Unable to read ~/.netrc")
        return None


def write_manta_credential(host, entity, key):
    path = ml.env.get_manta_credential_path()
    if not os.path.exists(path):
        ml.util.parent_makedirs(path)

    credential = ml.util.read_yaml(path)
    _info = {
        host: {entity: key},
    }
    credential.update(_info)
    ml.util.save_yaml(path, credential)


def read_manta_credential(host, entity="user"):
    path = ml.env.get_manta_credential_path()
    credential = ml.util.read_yaml(path)

    try:
        return credential[host][entity]
    except KeyError:
        print(f"credential not exists {host}/{entity}")
        return None


def write_key(settings, key, api=None):
    if not key:
        raise ValueError("No API key specified.")

    # TODO: Do we need validate before writing?
    # api = api or ml.api.MantaAPI(settings)
    if len(key) != 20:
        raise ValueError("API key must be 20 characters long, yours was %s" % len(key))

    # write_netrc(settings.base_url, "user", key)
    write_manta_credential(settings.base_url, "user", key)


def api_key(settings=None):
    if not settings:
        settings = ml.setup().settings
    if settings.api_key:
        return settings.api_key
    auth = read_manta_credential(settings.base_url)
    return auth


if __name__ == "__main__":
    s = ml.Settings()
    print(api_key(s))
    prompt_api_key(s)
    api_key(s)
