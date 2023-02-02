from setuptools import setup, find_packages

setup(
    name="mindflow",
    version="0.2.0",
    py_modules=["mindflow"],
    entry_points={"console_scripts": ["mf = mindflow.main:main"]},
    packages=find_packages(),
    install_requires=["requests", "pyperclip", "alive_progress", "simple_term_menu", "openai", "scikit-learn", "numpy", "cursor"],
)
