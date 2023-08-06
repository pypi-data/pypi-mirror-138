import logging
import typing

logger = logging.getLogger(__name__)


class GitInfo:
    def __init__(self, path: str):
        self.repo = self.build_repo(path)

    def build_repo(self, path: str):
        # https://github.com/gitpython-developers/GitPython/blob/cd29f07b2efda24bdc690626ed557590289d11a6/git/cmd.py#L365
        # looks like the import itself may fail in case the git executable
        # is not found
        # putting the import here so that the caller can handle the exception
        import git

        repo = git.Repo(path, search_parent_directories=True)

        return repo

    @property
    def current_commit_sha(self) -> str:
        return self.repo.head.object.hexsha

    @property
    def current_branch_name(self) -> str:
        return self.repo.active_branch.name

    @property
    def remote_url(self) -> typing.Optional[str]:
        remotes = self.repo.remotes
        if len(remotes) != 1:
            logger.warning("either more than one or no remote detected")
            return None
        return remotes[0].url

    @property
    def diff_patch(self) -> str:
        return self.repo.git.diff("--patch", "HEAD")

    @property
    def is_dirty(self) -> bool:
        return self.repo.is_dirty()
