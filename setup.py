from setuptools import setup, find_packages

AWS_KINESIS_CONSUMER_VERSION = "1.4.0"

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="aws-kinesis-consumer",
    description="Consume an AWS Kinesis Data Stream to look over the records from a terminal",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Thierry Nowak",
    author_email="thinow@gmail.com",
    maintainer="Thierry Nowak",
    maintainer_email="thinow@gmail.com",
    version=AWS_KINESIS_CONSUMER_VERSION,
    license="MIT",
    url="https://github.com/thinow/aws-kinesis-consumer",
    scripts=["cli/aws-kinesis-consumer"],
    packages=find_packages(),
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Utilities",
    ],
)
