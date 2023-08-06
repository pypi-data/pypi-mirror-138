import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tdi-sdk",
    version="0.0.2",
    author="Denis Germano",
    author_email="dlcgermano@gmai.com",
    description="Simple SDK to use TDI services",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/denisgermano/tdi_sdk",
    project_urls={
        "Bug Tracker": "https://github.com/denisgermano/tdi_sdk/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
)