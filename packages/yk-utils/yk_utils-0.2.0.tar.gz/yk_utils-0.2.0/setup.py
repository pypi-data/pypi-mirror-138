from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="yk_utils",
    version="0.2.0",
    description="YooniK utils package for python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="YooniK",
    author_email="tech@yoonik.me",
    url="https://github.com/dev-yoonik/yk-utils-python",
    license='MIT',
    packages=[
        "yk_utils",
        "yk_utils.apis",
        "yk_utils.image",
        "yk_utils.files",
        "yk_utils.models"
    ],
    install_requires=[
        'requests',
        'beautifulsoup4',
        'six',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)