from setuptools import setup, find_packages

setup(
    name="arxamination",
    version="0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "arxamination = main:main",
        ],
    },
)
