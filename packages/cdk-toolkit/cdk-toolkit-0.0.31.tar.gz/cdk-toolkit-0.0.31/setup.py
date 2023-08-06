# https://python-packaging-tutorial.readthedocs.io/en/latest/setup_py.html

from setuptools import setup, find_packages

setup(
    name='cdk-toolkit',
    version='0.0.31',
    author='Ryan Moos',
    author_email='ryan@moos.engineering',
    packages=find_packages(),
    # scripts=['bin/script1','bin/script2'],
    url='http://pypi.python.org/pypi/cdk-toolkit/',
    license='LICENSE',
    description='AWS Cloud Development Toolkit',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    install_requires=[
        "aws-cdk-lib",
        "boto3",
    ],
)

