from setuptools import find_packages, setup

# get version from mindflow/__init__.py
with open("mindflow/__init__.py", "r") as f:
    for line in f:
        if line.startswith("__version__"):
            version = line.split("=")[1].strip().strip('"')
            break

with open("requirements.txt", "r") as f:
    install_requires = f.read().strip().split("\n")

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="mindflow",
    python_requires=">=3.7.1",
    version=version,
    py_modules=["mindflow"],
    # entry_points={"console_scripts": ["mf = mindflow.main:main"]},
    entry_points={
        "console_scripts": [
            "mf = mindflow.cli.new_click_cli.cli_main:mindflow_cli",
            "mindflow = mindflow.cli.new_click_cli.cli_main:mindflow_cli",
        ],
    },
    packages=find_packages(),
    install_requires=install_requires,
    description="AI-powered search engine for your code!",
    long_description=long_description,
    long_description_content_type="text/markdown",
)
