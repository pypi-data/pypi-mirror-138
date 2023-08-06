import setuptools


with open("README.md", "r") as f:
    long_description = f.read()

with open("requirements.txt", "r") as f:
    requirements = f.read().split()

setuptools.setup(
    name="edit_maker",
    version="0.0.1",
    author="Marker",
    description="Generating formatted edits for text",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    # py_modules=["edit_maker"],
    package_dir={"": "edit_maker/src"},
    install_requires=requirements,
)
