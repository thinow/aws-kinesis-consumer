from time import sleep

import boto3
from boto3_type_annotations.kinesis import Client as KinesisClient


class Application:
    arguments: list
    kinesis: KinesisClient

    def __init__(self, arguments: list) -> None:
        self.arguments = arguments

    def prepare(self):
        self.kinesis: KinesisClient = boto3.client('kinesis', endpoint_url="http://localhost:4567")
        print(f"Application running with the following arguments : {self.arguments}")

    def consume(self):
        print("<no records>")

    def wait_for_delay(self):
        # TODO adapt the time from the configuration
        sleep(1)  # in seconds
