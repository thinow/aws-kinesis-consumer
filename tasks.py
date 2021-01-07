from invoke import task

from tasks_helper.demo.demo_consumer import DemoConsumer
from tasks_helper.demo.demo_producer import DemoProducer


@task
def test(c):
    c.run('docker-compose up -d')
    c.run('python -m pytest -vv')
    c.run('docker-compose down')


@task
def build(c):
    c.run('rm -rf dist/')
    c.run('pipenv-setup sync')
    c.run('python setup.py sdist bdist_wheel')


@task
def dockerbuild(c):
    build_folder = 'docker-build'
    c.run(f'rm -rvf {build_folder}')
    c.run(f'mkdir -v {build_folder}')
    for filepath in ['aws_kinesis_consumer', 'Pipfile', 'Pipfile.lock', 'docker/aws-kinesis-consumer/Dockerfile']:
        c.run(f'cp -Rv {filepath} {build_folder}')
    c.run(f'docker build -t aws-kinesis-consumer {build_folder}')


@task
def deploy(c, destination):
    if destination == 'staging':
        c.run('pip install twine==3.2.0')
        c.run('twine upload --skip-existing --repository-url https://test.pypi.org/legacy/ dist/*')
    elif destination == 'production':
        c.run('pip install twine==3.2.0')
        c.run('twine upload dist/*')
    else:
        raise ValueError(f'Unknown argument : {destination}')


@task
def demo(c, action):
    if action == 'consume':
        DemoConsumer.run(c, 'http://localhost:4567/', 'foo')
    elif action == 'produce':
        DemoProducer.run(c, 'http://localhost:4567/', 'foo')
    else:
        raise ValueError(f'Unknown argument : {action}')


@task
def snapshots(c):
    c.run('pytest --snapshot-update')
