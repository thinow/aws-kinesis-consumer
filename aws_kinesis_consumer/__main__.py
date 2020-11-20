from aws_kinesis_consumer.stream_service import StreamService


def main():
    for stream_name in StreamService().get_names_of_streams():
        print(stream_name)


if __name__ == "__main__":
    main()
