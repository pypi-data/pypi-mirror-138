from setuptools import find_packages, setup

with open("README.md", "r") as cd:
    long_description = cd.read()

setup(
    name='dmongo',
    packages=find_packages(include=['dmongo']),
    version='0.1.0',
    description='A python library for communicating and Querying mongodb',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Geoffrey Israel',
    author_email="israelgeoffrey13@gmail.com",
    license='MIT',
    install_requires=['pymongo==3.12.1'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)
