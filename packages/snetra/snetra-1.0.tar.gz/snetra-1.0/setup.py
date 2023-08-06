import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='snetra',
    version='1.0',
    scripts=['snetra'] ,
    author="Eshan Singh",
    author_email="r0x4r@yahoo.com",
    description="A Python based scanner uses shodan-internetdb to scan the IP.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/R0X4R/snetra",
    packages=setuptools.find_packages(),
    install_requires=[
        'requests'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
