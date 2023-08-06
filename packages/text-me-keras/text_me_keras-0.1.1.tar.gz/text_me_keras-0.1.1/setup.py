from setuptools import find_namespace_packages, setup
from pathlib import Path

from text_me_keras import __version__


root_directory = Path(__file__).parent
long_description = (root_directory / "README.md").read_text()


dev_pacakges = ["black==22.1.0", "isort==5.10.1", "pytest==5.2"]

setup(
    name="text_me_keras",
    version=__version__,
    author="Daniel John Varoli",
    author_email="daniel.varoli@gmail.com",
    description="A TenosorFlow callback that texts you back (to let you know how training is going).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/djvaroli/text_me_keras",
    packages=find_namespace_packages(".", include=["text_me_keras.*"]),
    package_dir={".": "text_me_keras"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=["tensorflow>=2.7.0", "twilio==7.6.0"],
)
