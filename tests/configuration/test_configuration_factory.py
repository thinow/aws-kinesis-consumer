import pytest

from aws_kinesis_consumer.configuration.configuration import IteratorType
from aws_kinesis_consumer.configuration.factory import ConfigurationFactory


def test_help(capsys, snapshot):
    with pytest.raises(SystemExit):
        parse('--help')
    snapshot.assert_match(capsys.readouterr().out, 'ArgumentParserHelpOutput')


def test_stream_name():
    configuration = parse('--stream-name STREAM')
    assert configuration.stream_name == 'STREAM'


def test_stream_name_is_required():
    with pytest.raises(SystemExit) as error:
        parse('')
    assert str(error.value) == '2'


def test_endpoint():
    configuration = parse('--stream-name STREAM --endpoint ENDPOINT')
    assert configuration.endpoint == 'ENDPOINT'


def test_endpoint_defaults_to_none():
    configuration = parse('--stream-name STREAM')
    assert configuration.endpoint is None


def test_iterator_type():
    configuration = parse('--stream-name STREAM --iterator-type trim-horizon')
    assert configuration.iterator_type == IteratorType.TRIM_HORIZON


def test_iterator_type_defaults_to_latest():
    configuration = parse('--stream-name STREAM')
    assert configuration.iterator_type == IteratorType.LATEST


def test_iterator_type_fails_on_unknown_values():
    with pytest.raises(SystemExit) as error:
        parse('--stream-name STREAM --iterator-type unknown')
    assert str(error.value) == '2'


def parse(arguments_as_str):
    factory = ConfigurationFactory()
    arguments_as_list = arguments_as_str.split(' ')
    return factory.create_configuration(arguments_as_list)
