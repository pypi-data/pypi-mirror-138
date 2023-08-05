import setuptools

setuptools.setup(
    name="toughastgen",
    version="0.0.5",
    author="Denis Tarasov",
    author_email="dt6cgsg@gmail.com",
    description="A small example package",
    long_description='A small example package',
    url="https://github.com/DT6A/HSE_Python",
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
        "astunparse==1.6.3",
        "networkx==2.6.3",
        "matplotlib",
        "pydot>=1.2.4"
    ]
)