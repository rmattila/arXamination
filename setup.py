from setuptools import setup, find_packages

setup(
    name="arxamination",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        # Add your dependencies here
    ],
    entry_points={
        "console_scripts": [
            "arxamination = arxamination.main:main",
        ],
    },
)
