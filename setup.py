from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="safarireadinglist",
    version="0.1.0",
    author="Oliver K. Ernst",
    description="Safari reading list",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/smrfeld/safari-reading-list",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points = {
        'console_scripts': ['export-safari-rl=safarireadinglist.command_line:cli'],
    }
)