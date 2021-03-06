from invoke import task

from tasks_helper.assert_no_todos.assert_no_todos import assert_no_todos
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
        print(f'--- Building for {packager.get_name()}')
        packager.build(c)


@task
def deploy(c, destination):
    for packager in packagers:
        print(f'--- Deploying for {packager.get_name()}')
        packager.deploy(c, destination)


@task
def demo(c, action):
    if action == 'consume':
        DemoConsumer.run(c, 'http://localhost:4567/', 'foo')
    elif action == 'produce':
        DemoProducer.run(c, 'http://localhost:4567/', 'foo')
    else:
        raise ValueError(f'Unknown argument : {action}')


@task
def assertnotodos(c):
    assert_no_todos()


@task
def snapshots(c):
    c.run('pytest --snapshot-update')
