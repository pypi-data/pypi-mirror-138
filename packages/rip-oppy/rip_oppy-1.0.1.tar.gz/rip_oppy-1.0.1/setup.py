import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
#README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="rip_oppy",
    version="1.0.1",
    description="Homage to the Mars Rover Opportunity",
    #long_description=README,
    #long_description_content_type="text/markdown",
    url="https://github.com/CoraDeFrancesco/hacklahoma_2022",
    author="Cora, Cosme, and Alex",
    author_email="coraanndefran@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["rip_oppy"],
    include_package_data=True,
    install_requires=["reverse_geocode", "numpy"],
    entry_points={
        "console_scripts": [
            "rip_oppy_comm=rip_oppy.__main__:main",
        ]
    },
)
