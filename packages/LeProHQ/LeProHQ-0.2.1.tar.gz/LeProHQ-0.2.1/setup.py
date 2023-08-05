# -*- coding: utf-8 -*-
import pathlib

import packutil as pack
from setuptools import find_packages, setup

# write version on the fly - inspired by numpy
MAJOR = 0
MINOR = 2
MICRO = 1

repo_path = pathlib.Path(__file__).absolute().parent


def setup_package():
    # write version
    pack.versions.write_version_py(
        MAJOR,
        MINOR,
        MICRO,
        pack.versions.is_released(repo_path),
        filename="src/LeProHQ/version.py",
    )
    # paste Readme
    with open("README.md", "r") as fh:
        long_description = fh.read()
    # do it
    setup(
        name="LeProHQ",
        version=pack.versions.mkversion(MAJOR, MINOR, MICRO),
        description="(Un-)polarized Leptoproduction of Heavy Quarks",
        long_description=long_description,
        long_description_content_type="text/markdown",
        author="F. Hekhorn",
        author_email="felix.hekhorn@mi.infn.it",
        # url="https://github.com/N3PDF/yadism",
        # project_urls={
        #    "Documentation": "https://n3pdf.github.io/yadism/",
        #    "Changelog": "https://github.com/N3PDF/yadism/releases",
        #    "Issue Tracker": "https://github.com/N3PDF/yadism/issues",
        #    "Coverage": "https://codecov.io/gh/N3PDF/yadism",
        # },
        package_dir={"": "src"},
        packages=find_packages("src"),
        package_data={"LeProHQ": ["data/*/*.dat"]},
        zip_safe=False,
        classifiers=[
            "Operating System :: Unix",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Topic :: Scientific/Engineering",
            "Topic :: Scientific/Engineering :: Physics",
        ],
        install_requires=[
            "numpy",
            "numba",
            "scipy",
        ],
        python_requires=">=3.7",
    )


if __name__ == "__main__":
    setup_package()
