import invoke

from tasks_helper.packager.base import Packager


class PipPackager(Packager):
    def get_name(self) -> str:
        return "pip"

    def build(self, runner: invoke.Runner) -> None:
        runner.run('rm -rf dist/')
        runner.run('pipenv-setup sync')
        runner.run('python setup.py sdist bdist_wheel')

    def deploy(self, runner: invoke.Runner, destination: str) -> None:
        runner.run('pip install twine==3.2.0')
        if destination == 'staging':
            runner.run('twine upload --skip-existing --repository-url https://test.pypi.org/legacy/ dist/*')
        elif destination == 'production':
            runner.run('twine upload dist/*')
        else:
            raise ValueError(f'Unknown argument : {destination}')
