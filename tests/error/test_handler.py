from botocore.exceptions import NoRegionError, NoCredentialsError, PartialCredentialsError, ClientError
from pytest import CaptureFixture, raises

from aws_kinesis_consumer import ErrorHandler
from aws_kinesis_consumer.ui.printer import Printer


def test_user_interrupting_program(capsys: CaptureFixture):
    # when
    with raises(SystemExit) as raised_error:
        ErrorHandler(Printer()).handle(KeyboardInterrupt())

    # then
    assert program_exists(raised_error, expected_code=0)
    assert extract_output(capsys) == {
        'stdout': [],
        'stderr': [],
    }


def test_bypass_system_exit(capsys: CaptureFixture):
    # when
    with raises(SystemExit) as raised_error:
        ErrorHandler(Printer()).handle(SystemExit(123))

    # then
    assert program_exists(raised_error, expected_code=123)
    assert extract_output(capsys) == {
        'stdout': [],
        'stderr': [],
    }


def test_unexpected_error(capsys: CaptureFixture):
    # when
    with raises(SystemExit) as raised_error:
        ErrorHandler(Printer()).handle(RuntimeError('Unexpected error'))

    # then
    assert program_exists(raised_error, expected_code=1)
    assert extract_output(capsys) == {
        'stdout': [],
        'stderr': [
            "! ERROR: the program stopped due to the following issue.",
            "! RuntimeError('Unexpected error')",
        ],
    }


def test_missing_aws_region(capsys: CaptureFixture):
    # when
    with raises(SystemExit) as raised_error:
        ErrorHandler(Printer()).handle(NoRegionError())

    # then
    assert program_exists(raised_error, expected_code=1)
    assert extract_output(capsys) == {
        'stdout': [],
        'stderr': [
            "! ERROR: AWS region has not been found.",
            "! Please pass the region using the --region argument. Example:",
            "! $ aws-kinesis-consumer --stream-name MyStream --region us-east-1",
        ],
    }


def test_partially_missing_aws_credentials(capsys: CaptureFixture):
    # when
    with raises(SystemExit) as raised_error:
        ErrorHandler(Printer()).handle(PartialCredentialsError(
            provider='provider', cred_var='cred_var'
        ))

    # then
    assert program_exists(raised_error, expected_code=1)
    assert extract_output(capsys) == {
        'stdout': [],
        'stderr': [
            "! ERROR: AWS credentials have not been found.",
            "! Please pass the credentials using the following environment variables :",
            "! AWS_ACCESS_KEY_ID",
            "! AWS_SECRET_ACCESS_KEY",
            "! AWS_SESSION_TOKEN (optional)",
        ],
    }


def test_missing_aws_credentials(capsys: CaptureFixture):
    # when
    with raises(SystemExit) as raised_error:
        ErrorHandler(Printer()).handle(NoCredentialsError())

    # then
    assert program_exists(raised_error, expected_code=1)
    assert extract_output(capsys) == {
        'stdout': [],
        'stderr': [
            "! ERROR: AWS credentials have not been found.",
            "! Please pass the credentials using the following environment variables :",
            "! AWS_ACCESS_KEY_ID",
            "! AWS_SECRET_ACCESS_KEY",
            "! AWS_SESSION_TOKEN (optional)",
        ],
    }


def test_expired_aws_token(capsys: CaptureFixture):
    # when
    with raises(SystemExit) as raised_error:
        ErrorHandler(Printer()).handle(
            ClientError(operation_name='AnyAWSOperation', error_response={
                'Error': {
                    'Code': 'ExpiredTokenException'
                }
            })
        )

    # then
    assert program_exists(raised_error, expected_code=1)
    assert extract_output(capsys) == {
        'stdout': [],
        'stderr': [
            "! ERROR: AWS session token has expired.",
            "! Please refresh the AWS credentials.",
        ],
    }


def test_unknown_aws_client_error(capsys: CaptureFixture):
    # when
    with raises(SystemExit) as raised_error:
        ErrorHandler(Printer()).handle(
            ClientError(error_response={}, operation_name='AnyAWSOperation')
        )

    # then
    assert program_exists(raised_error, expected_code=1)
    assert extract_output(capsys) == {
        'stdout': [],
        'stderr': [
            "! ERROR: the program stopped due to the following issue.",
            "! ClientError('An error occurred (Unknown) when calling the AnyAWSOperation operation: Unknown')",
        ],
    }


def test_stream_not_found(capsys: CaptureFixture):
    # when
    with raises(SystemExit) as raised_error:
        ErrorHandler(Printer()).handle(
            ClientError(operation_name='AnyAWSOperation', error_response={
                'Error': {
                    'Code': 'ResourceNotFoundException',
                    'Message': 'OriginalErrorMessage',
                }
            })
        )

    # then
    assert program_exists(raised_error, expected_code=1)
    assert extract_output(capsys) == {
        'stdout': [],
        'stderr': [
            '! ERROR: the Kinesis Stream has not been found.',
            '! OriginalErrorMessage',
            '! Hint: verify the account id, the stream name, and the AWS region.'
        ],
    }


def program_exists(exception_info, expected_code) -> bool:
    exception = exception_info.value
    return isinstance(exception, SystemExit) and exception.code == expected_code


def extract_output(capsys: CaptureFixture):
    captured = capsys.readouterr()
    return {
        'stdout': captured.out.splitlines(),
        'stderr': captured.err.splitlines(),
    }
