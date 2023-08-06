import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
PROJECT_NAME="perceptron_pypi"
USER_NMAE="dhires9196"

setuptools.setup(
    name=f"{PROJECT_NAME}-{USER_NMAE}",
    version="0.0.1",
    author="USER_NMAE",
    author_email="dhires9196@gmail.com",
    description="its a implementaion of perceptron",
    long_description=long_description,#it will use from README.md
    long_description_content_type="text/markdown",
    url=f"https://github.com/{USER_NMAE}/{PROJECT_NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/{USER_NMAE}/{PROJECT_NAME}/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=["numpy","tqdm"]
)