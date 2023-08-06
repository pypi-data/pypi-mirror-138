import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="abi-writer",
    version="1.0.0",
    author="Subhasish Goswami",
    author_email="subhasishgoswami00@gmail.com",
    description="Documentation for Solidity ABI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/subhasishgoswami/ABI-Documentation",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)