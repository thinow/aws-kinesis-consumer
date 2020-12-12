from setuptools import setup, find_packages

VERSION = '1.0.1'

with open('README.md', 'r') as fh:
    long_description = fh.read()

if __name__ == '__main__':
    setup(
        name='aws-kinesis-consumer',
        description='Consume an AWS Kinesis Data Stream to look over the records from a terminal',
        long_description=long_description,
        long_description_content_type='text/markdown',
        author='Thierry Nowak',
        author_email='thinow@gmail.com',
        maintainer='Thierry Nowak',
        maintainer_email='thinow@gmail.com',
        version=VERSION,
        license='MIT',
        url='https://github.com/thinow/aws-kinesis-consumer',
        scripts=['cli/aws-kinesis-consumer'],
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
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Natural Language :: English',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3 :: Only',
            'Programming Language :: Python :: 3.10',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Topic :: Scientific/Engineering',
            'Topic :: Scientific/Engineering :: Information Analysis',
            'Topic :: Utilities',
        ],
    )
