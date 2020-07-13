import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="yongshi-pyqtgameboard",
    version="0.1.0",
    author="Michael-Yongshi",
    author_email="4registration@outlook.com",
    description="A gameboard widget for pyqt gui's package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Michael-Yongshi/PyQtGameBoard",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)