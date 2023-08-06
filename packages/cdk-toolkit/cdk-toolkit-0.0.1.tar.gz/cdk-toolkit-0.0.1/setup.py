from setuptools import setup, find_packages

setup(
    name='cdk-toolkit',
    version='0.0.1',
    author='Ryan Moos',
    author_email='ryan@moos.engineering',
    packages=find_packages(),
    # scripts=['bin/script1','bin/script2'],
    url='http://pypi.python.org/pypi/cdk-toolkit/',
    license='LICENSE',
    description='AWS CDK Toolkit',
    long_description=open('README.md').read(),
    install_requires=[
        "aws-cdk-lib",
        "boto3",
    ],
)