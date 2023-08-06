import setuptools

long_description = """
# QSARModelingPy

QSARModelingPy is an open-source computational package to generate and validate QSAR models.

**What you _can_ do with QSARModelingPy**

-   Select variables through either OPS or Genetic Algorithm
-   Dimensionality reduction:
    -   Correlation cut
    -   Variance cut
    -   Autocorrelation cut
-   Validate your models:
    -   Cross Validation
    -   y-randomization / Leave-N-out
    -   External Validation

## Usage
After installing this package with:
```
$ pip install qsarmodelingpy-gui
```
Just launch the application:
```
$ qsarmodelingpy
```
or:
```
$ python -m qsarmodelingpy-gui
```
"""

setuptools.setup(
    name="qsarmodelingpy-gui",
    version="0.2.4",
    author="Reis Filho, H. M.; Martins, J. P. A",
    author_email="helitonmrf@ufmg.br,jpam@qui.ufmg.br",
    description="A software for building and validating QSAR models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hellmrf/QSARModelingPyInterfaces",
    packages=["qsarmodelingpy_gui"],
    package_dir={"qsarmodelingpy_gui": "GUI"},
    package_data={"qsarmodelingpy_gui": ["Views/*.glade"]},
    install_requires=[
        'qsarmodelingpy>=0.3.0',
        'pygobject==3.30.5',
        'typing_extensions',
        'coloredlogs',
        'matplotlib',
        'tornado',
        'PyQt5',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'qsarmodelingpy = qsarmodelingpy_gui.main:main',
        ],
    },
    python_requires='>=3.6',
    license_files = ('LICENSE',),
)
