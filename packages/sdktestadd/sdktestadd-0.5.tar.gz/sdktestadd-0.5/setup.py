import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sdktestadd",
    version="0.5",
    author="YaShiko",
    author_email="m15339346028@163.com",
    description="SDK about postgres",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['pandas==1.4.1', 'numpy==1.22.1'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6"
)