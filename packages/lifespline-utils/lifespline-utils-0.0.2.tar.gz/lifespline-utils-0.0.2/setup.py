"""Lifespline Utils Package Setup.
"""
from typing import List
from setuptools import setup, find_packages



with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

def _increment_version() -> str:
    """Increment project version.

    TODO: increment protocol

    Returns:
        str: [description]
    """    
    return '0.0.2'

def _get_install_reqs() -> List[str]:
    """Get dependencies for the lifespline-utils python package.

    TODO: add to setup(install_requires=_get_install_reqs())

    Returns:
        [str]: A list of dependencies for this package
    """
    # TODO: lifespline_utils.config.Config
    with open("requirements/main.md", mode="r", encoding="UTF-8") as deps:
        return list(deps)

setup(
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "",
        "Operating System :: OS Independent",
    ],
    # pip info
    name="lifespline-utils",
    version=_increment_version(),
    author="diogo",
    author_email="lifespline@fastmail.com",
    description="Lifespline Utils",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lifespline/lifespline-utils",
    # import info
    package_dir={"": "src"},
    packages=["lifespline_utils"],
)
