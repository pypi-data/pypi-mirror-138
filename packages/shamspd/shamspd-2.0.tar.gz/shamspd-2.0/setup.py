from pathlib import Path
import setuptools
print("hi")

setuptools.setup(
    name="shamspd",
    version="2.0",
    long_description=Path("test/README.md").read_text(),
    packages=setuptools.find_packages(exclude=["test", "data"])
)
