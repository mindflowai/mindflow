from setuptools import setup, find_packages


with open("requirements.txt", "r") as f:
    install_requires = f.read().strip().split("\n")

setup(
    name="mindflow",
    version="0.2.11",
    py_modules=["mindflow"],
    entry_points={"console_scripts": ["mf = mindflow.main:main"]},
    packages=find_packages(),
    install_requires=install_requires,
)
