import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="aiy_prayer",
    version="1.0.0",
    description="AIY optimized Python command line tool that tells when the next Islamic prayer will occur.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Nabil-Lahssini/Google-AIY-prayer_assistant",
    author="Nabil Lahssini",
    author_email="NabilLahssini@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9"
    ],
    packages=["aiy_prayer"],
    install_requires=["prayer-tool", "pygame"],
    entry_points={
        "console_scripts": ['aiy_prayer=aiy_prayer.main:main']
    },
    include_package_data=True,
    package_data={'aiy_prayer': ['data/*.mp3']},
)