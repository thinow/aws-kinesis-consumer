import pytest


class MockedKinesis(object):
    def foo(self):
        return 'foo'


@pytest.fixture
def mocked_kinesis() -> MockedKinesis:
    return MockedKinesis()


def test_consume_trim_horizon(mocked_kinesis: MockedKinesis):
    assert mocked_kinesis.foo() == 'foo'
