from gettext import install
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

PKG_NAME="SimplePerceptron_package"
PROJECT_NAME = "SimplePerceptron-package"
USERNAME = "Ankit-Mehra"

setuptools.setup(
    name=f"{PKG_NAME}-{USERNAME}",
    version="0.0.3",
    author=USERNAME,
    author_email="ankitmehra1986@gmail.com",
    description="A small example package for perceptron",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/{USERNAME}/{PROJECT_NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/{USERNAME}/{PROJECT_NAME}/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requies = [
        "numpy==1.22.2",
        "pandas==1.4.0",
        "joblib==1.1.0"

    ]
)