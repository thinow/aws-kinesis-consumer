from invoke import task

from tasks_helper.demo.demo_consumer import DemoConsumer
from tasks_helper.demo.demo_producer import DemoProducer
from tasks_helper.packager.docker import DockerPackager
from tasks_helper.packager.pip import PipPackager

packagers: tuple = (
    PipPackager(),
    DockerPackager(),
)


@task
def test(c):
    c.run('docker-compose up -d')
    c.run('python -m pytest -vv')
    c.run('docker-compose down')


@task
def build(c):
    for packager in packagers:
        c.run(f'echo "--- Building for {packager.get_name()}"')
        packager.build(c)


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
