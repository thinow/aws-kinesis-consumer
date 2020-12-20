from invoke import task


@task
def test(c):
    c.run('docker-compose up -d')
    c.run('python -m pytest -vv')
    c.run('docker-compose down')


def demo_consume(c):
    environment_vars = ' '.join([
        'AWS_DEFAULT_REGION=any',
        'AWS_SECRET_ACCESS_KEY=any',
        'AWS_ACCESS_KEY_ID=any',
    ])

    arguments = ' '.join([
        '--endpoint http://localhost:4567/',
        '--stream-name foo',
    ])

    c.run('docker-compose up -d')
    c.run(f'{environment_vars} python -m aws_kinesis_consumer {arguments}')


def demo_produce(c):
    c.run('docker-compose up -d')
    c.run('python ./scripts/producer_dummy.py')


@task
def demo(c, action):
    if action == 'consume':
        demo_consume(c)
    elif action == 'produce':
        demo_produce(c)
    else:
        raise ValueError(f'Unknown argument : {action}')
