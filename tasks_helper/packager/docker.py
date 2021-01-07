import invoke

from setup import VERSION
from tasks_helper.packager.base import Packager

IMAGE_NAME = 'thinow/aws-kinesis-consumer'

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
        runner.run(f'docker build -t {IMAGE_NAME}:beta {BUILD_FOLDER}')

    def deploy(self, runner: invoke.Runner, destination: str) -> None:
        runner.run(f'docker push {IMAGE_NAME}:beta')
        for tag in ('latest', VERSION):
            runner.run(f'docker tag {IMAGE_NAME}:beta {IMAGE_NAME}:{tag}')
            runner.run(f'docker push {IMAGE_NAME}:{tag}')
