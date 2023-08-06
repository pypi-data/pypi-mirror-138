import setuptools

with open("README.md", "r", encoding="utf-8", errors="ignore") as fh:
    long_description = fh.read()

setuptools.setup(
    name="new-DisUtils",
    version="1.3.7",
    author="DTS",
    description="DisUtils is a very useful library made to be used with pycord.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.github.com/DTS-11/DisUtils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">= 3.6",
    include_package_data=True,
    install_requires=["py-cord >= 1.7.3"],
    extras_require={"voice": ["py-cord[voice]", "youtube-dl"]}
)
