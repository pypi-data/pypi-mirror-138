from setuptools import setup, find_packages

version = "0.0"

with open("README.md") as f:
    readme = f.read()

with open("requirements.txt") as f:
    requirements = [line.strip() for line in open("requirements.txt").readlines()]

setup(
    name="dds_cli",
    version=version,
    description="A command line tool to manage data and projects in the SciLifeLab Data Delivery System.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/ScilifelabDataCentre/dds_cli",
    author="SciLifeLab Data Centre",
    author_email="datacentre@scilifelab.se",
    license="MIT",
    packages=find_packages(exclude=("docs")),
    include_package_data=True,
    install_requires=requirements,
    setup_requires=["twine>=1.11.0", "setuptools>=38.6."],
    entry_points={
        "console_scripts": [
            "dds = dds_cli.__main__:dds_main",
        ],
    },
    zip_safe=False,
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 4 - Beta",
        # Indicate who your project is intended for
        "Intended Audience :: Science/Research",
        "Topic :: Software Development :: Build Tools",
        # Pick your license as you wish (should match "license" above)
        "License :: OSI Approved :: MIT License",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="data delivery research science scilifelab",
    python_requires=">=3.7",
)
