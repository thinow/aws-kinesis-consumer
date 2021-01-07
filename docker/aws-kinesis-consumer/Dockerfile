FROM python:3.7.9-alpine3.12

LABEL maintainer="Thierry Nowak" \
      email="thinow@gmail.com" \
      description="aws-kinesis-consumer offers the ability to simply look up the records from a AWS Kinesis Data Stream (https://github.com/thinow/aws-kinesis-consumer)"

ENTRYPOINT ["pipenv", "run", "python", "-m", "aws_kinesis_consumer"]

WORKDIR /home

RUN pip install pipenv==2020.11.15

COPY Pipfile /home
COPY Pipfile.lock /home
COPY aws_kinesis_consumer /home/aws_kinesis_consumer

RUN pipenv sync