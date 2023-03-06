from setuptools import setup, find_packages


with open("requirements.txt", "r") as f:
    install_requires = f.read().strip().split("\n")

setup(
    name="mindflow",
    version="0.3",
    py_modules=["mindflow"],
    # entry_points={"console_scripts": ["mf = mindflow.main:main"]},
    entry_points={"console_scripts": ["mf = mindflow.cli.new_click_cli.cli_main:mindflow_cli"]},
    packages=find_packages(),
    install_requires=install_requires,
)
