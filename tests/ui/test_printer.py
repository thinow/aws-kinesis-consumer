from pytest import CaptureFixture

from aws_kinesis_consumer.ui.printer import Printer


def test_info(capsys: CaptureFixture):
    # when
    Printer().info('INFO TEXT')

    # then
    assert capsys.readouterr().err.splitlines() == [
        '> INFO TEXT',
    ]


def test_info_with_replaceable(capsys: CaptureFixture):
    # when
    Printer().info('FIRST', replaceable=True)
    Printer().info('SECOND', replaceable=True)
    Printer().info('THIRD', replaceable=False)

    # then
    assert capsys.readouterr().err.splitlines(keepends=True) == [
        '> FIRST\r',
        '> SECOND\r',
        '> THIRD\n',
    ]


def test_error(capsys: CaptureFixture):
    # when
    Printer().error('ERROR TEXT')

    # then
    assert capsys.readouterr().err.splitlines() == [
        '! ERROR TEXT',
    ]


def test_data(capsys: CaptureFixture):
    # when
    Printer().data(b'DATA TEXT')

    # then
    assert capsys.readouterr().out.splitlines() == [
        'DATA TEXT',
    ]
