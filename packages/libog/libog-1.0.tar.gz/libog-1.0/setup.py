import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="libog",
    version="1.0",
    author="oliverbdot",
    author_email="author@example.com",
    description="A small library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/oliverbdot/stdog",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    package_dir={"": "libog"},
    packages=setuptools.find_packages(where="libog"),
    python_requires=">=3.6",
)
