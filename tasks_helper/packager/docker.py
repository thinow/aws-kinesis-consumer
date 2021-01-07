import invoke

from tasks_helper.packager.base import Packager

BUILD_FOLDER = 'build-docker'


class DockerPackager(Packager):
    def get_name(self) -> str:
        return "docker"

    def build(self, runner: invoke.Runner) -> None:
        runner.run(f'rm -rvf {BUILD_FOLDER}')
        runner.run(f'mkdir -v {BUILD_FOLDER}')
        for filepath in ['aws_kinesis_consumer', 'Pipfile', 'Pipfile.lock', 'docker/aws-kinesis-consumer/Dockerfile']:
            runner.run(f'cp -Rv {filepath} {BUILD_FOLDER}')
        runner.run(f'docker build -t aws-kinesis-consumer {BUILD_FOLDER}')
