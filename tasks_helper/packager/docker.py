import os

import invoke

from aws_kinesis_consumer.configuration.factory import AWS_KINESIS_CONSUMER_VERSION
from tasks_helper.packager.base import Packager

IMAGE_NAME = 'thinow/aws-kinesis-consumer'

BUILD_FOLDER = 'build-docker'

REQUIRED_IN_DOCKER_CONTEXT = (
    'docker/aws-kinesis-consumer/Dockerfile',
    'aws_kinesis_consumer',
)

DOCKER_HUB_DESCRIPTION = 'Consume an AWS Kinesis Data Stream to look over the records from a terminal.'


class DockerPackager(Packager):
    def get_name(self) -> str:
        return "docker"

    def build(self, runner: invoke.Runner) -> None:
        runner.run(f'rm -rvf {BUILD_FOLDER}')
        runner.run(f'mkdir -v {BUILD_FOLDER}')
        for file in REQUIRED_IN_DOCKER_CONTEXT:
            runner.run(f'cp -Rv {file} {BUILD_FOLDER}')
        runner.run(f'pipenv lock --requirements | grep -v \'#\' > {BUILD_FOLDER}/requirements.txt')
        runner.run(f'docker build -t {IMAGE_NAME}:beta {BUILD_FOLDER}')

    def deploy(self, runner: invoke.Runner, destination: str) -> None:
        runner.run(f'docker push {IMAGE_NAME}:beta')
        if destination == 'production':
            DockerPackager.push_doc_to_docker_hub(runner)
            for tag in ('latest', AWS_KINESIS_CONSUMER_VERSION):
                runner.run(f'docker tag {IMAGE_NAME}:beta {IMAGE_NAME}:{tag}')
                runner.run(f'docker push {IMAGE_NAME}:{tag}')

    @staticmethod
    def push_doc_to_docker_hub(runner: invoke.Runner) -> None:
        runner.run(f'''
            docker run --rm \
                -e DOCKERHUB_USERNAME="{os.environ["DOCKER_USERNAME"]}" \
                -e DOCKERHUB_PASSWORD="{os.environ["DOCKER_PASSWORD"]}" \
                -e DOCKERHUB_REPO_PREFIX=thinow \
                -e DOCKERHUB_REPO_NAME=aws-kinesis-consumer \
                -e SHORT_DESCRIPTION="{DOCKER_HUB_DESCRIPTION}" \
                -v $PWD/README.md:/data/README.md \
                sheogorath/readme-to-dockerhub
        ''')
