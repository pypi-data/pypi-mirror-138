import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hse-python-hw_1-avushakova",
    version="0.0.3",
    author="Alina Ushakova",
    author_email="spb.alina.ushakova@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AlinaUsh/HSE_Python",
    project_urls={
        "Bug Tracker": "https://github.com/AlinaUsh/HSE_Python/issues",
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
        "astunparse",
        "networkx",
        "matplotlib",
        "pydot>=1.2.4"
    ]
)