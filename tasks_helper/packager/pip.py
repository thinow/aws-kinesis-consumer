import invoke

from tasks_helper.packager.base import Packager


class PipPackager(Packager):
    def get_name(self) -> str:
        return "pip"

    def build(self, runner: invoke.Runner) -> None:
        runner.run('rm -rf dist/')
        runner.run('pipenv-setup sync')
        runner.run('python setup.py sdist bdist_wheel')
