import re

import pytest

from aws_kinesis_consumer.configuration.configuration import IteratorType
from aws_kinesis_consumer.configuration.factory import ConfigurationFactory


def test_help(capsys, snapshot):
    with pytest.raises(SystemExit):
        parse('--help')
    snapshot.assert_match(capsys.readouterr().out, 'ArgumentParserHelpOutput')


def test_version(capsys):
    with pytest.raises(SystemExit):
        parse('--version')

    version_pattern = re.compile(r'\d+\.\d+\.\d+')
    assert version_pattern.match(capsys.readouterr().out), "Output should be a valid version"


def test_stream_name():
    configuration = parse('--stream-name STREAM')
    assert configuration.stream_name == 'STREAM'


def test_stream_name_with_short_name_argument():
    configuration = parse('-s STREAM')
    assert configuration.stream_name == 'STREAM'


def test_stream_name_is_required():
    with pytest.raises(SystemExit) as error:
        parse('')
    assert str(error.value) == '2'


def test_max_records():
    configuration = parse('--stream-name STREAM --max-records-per-request 123')
    assert configuration.max_records_per_request == 123


def test_max_records_defaults_to_expected_value():
    configuration = parse('--stream-name STREAM')
    assert configuration.max_records_per_request is 10


def test_max_records_must_be_number(capsys, snapshot):
    with pytest.raises(SystemExit):
        parse('--stream-name STREAM --max-records-per-request NOT_A_NUMBER')

    snapshot.assert_match(capsys.readouterr().err, 'ArgumentParserMaxRecordsMustBeNumber')


def test_endpoint():
    configuration = parse('--stream-name STREAM --endpoint ENDPOINT')
    assert configuration.endpoint == 'ENDPOINT'


def test_endpoint_defaults_to_none():
    configuration = parse('--stream-name STREAM')
    assert configuration.endpoint is None


def test_region():
    configuration = parse('--stream-name STREAM --region eu-central-1')
    assert configuration.region == 'eu-central-1'


def test_region_defaults_to_none():
    configuration = parse('--stream-name STREAM')
    assert configuration.region is None


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
