from setuptools import find_packages, setup

setup(
    name="common-lib",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["pydantic-settings==2.10.1", "pymongo==4.14.1", "pyjwt==2.10.1", "bcrypt==4.3.0"],
)
