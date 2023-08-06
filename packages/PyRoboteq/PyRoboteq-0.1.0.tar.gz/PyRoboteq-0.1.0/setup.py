import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyRoboteq",
    version="0.1.0",
    author="Michael Pogodin",
    author_email="miker2808@gmail.com",
    description="Python library to ease with roboteq motor driver programming",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Miker2808/PyRoboteq",
    packages=setuptools.find_namespace_packages(where="PyRoboteq"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)