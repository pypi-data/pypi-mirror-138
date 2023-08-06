from setuptools import setup, find_packages

with open("requirements.txt", "r") as file:
    requirements = file.readlines()
    print(requirements)

long_description = "Opinionated generation of markdown files from json schemas"

setup(
    name="schema2md",
    version="0.0.6",
    author="ku222",
    author_email="kovid.uppal@gmail.com",
    url="https://github.com/ku222",
    description=long_description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.6",
    entry_points={"console_scripts": ["schema2md = schema2md.cli:main"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="json schema markdown",
    install_requires=requirements,
    zip_safe=False,
)
