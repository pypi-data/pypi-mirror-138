import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SimSCSnTree",
    version="0.0.9",
    author="Xian Fan Mallory",
    author_email="xfan2@fsu.edu",
    description="Simulating single cell sequencing data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/compbiofan/SimSCSnTree",
    project_urls={
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        "numpy>=1.18.0",
        "anytree",
        "scipy==1.5.0",
    ],
)
