import sys

from pytest import CaptureFixture

from aws_kinesis_consumer.ui.printer import Printer
from aws_kinesis_consumer.ui.progress import Progress


def test_initial_progress_value(capsys: CaptureFixture):
    # when
    create_progress(3).print()

    # then
    force_end_of_capture()
    assert extract_final_output(capsys) == [
        '> TEXT 0/3'
    ]


def test_first_call_to_increment_and_print(capsys: CaptureFixture):
    # when
    create_progress(3).increment_and_print()

    # then
    force_end_of_capture()
    assert extract_final_output(capsys) == [
        '> TEXT 1/3'
    ]


def test_consecutive_calls_to_increment_and_print(capsys: CaptureFixture):
    # when
    progress = create_progress(3)
    progress.increment_and_print()
    progress.increment_and_print()

    # then
    force_end_of_capture()
    assert extract_final_output(capsys) == [
        '> TEXT 2/3',
    ]


def test_extra_calls_to_increment_and_print(capsys: CaptureFixture):
    # when
    progress = create_progress(3)
    progress.increment_and_print()
    progress.increment_and_print()
    progress.increment_and_print()
    progress.increment_and_print()  # 4 calls = one more call than max_value

    # then
    force_end_of_capture()
    assert extract_final_output(capsys) == [
        '> TEXT 3/3',
        '> TEXT 4/3',
    ]


def create_progress(max_value: int):
    return Progress('TEXT', max_value, Printer())


def force_end_of_capture():
    print('', file=sys.stdout)
    print('', file=sys.stderr)


def extract_final_output(capsys: CaptureFixture):
    captured = capsys.readouterr()
    return split_lines(captured.err)


def split_lines(output: str) -> list:
    lines = output.splitlines(keepends=True)
    lines = filter(lambda l: l.endswith('\n'), lines)  # filters out lines about to be replaced
    lines = map(lambda l: l.replace('\r', ''), lines)  # removes end-of-line character
    lines = map(lambda l: l.replace('\n', ''), lines)  # removes end-of-line character
    lines = filter(lambda l: len(l) != 0, lines)  # filters out empty lines
    return list(lines)
