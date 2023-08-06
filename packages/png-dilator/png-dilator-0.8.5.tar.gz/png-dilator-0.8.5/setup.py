'''
Author: GT<caogtaa@gmail.com>
Date: 2021-05-07 12:05:41
LastEditors: Please set LastEditors
LastEditTime: 2022-02-15 09:50:59
'''
import pathlib
from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="png-dilator",
    version="0.8.5",
    description="Dilate texture with low alpha pixel to prevent \"black edge\" when rendered by GL",
    long_description=README,
    long_description_content_type="text/markdown",
    # url="https://github.com/caogtaa,
    author="GT",
    author_email="caogtaa@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=["pillow", "numpy", "fire"],
    entry_points={
        "console_scripts": [
            "dilator=dilator.__main__:main",
        ]
    },
)