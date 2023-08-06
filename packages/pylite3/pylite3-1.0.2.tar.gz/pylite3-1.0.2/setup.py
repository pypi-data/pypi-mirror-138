from setuptools import setup, find_packages

PACKAGE_NAME = "pylite3"
VERSION = "1.0.2"

classifiers=[
    "License :: OSI Approved :: MIT License",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: MacOS",
    "Operating System :: POSIX :: Linux",
    "Programming Language :: Python :: 3.8",
]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    license="MIT",
    classifiers=classifiers,
    url="https://github.com/nguyenvantat1182002/pylite3",
    author="nguyenvantat1182002",
    author_email="nguyenvantat1182002@gmail.com",
    packages=find_packages(),
)