import setuptools

with open("src/README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="u2x",
    version="0.0.2",

    author="cvdnn",
    author_email="cvvdnn@gmail.com",

    keywords=("pip", "license", "image", "tool"),
    description="A python util package",
    long_description=long_description,
    long_description_content_type="text/markdown",

    url="https://github.com/xuebinqin/U-2-Net",
    project_urls={
        "Bug Tracker": "https://github.com/xuebinqin/U-2-Net/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),

    python_requires=">=3.6",
)
