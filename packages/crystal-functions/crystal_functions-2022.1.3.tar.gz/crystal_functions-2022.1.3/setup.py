import setuptools

long_description = 'This repository contains functions to be used with the\
 <a href="https://www.crystal.unito.it/index.php">CRYSTAL code</a>.'

setuptools.setup(
    name="crystal_functions",
    version="2022.1.3",
    author="Bruno Camino",
    author_email="camino.bruno@gmail.com",
    description="Functions to be used with the CRYSTAL code.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/crystal-code-tools/crystal_functions",
    project_urls={
        "Bug Tracker": "https://github.com/crystal-code-tools/crystal_functions/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(include=['crystal_functions', 'crystal_functions.*']),
    python_requires=">=3.6",
    install_requires=[
        "numpy>=1.20.1",
        "requests",
        "ruamel.yaml>=0.15.6",
        "monty>=3.0.2",
        "scipy>=1.5.0",
        "tabulate",
        "spglib>=1.9.9.44",
        "networkx>=2.2",
        "matplotlib>=1.5",
        "palettable>=3.1.1",
        "sympy",
        "pandas",
        "plotly>=4.5.0",
        "uncertainties>=3.1.4",
        "Cython>=0.29.23",
        "pybtex",
        "tqdm",
	"pymatgen>=2022.2"
    ]
)
