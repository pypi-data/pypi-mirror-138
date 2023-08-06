import io
from setuptools import setup

requirements = [
    "pytodotxt>=1.2.1",
    "dateparser>=0.7.4",
    "click>=8.0.0",
    "prompt-toolkit>=3.0.5",
]

# Use the README.md content for the long description:
with io.open("README.md", encoding="utf-8") as fo:
    long_description = fo.read()

setup(
    name="full-todotxt",
    version="0.1.6",
    url="https://github.com/seanbreckenridge/full_todotxt",
    author="Sean Breckenridge",
    author_email="seanbrecke@gmail.com",
    description=(
        """todotxt interactive interface that forces you to specify attributes"""
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    test_suite="tests",
    install_requires=requirements,
    packages=["full_todotxt"],
    entry_points={"console_scripts": ["full_todotxt = full_todotxt.__main__:cli"]},
    keywords="todotxt todo.txt todo",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
