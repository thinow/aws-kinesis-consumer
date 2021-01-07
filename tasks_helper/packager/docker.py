import invoke

from tasks_helper.packager.base import Packager

BUILD_FOLDER = 'build-docker'

REQUIRED_IN_DOCKER_CONTEXT = (
    'docker/aws-kinesis-consumer/Dockerfile',
    'aws_kinesis_consumer',
    'Pipfile',
    'Pipfile.lock',
)


class DockerPackager(Packager):
    def get_name(self) -> str:
        return "docker"

    def build(self, runner: invoke.Runner) -> None:
        runner.run(f'rm -rvf {BUILD_FOLDER}')
        runner.run(f'mkdir -v {BUILD_FOLDER}')
        for file in REQUIRED_IN_DOCKER_CONTEXT:
            runner.run(f'cp -Rv {file} {BUILD_FOLDER}')
        runner.run(f'docker build -t aws-kinesis-consumer {BUILD_FOLDER}')

    def deploy(self, runner: invoke.Runner, destination: str) -> None:
        # TODO implement docker push
        runner.run('echo "Not yet implemented!"')
        pass
