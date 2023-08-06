import setuptools
from pathlib import Path

setuptools.setup(
    name="pypam3",
    version='0.0.2',
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["tests", "data", "venv"])
)
