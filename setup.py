#
"""
"""
from setuptools import setup, find_packages

install_requires = [
    "httpretty>=0.8.0",
    "Jinja2==2.7.2",
]

setup(
    name='moogle',
    version='0.1',
    packages=find_packages(),
    install_requires=install_requires,
)
