from setuptools import setup, find_packages

setup(
    name="StudyDashboard",
    version="0.1.0",
    packages=find_packages(),            # src/ und ui/ werden so automatisch mit aufgenommen
    install_requires=[
        "PyQt6>=6.4.2",
        "matplotlib>=3.7.0",
    ],
    python_requires=">=3.6,<=3.9",        # erlaubt Python 3.6 bis 3.9
)