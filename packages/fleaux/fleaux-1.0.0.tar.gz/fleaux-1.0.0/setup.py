import pathlib
from setuptools import setup


HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="fleaux",
    version="1.0.0",
    description="setup up boilerplate code for python and c++",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Oliver G.",
    author_email="oliverbcontact@gmail.com",
    license="GNU",
    classifiers=[
        "Programming Language :: Python :: 3.9",
    ],
    packages=["fleaux"],
    include_package_data=True,
    install_requires=["libog",],
    entry_points={
        "console_scripts": [
            "fleaux=fleaux.__main__:main",
        ]
    },
)
