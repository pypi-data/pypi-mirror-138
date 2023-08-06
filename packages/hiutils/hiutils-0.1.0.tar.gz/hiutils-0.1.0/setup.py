import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hiutils",
    version="0.1.0",
    author="Dan Bean",
    author_email="daniel.bean@kcl.ac.uk",
    description="Utilities for health informatics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dbeanm/hiutils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)