import setuptools

with open("README.md", "r", encoding="UTF-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jko_rotating_loggers",
    version="0.0.5",
    author="Roy Hung",
    author_email="roy.hung@jkos.com",
    description="A time rotating log",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
