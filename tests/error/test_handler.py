from pytest import CaptureFixture, raises

# TODO test NoRegionError
# TODO test AWS credentials error (not found, session expired, invalid key id, secret, session token)
# TODO test successful --help
# TODO test erroneous --help
from aws_kinesis_consumer import ErrorHandler


def test_unexpected_error(capsys: CaptureFixture):
    # when
    with raises(SystemExit) as raised_error:
        ErrorHandler.handle(RuntimeError('Unexpected error'))

    # then
    assert is_exit_program_error(raised_error)
    assert extract_output(capsys) == {
        'stdout': [],
        'stderr': [
            'ERROR: the program stopped due to the following issue.',
            'Unexpected error',
        ],
    }


def test_user_interrupting_program(capsys: CaptureFixture):
    # when
    ErrorHandler.handle(KeyboardInterrupt())

    # then
    assert extract_output(capsys) == {
        'stdout': [],
        'stderr': [],
    }


def is_exit_program_error(exception_info) -> bool:
    exception = exception_info.value
    return isinstance(exception, SystemExit) and exception.code == 1


def extract_output(capsys: CaptureFixture):
    captured = capsys.readouterr()
    return {
        'stdout': captured.out.splitlines(),
        'stderr': captured.err.splitlines(),
    }
