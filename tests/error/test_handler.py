import pytest

from aws_kinesis_consumer import ErrorHandler

handler = ErrorHandler()


def test_unexpected_error(capsys):
    # when
    with pytest.raises(SystemExit) as raised_error:
        handler.handle(RuntimeError('Unexpected error'))

    # then
    output = capsys.readouterr()
    assert output.out.splitlines() == []
    assert output.err.splitlines() == [
        'ERROR: the program stopped due to the following issue.',
        'Unexpected error',
    ]

    assert isinstance(raised_error.value, SystemExit)
    assert raised_error.value.code == 1

# TODO test key interrupt
# TODO test NoRegionError
# TODO test AWS credentials error (not found, session expired, invalid key id, secret, session token)
# TODO test exit code
# TODO test any unknown exception
# TODO test successful --help
# TODO test erroneous --help
