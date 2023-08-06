from setuptools import setup

requirements = [
    "yaml",
]

with open("README.md") as f:
    long_description = f.read()

setup(
    name="oeven",
    pymodules=["oeven"],
    package_dir = {'': 'oeven'},
    version="0.0.10",
    description="Command line interface for managing your tasks inside terminal.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=requirements,
    python_requires=">=3",
    entry_points={"console_scripts": ["oeven = oeven.oeven:main"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    author="Joaco Monsalvo",
    author_email="jmonsalvo.contact@protonmail.com",
    url="https://github.com/joacomonsalvo/oeven",
)