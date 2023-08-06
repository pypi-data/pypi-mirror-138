import configparser
import functools
import os
from urllib.parse import urlparse, urlunparse

from git import exc, Repo


def false_if_git_disabled(func):
    @functools.wraps(func)
    def wrapped_func(*args, **kwargs):
        if not args[0].repo:
            return False
        else:
            return func(*args, **kwargs)

    return wrapped_func


class GitRepo:
    def __init__(self, root=None, remote="origin", lazy=True):
        self.remote_name = remote
        self._root = root
        self._repo = None
        if not lazy:
            self.repo

    @property
    def repo(self):
        if self._repo is None:
            if self.remote_name is None:
                self._repo = False
            else:
                try:
                    self._repo = Repo(self._root or os.getcwd(), search_parent_directories=True)
                except exc.InvalidGitRepositoryError:
                    print("git repository is invalid")
                    self._repo = False
        return self._repo

    @property
    def enabled(self):
        return bool(self.repo)

    @property
    @false_if_git_disabled
    def branch(self):
        return self.repo.head.ref.name

    @property
    @false_if_git_disabled
    def dirty(self):
        return self.repo.is_dirty()

    @property
    @false_if_git_disabled
    def email(self):
        try:
            return self.repo.config_reader().get_value("user", "email")
        except configparser.Error:
            return None

    @property
    @false_if_git_disabled
    def last_commit(self):
        if not self.repo.head or not self.repo.head.is_valid():
            return None
        try:
            if len(self.repo.refs) > 0:
                return self.repo.head.commit.hexsha
            else:
                return self.repo.git.show_ref("--head").split(" ")[0]
        except Exception:
            print("Unable to find most recent commit in git")
            return None

    @property
    @false_if_git_disabled
    def root(self):
        return self.repo.git.rev_parse("--show-toplevel")

    @property
    @false_if_git_disabled
    def remote(self):
        try:
            return self.repo.remotes[self.remote_name]
        except IndexError:
            return None

    @property
    def remote_url(self):
        if not self.remote:
            return None
        parsed = urlparse(self.remote.url)
        hostname = parsed.hostname
        if parsed.port:
            hostname += ":" + str(parsed.port)
        if parsed.password:
            loc = f"{parsed.username}:@{hostname}"
            return urlunparse(parsed._replace(netloc=loc))
        return urlunparse(parsed._replace(netloc=hostname))

    @property
    @false_if_git_disabled
    def root_dir(self):
        return self.repo.git.rev_parse("--show-toplevel")

    @false_if_git_disabled
    def get_upstream_fork_point(self):
        """Get the most recent ancestor of HEAD that occurs on an upstream
        branch.

        First looks at the current branch's tracking branch, if applicable. If
        that doesn't work, looks at every other branch to find the most recent
        ancestor of HEAD that occurs on a tracking branch.

        Returns:
            git.Commit object or None

        https://git-scm.com/book/en/v2/Git-Branching-Remote-Branches
        https://git-scm.com/docs/git-merge-base
        """
        possible_relatives = []
        try:
            try:
                branch = self.repo.active_branch
            except (TypeError, ValueError):
                print("git is in a detached head state")
                return None  # detached head
            else:
                tracking_branch = branch.tracking_branch()
                if tracking_branch is not None:
                    possible_relatives.append(tracking_branch.commit)

            if len(possible_relatives) == 0:
                for branch in self.repo.branches:
                    tracking_branch = branch.tracking_branch()
                    if tracking_branch is not None:
                        possible_relatives.append(tracking_branch.commit)

            most_recent_ancestor = None
            for relative in possible_relatives:
                # When the history involves criss-cross merges,
                # there can be more than one best common ancestor
                for common_ancestor in self.repo.merge_base(self.repo.head, relative):
                    if most_recent_ancestor is None:
                        most_recent_ancestor = common_ancestor
                    elif self.repo.is_ancestor(most_recent_ancestor, common_ancestor):
                        most_recent_ancestor = common_ancestor
            return most_recent_ancestor

        except exc.GitCommandError as e:
            print(f"git remote upstream fork point could not be found: {e}")
            return None

    @false_if_git_disabled
    def is_tracked(self, file_name):
        return file_name not in self.repo.untracked_files


if __name__ == "__main__":
    g = GitRepo()
    # g.root
    # g.remote
    # g.remote_url
    # g.branch
    # g.email
    # g.last_commit
    # g.repo
    # g.root_dir
    # g.get_upstream_fork_point()
    # g.is_tracked()
