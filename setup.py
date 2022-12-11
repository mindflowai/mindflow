"""
Setup script for mindflow
"""
from setuptools import setup

setup(
    name="mindflow",
    version="0.1",
    py_modules=["mindflow"],
    entry_points={"console_scripts": ["mf = main:main"]},
    install_requires=["requests", "revChatGPT", "bs4", "chardet", "pyperclip", "gitpython"],
)
