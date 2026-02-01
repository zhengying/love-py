"""
Setup script for love-api-py package.
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="love-api-py",
    version="11.5.0",
    author="LOVE2D Python Interface Project",
    author_email="",
    description="Complete LÖVE 2D game framework API documentation in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/love2d-community/love-api",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Games/Entertainment",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    keywords="love2d, love, game, framework, api, documentation, lua, gamedev",
    project_urls={
        "Bug Reports": "https://github.com/love2d-community/love-api/issues",
        "Source": "https://github.com/love2d-community/love-api",
        "LÖVE Homepage": "https://love2d.org/",
    },
)
