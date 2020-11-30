import typing
from enum import Enum


class IteratorTypeProperties:
    def __init__(self, argument: str, shard_filter_type: str, shard_iterator_type: str) -> None:
        self.argument = argument
        self.shard_filter_type = shard_filter_type
        self.shard_iterator_type = shard_iterator_type


class IteratorType(Enum):
    LATEST = IteratorTypeProperties(
        argument='latest',
        shard_filter_type='AT_LATEST',
        shard_iterator_type='LATEST',
    )
    TRIM_HORIZON = IteratorTypeProperties(
        argument='trim-horizon',
        shard_filter_type='AT_TRIM_HORIZON',
        shard_iterator_type='TRIM_HORIZON',
    )


class Configuration:

    def __init__(self,
                 stream_name: str,
                 iterator_type: IteratorType,
                 endpoint: typing.Optional[str],
                 delay_in_ms: int,
                 ):
        self.iterator_type = iterator_type
        self.stream_name = stream_name
        self.endpoint = endpoint
        self.delay_in_ms = delay_in_ms

    def __str__(self) -> str:
        return f'Configuration<stream_name={self.stream_name}>'
