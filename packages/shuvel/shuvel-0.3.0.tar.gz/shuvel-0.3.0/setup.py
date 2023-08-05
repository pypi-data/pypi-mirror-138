import setuptools
from shuvel import __version__, PROG_DESC

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="shuvel",
    author="TheTwitchy",
    version=__version__,
    author_email="thetwitchy@thetwitchy.com",
    description=PROG_DESC,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/TheTwitchy/shuvel",
    license="MIT",
    license_files=("LICENSE",),
    packages=setuptools.find_packages(),
    install_requires=[
        "click",
        "rich"
    ],
    entry_points={
        "console_scripts": [
            "shuvel = shuvel.main:shuvel_cli",
        ],
    },
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
)
