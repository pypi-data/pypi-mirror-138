import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name="TeamStrange",
    version="1.0",
    author="Martin Clever",
    author_email="martin.clever@rwth-aachen.de",
    description="A small package for working with time series. Created by Team Strange.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.rwth-aachen.de/swc/teaching/winter-term-21-22/lab-timeseries-synthesizer/team-strange/-/tree/main",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    install_requires=['pandas'],
    packages=setuptools.find_packages(where="src"),

    python_requires=">=3.6",
)