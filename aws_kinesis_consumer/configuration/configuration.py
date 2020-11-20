class Configuration:

    def __init__(self, stream_name: str, endpoint: str):
        self.stream_name = stream_name
        self.endpoint = endpoint

    def __str__(self) -> str:
        return f'Configuration<stream_name={self.stream_name}>'
