import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

#     packages=["otfcommon"], """


# This call to setup() does all the work
setup(
    name="otfpythonpkg",
    version="0.2.0",
    description="Provides common classes that will be shared between python applications",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/ronroyce22/otfpythonpkg.git",
    author="Ron Royce",
    author_email="rroycems@outlook.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=["feedparser", "html2text"],
    entry_points={
    },
)
