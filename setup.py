"""Setup module of the package."""
import uuid

__author__ = 'Matthieu Gouel <matthieu.gouel@gmail.com>'
from setuptools import setup, find_packages
from pip.req import parse_requirements


INSTALL_REQS = parse_requirements('requirements.txt', session=uuid.uuid1())
REQS = [str(ir.req) for ir in INSTALL_REQS]

setup(
    name="api",
    packages=find_packages(),
    include_package_data=True,
    install_requires=REQS
)
