from setuptools import setup
from setuptools import find_packages

with open("Readme.md", "r") as fh:
    long_description = fh.read()


setup(
    name='cotres',
    version="0.0.1",
    author="Mariusz Wozniak",
    author_email="mariusz.wozniak@cern.ch",
    description="Conductor Transient Response Simulator",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://gitlab.cern.ch/mawoznia/cotres",
    keywords={'Conductor', 'Transient', 'Response'},
    install_requires=["numpy"],
    extras_require={"dev": ["pandas", "matplotlib",],},
    python_requires='>=3.8',
    include_package_data=True,
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8"],

)
