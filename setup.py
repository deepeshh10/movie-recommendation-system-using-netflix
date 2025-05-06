from setuptools import setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

# Project configuration
REPO_NAME = "MovieMatch"
AUTHOR_USER_NAME = "ShonDsouza"
SRC_REPO = "src"
LIST_OF_REQUIREMENTS = ['flask', 'requests', 'numpy', 'pandas']


setup(
    name=REPO_NAME,
    version="1.0.0",
    author="Shon Dsouza & Deepesh",
    description="A modern movie recommendation system with machine learning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",  # You can add your GitHub URL here if you have one
    author_email="",  # You can add your email here if you want
    packages=[SRC_REPO],
    license="MIT",
    python_requires=">=3.7",
    install_requires=LIST_OF_REQUIREMENTS
)
