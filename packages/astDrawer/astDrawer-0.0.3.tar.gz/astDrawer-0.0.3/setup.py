from setuptools import setup, find_packages

requirements = ["networkx>=2.0", "matplotlib>=3"]

setup(
    name="astDrawer",
    version="0.0.3",
    description="Draw image of ast of fibbonacci numbers code",
    packages=find_packages(),
    install_requires=requirements,
)
