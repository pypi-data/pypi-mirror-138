import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="autohyp",
    version="0.0.2",
    author="Gabriel Nager",
    author_email="gabenager@gmail.com.com",
    description="A simple hypothesis testing package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Gabriel-Aspen/autohyp",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)