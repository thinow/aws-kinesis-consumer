import runpy

from setuptools import setup, find_packages

version_meta = runpy.run_path("./version.py")
VERSION = version_meta["__version__"]

with open("README.md", "r") as fh:
    long_description = fh.read()


def parse_requirements(filename):
    with open(filename) as file:
        lineiter = (line.strip() for line in file)
        return [line for line in lineiter if line and not line.startswith("#")]


if __name__ == "__main__":
    setup(
        name="aws-kinesis-consumer",
        version=VERSION,
        packages=find_packages(),
        install_requires=parse_requirements("requirements.txt"),
        python_requires=">=3.6.3",
        scripts=["scripts/cli.sh"],
        description="Simply look up the records from a AWS Kinesis Data Stream",
        long_description=long_description,
        long_description_content_type="text/markdown",
    )
