import datetime
import json
import multiprocessing
import os
import subprocess
import sys
from shutil import copyfile
from typing import List

import pynvml

import manta_lab as ml
from manta_lab.base.filenames import (
    CONDA_ENVIRONMENTS_FNAME,
    DIFF_FNAME,
    METADATA_FNAME,
    REQUIREMENTS_FNAME,
)
from manta_lab.base.git_repo import GitRepo


def parse_pip_reqs(save_path):
    try:
        import pkg_resources

        installed_packages = [d for d in iter(pkg_resources.working_set)]
        installed_packages_list = sorted(["%s==%s" % (i.key, i.version) for i in installed_packages])
        with open(save_path, "w") as f:
            f.write("\n".join(installed_packages_list))
    except Exception:
        print("Error saving pip packages")
    print("save pip done")


def parse_conda_env(save_path):
    current_shell_is_conda = os.path.exists(os.path.join(sys.prefix, "conda-meta"))
    if not current_shell_is_conda:
        return False

    print("save conda")
    try:
        with open(save_path, "w") as f:
            subprocess.call(["conda", "env", "export"], stdout=f, stderr=subprocess.DEVNULL)
    except Exception:
        print("Error saving conda packages")
    print("save conda done")


def save_code(settings, repo: GitRepo) -> str:
    root = repo.root or os.getcwd()
    program_relative = settings.program_relpath
    ml.util.mkdir(os.path.join(settings.files_dir, "code", os.path.dirname(program_relative)))

    program_absolute = os.path.join(root, program_relative)
    if not os.path.exists(program_absolute):
        print("unable to save code -- can't find %s" % program_absolute)
        return

    saved_program = os.path.join(settings.files_dir, "code", program_relative)
    if not os.path.exists(saved_program):
        copyfile(program_absolute, saved_program)
    print("save code done")

    return program_relative


def save_git_patches(settings, repo: GitRepo) -> List:
    """Save the current state of this repository"""
    print("save patches")
    base_dir = settings.files_dir
    saved_patches = []
    try:
        root = repo.root
        diff_args = ["git", "diff", "--submodule=diff"]

        if repo.dirty:
            patch_path = os.path.join(base_dir, DIFF_FNAME)
            with open(patch_path, "wb") as patch:
                subprocess.check_call(diff_args + ["HEAD"], stdout=patch, cwd=root, timeout=5)
                saved_patches.append(os.path.relpath(patch_path, start=base_dir))

        upstream_commit = repo.get_upstream_fork_point()
        if upstream_commit != repo.repo.head.commit:
            sha = upstream_commit.hexsha
            upstream_patch_path = os.path.join(base_dir, "upstream_diff_{}.patch".format(sha))
            with open(upstream_patch_path, "wb") as upstream_patch:
                subprocess.check_call(diff_args + [sha], stdout=upstream_patch, cwd=root, timeout=5)
                saved_patches.append(os.path.relpath(upstream_patch_path, start=base_dir))
    except (
        subprocess.CalledProcessError,
        subprocess.TimeoutExpired,
    ) as e:
        print("Error generating diff patches: %s" % e)
    print("save patches done")
    return saved_patches


class Meta:
    def __init__(self, settings: ml.Settings, interface=None) -> None:
        self._settings = settings
        self._interface = interface

        self.data = {}
        self._git = GitRepo(remote=settings["git_remote"] if "git_remote" in settings.keys() else "origin")

        self._saved_code_path = None
        self._saved_patches = []

        self.patch_path = os.path.join(settings.files_dir, DIFF_FNAME)
        self.pip_req_path = os.path.join(settings.files_dir, REQUIREMENTS_FNAME)
        self.conda_env_path = os.path.join(settings.files_dir, CONDA_ENVIRONMENTS_FNAME)
        self.meta_path = os.path.join(settings.files_dir, METADATA_FNAME)

    def _collect_sys(self):
        self.data["system"] = self._settings.system
        self.data["python"] = self._settings.python
        self.data["startedAt"] = self._settings.start_timestamp
        self.data["docker"] = self._settings.docker

        try:
            pynvml.nvmlInit()
            self.data["gpu"] = pynvml.nvmlDeviceGetName(pynvml.nvmlDeviceGetHandleByIndex(0)).decode("utf8")
            self.data["gpu_count"] = pynvml.nvmlDeviceGetCount()
        except Exception:
            pass
        try:
            self.data["cpu_count"] = multiprocessing.cpu_count()
        except Exception:
            pass

        self.data["cuda"] = self._settings.cuda
        self.data["args"] = self._settings.args
        self.data["state"] = "running"

    def _collect_git(self):
        self.data["git"] = {
            "remote": self._git.remote_url,
            "commit": self._git.last_commit,
        }
        self.data["email"] = self._git.email
        self.data["root"] = self._git.root or self.data["root"] or os.getcwd()

    def collect(self):
        """Collect meta information
        system, git, pip-requirements, conda-env
        """
        self._collect_sys()

        if not self._settings.disable_git and self._git.enabled:
            self._collect_git()

        if self._settings.save_code:
            if self._settings.program_relpath is not None:
                self._saved_code_path = save_code(self._code_path)
            if self._git.enabled:
                self._saved_patches = save_git_patches(self._git_patches)

        if self._settings.save_requirements:
            parse_pip_reqs(self.pip_req_path)
            parse_conda_env(self.conda_env_path)

    def register(self):
        # update meta info
        self._interface.publish_meta(self.data)

        with open(self.meta_path, "w") as f:
            s = json.dumps(self.data, indent=4)
            f.write(s)
            f.write("\n")
        base_name = os.path.basename(self.meta_path)
        meta_files = [base_name]

        if self._saved_code_path:
            saved_program = os.path.join("code", self._saved_code_path)
            meta_files.append(saved_program)
        for patch in self._saved_patches:
            meta_files.append(patch)

        # TODO: files upload by artifact
        # meta_artifact = Artifact()

        # upload meta related files
        # self._interface.publish_artifact(meta_artifact)


if __name__ == "__main__":

    m = Meta(ml.Settings())
    m.collect()
