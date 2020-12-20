from invoke import task

from demo.demo_consumer import DemoConsumer
from demo.demo_producer import DemoProducer


@task
def test(c):
    c.run('docker-compose up -d')
    c.run('python -m pytest -vv')
    c.run('docker-compose down')


@task
def dist(c):
    c.run('rm -rf dist/')
    c.run('pipenv-setup sync')
    c.run('python setup.py sdist bdist_wheel')


@task
def demo(c, action):
    if action == 'consume':
        DemoConsumer.run(c, 'http://localhost:4567/', 'foo')
    elif action == 'produce':
        DemoProducer.run(c, 'http://localhost:4567/', 'foo')
    else:
        raise ValueError(f'Unknown argument : {action}')
