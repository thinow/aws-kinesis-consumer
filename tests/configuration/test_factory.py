from aws_kinesis_consumer.configuration.factory import ConfigurationFactory


def test_stream_name():
    configuration = parse('--stream-name STREAM')
    assert configuration.stream_name == 'STREAM'


def test_endpoint():
    configuration = parse('--stream-name STREAM --endpoint ENDPOINT')
    assert configuration.endpoint == 'ENDPOINT'


def test_endpoint_defaults_to_none():
    configuration = parse('--stream-name STREAM')
    assert configuration.endpoint is None


def parse(arguments_as_str):
    factory = ConfigurationFactory()
    arguments_as_list = arguments_as_str.split(' ')
    return factory.create_configuration(arguments_as_list)
