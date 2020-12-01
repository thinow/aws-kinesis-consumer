from setuptools import setup, find_packages

VERSION = '1.0.0'

with open('README.md', 'r') as fh:
    long_description = fh.read()

if __name__ == '__main__':
    setup(
        name='aws-kinesis-consumer',
        url='https://github.com/thinow/aws-kinesis-consumer',
        version=VERSION,
        packages=find_packages(),
        install_requires=[
            'boto3==1.16.25',
            'boto3-type-annotations==0.3.1',
            'botocore==1.19.25',
            'jmespath==0.10.0',
            'python-dateutil==2.8.1',
            's3transfer==0.3.3',
            'urllib3==1.25.11',
        ],
        python_requires='>=3.6',
        scripts=['cli/aws-kinesis-consumer'],
        description='Simply look up the records from a AWS Kinesis Data Stream',
        long_description=long_description,
        long_description_content_type='text/markdown',
    )
