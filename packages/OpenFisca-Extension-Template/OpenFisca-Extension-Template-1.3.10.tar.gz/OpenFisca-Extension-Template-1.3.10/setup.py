"""This file contains your extension package's metadata and dependencies."""

from pathlib import Path

from setuptools import find_packages, setup

# Read the contents of our README file for PyPi
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()  # pylint: disable=W1514

setup(
    name = "OpenFisca-Extension-Template",
    version = "1.3.10",
    author = "OpenFisca Team",
    author_email = "contact@openfisca.org",
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering :: Information Analysis",
        ],
    description = "An OpenFisca extension that adds some variables to an already-existing tax and benefit system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords = "benefit microsimulation social tax",
    license = "http://www.fsf.org/licensing/licenses/agpl-3.0.html",
    license_files = ("LICENSE",),
    url = "https://github.com/openfisca/extension-template",
    include_package_data = True,  # Will read MANIFEST.in
    data_files = [
        ("share/openfisca/openfisca-extension-template", ["CHANGELOG.md", "README.md"]),
        ],
    install_requires = [
        "OpenFisca-Country-Template >= 3.8.0,  < 4",
        ],
    extras_require = {
        "dev": [
            "autopep8 >= 1.5.4, < 2.0.0",
            "flake8 >= 3.8.0, < 4.0.0",
            "flake8-bugbear >= 20.1.0, < 22.0.0",
            "flake8-builtins >= 1.5.0, < 2.0.0",
            "flake8-coding >= 1.3.0, < 2.0.0",
            "flake8-commas >= 2.0.0, < 3.0.0",
            "flake8-comprehensions >= 3.2.0, < 4.0.0",
            "flake8-docstrings >= 1.5.0, < 2.0.0",
            "flake8-import-order >= 0.18.0, < 1.0.0",
            "flake8-print >= 3.1.0, < 5.0.0",
            "flake8-quotes >= 3.2.0, < 4.0.0",
            "flake8-simplify >= 0.9.0, < 1.0.0",
            "flake8-use-fstring >= 1.1.0, < 2.0.0",
            "pylint >= 2.6.0, < 3.0.0",
            "pycodestyle >= 2.6.0, < 3.0.0",
            ],
        },
    packages = find_packages(),
    )
