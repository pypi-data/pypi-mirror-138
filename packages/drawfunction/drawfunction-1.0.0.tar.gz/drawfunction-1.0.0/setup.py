from setuptools import setup

setup(
    name="drawfunction",
    version="1.0.0",
    packages=['drawfunction'],
    url="https://github.com/andreyshspb/deep-python/tree/main/hw01",
    author='andreyshspb',
    author_email='andreyshspb@gmail.com',
    install_requires=[
        "networkx==2.6.3",
        "matplotlib==3.5.1",
        "pydot==1.4.2",
    ],
)
