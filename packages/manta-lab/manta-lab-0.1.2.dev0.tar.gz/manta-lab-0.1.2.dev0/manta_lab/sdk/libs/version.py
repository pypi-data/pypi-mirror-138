#
import requests
from pkg_resources import parse_version

import manta_lab as ml


def _find_available(current_version):
    pypi_url = f"https://pypi.org/pypi/{ml.__pypi_name__}/json"
    yanked_dict = {}
    try:
        pkg = requests.get(pypi_url, timeout=3).json()

        latest_version = pkg["info"]["version"]
        for version, fields in pkg["releases"].items():
            for item in fields:
                if item["yanked"]:
                    yanked_dict[version] = item.get("yanked_reason")
    except Exception:
        return

    result = dict(
        latest_version=latest_version,
        upgradable=True,
        pip_prerelease=False,
        deleted=False,
        yanked=False,
        yanked_reason="",
    )
    # Check if current version has been yanked or deleted
    # no return yanked or deleted if there is nothing to upgrade to
    release_list = pkg["releases"].keys()
    if current_version in release_list:
        result["yanked"] = current_version in yanked_dict
        result["yanked_reason"] = yanked_dict.get(current_version, None)
    else:
        result["deleted"] = True

    # Check pre-releases
    parsed_current_version = parse_version(current_version)
    if parse_version(latest_version) <= parsed_current_version:
        # pre-releases are not included in latest_version
        # so if we are currently running a pre-release we check more
        if not parsed_current_version.is_prerelease:
            return
        # Candidates are pre-releases with the same base_version
        release_list = map(parse_version, release_list)
        release_list = filter(lambda v: v.is_prerelease, release_list)
        release_list = filter(
            lambda v: v.base_version == parsed_current_version.base_version,
            release_list,
        )
        release_list = sorted(release_list)
        if not release_list:
            return

        parsed_latest_version = release_list[-1]
        if parsed_latest_version <= parsed_current_version:
            result["upgradable"] = False
        result["latest_version"] = str(parsed_latest_version)
        result["pip_prerelease"] = True

    return result


def parse_version_messages(current_version):
    info = _find_available(current_version)
    if not info:
        return

    upgrade_message = None
    yank_message = None
    delete_message = None

    if info["upgradable"]:
        lib_name = ml.__pypi_name__
        pip_postfix = " --pre" if info["pip_prerelease"] else ""  # noqa
        upgrade_message = (
            f"{lib_name} version {info['latest_version']} is available!  To upgrade, please run:\n"
            f" $ pip install {lib_name} --upgrade{pip_postfix}"
        )

    if info["deleted"]:
        delete_message = f"{lib_name} version {current_version} has been retired!  Please upgrade."

    if info["yanked"]:
        yank_message = (
            f"{lib_name} version {current_version} has been recalled!  ({info['yanked_reason']}) Please upgrade."
        )

    return {
        "upgrade_message": upgrade_message,
        "yank_message": delete_message,
        "delete_message": yank_message,
    }


if __name__ == "__main__":
    parse_version_messages("0.0.1")
