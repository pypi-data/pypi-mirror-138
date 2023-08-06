import setuptools
from distutils.util import convert_path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

version = {}
ver_path = convert_path("classoptions/version.py")
with open(ver_path) as ver_file:
    exec(ver_file.read(), version)

setuptools.setup(
    name="classoptions",
    version=version["__version__"],
    author=version["__author__"],
    author_email="adrianmrit@gmail.com",
    description="Implement namespaced and inheritable metadata at the class level.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/adrianmrit/classoptions",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    package_dir={"classoptions": "classoptions"},
    packages=["classoptions"],
    python_requires=">=3.6",
)
