import invoke


class DemoConsumer:

    @classmethod
    def run(cls, runner: invoke.Runner, endpoint: str, stream_name: str):
        environment_vars = ' '.join([
            'AWS_SECRET_ACCESS_KEY=any',
            'AWS_ACCESS_KEY_ID=any',
        ])

        arguments = ' '.join([
            f'--endpoint {endpoint}',
            f'--stream-name {stream_name}',
            f'--region any-region',
        ])

        runner.run('docker-compose up -d')
        runner.run(f'{environment_vars} python -m aws_kinesis_consumer {arguments}')
