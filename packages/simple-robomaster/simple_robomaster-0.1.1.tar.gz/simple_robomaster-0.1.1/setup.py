import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simple_robomaster",
    version="0.1.1",
    author="Levon Gevorgyan",
    author_email="levongevdav@gmail.com",
    description="Simple Wrapper for Robot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/levon-gevorgyan/simple_robomaster",
    project_urls={
        "Bug Tracker": "https://github.com/levon-gevorgyan/simple_robomaster/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "robomaster>=0.1.1.65"
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)