from enum import Enum


class IteratorType(Enum):
    LATEST = 'latest'
    TRIM_HORIZON = 'trim-horizon'


class Configuration:

    def __init__(self, stream_name: str, iterator_type: IteratorType, endpoint=None, delay_in_ms=1_000):
        self.iterator_type = iterator_type
        self.stream_name = stream_name
        self.endpoint = endpoint
        self.delay_in_ms = delay_in_ms

    def __str__(self) -> str:
        return f'Configuration<stream_name={self.stream_name}>'
