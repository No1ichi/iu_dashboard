from setuptools import setup, find_packages

setup(
    name="Dashboard",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "PyQt6>=6.4.2",
        "matplotlib>=3.7.0",
    ],
    python_requires=">=3.6,<=3.9",
)