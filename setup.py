
import setuptools

from py_build import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py-build",
    version=__version__,
    author="Cory Laughlin",
    author_email="corylcomposinger@gmail.com",
    description="A package that can be used to create an installer program",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(exclude=('tests',)),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)