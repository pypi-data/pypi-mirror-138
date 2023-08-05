# -*- coding: utf-8 -*-
import os

from setuptools import setup, find_packages


def read(filename):
    with open(filename, "r") as file_handle:
        return file_handle.read()


def get_version(version_tuple):
    if not isinstance(version_tuple[-1], int):
        return ".".join(map(str, version_tuple[:-1])) + version_tuple[-1]
    return ".".join(map(str, version_tuple))


init = os.path.join(os.path.dirname(__file__), "pydatafabric", "__init__.py")
version_line = list(filter(lambda l: l.startswith("VERSION"), open(init)))[0]

VERSION = get_version(eval(version_line.split("=")[-1]))
README = os.path.join(os.path.dirname(__file__), "README.md")

# Start dependencies group
emart = [
    "seaborn==0.11.2",
    "scipy==1.8.0",
    "implicit==0.5.2",
    "matplotlib==3.5.1",
    "openpyxl==3.0.9",
]

install_requires = [
    "thrift-sasl==0.4.3",
    "pyhive[hive]==0.6.4",
    "pyarrow==7.0.0",
    "pandas==1.4.0",
    "slackclient==2.9.3",
    "httplib2==0.20.4",
    "tabulate==0.8.9",
    "sqlalchemy==1.4.31",
    "packaging",
    "tqdm==4.62.3",
    "ipywidgets",
    "hmsclient-hive-3",
    "hvac",
    "redis",
    "click",
    "PyGithub",
    "pycryptodome",
    # Airflow Provider Google Reference: https://airflow.apache.org/docs/apache-airflow-providers-google/stable/index.html#pip-requirements
    "grpcio",
    "grpcio-gcp",
    "pandas_gbq<0.15.0",
    "google-api-python-client",
    "google-auth-httplib2",
    "google-cloud-core",
    "google-cloud-bigquery",
    "google-cloud-bigquery-datatransfer",
    "google-cloud-container",
    "google-cloud-datastore",
    "google-cloud-language",
    "google-cloud-storage",
    "google-cloud-spanner",
    "google-cloud-monitoring",
]

EXTRAS_REQUIRE = {
    "emart": emart,
}

setup(
    name="pydatafabric",
    version=VERSION,
    python_requires=">=3.8,<3.11",
    packages=find_packages("."),
    author="SHINSEGAE DataFabric",
    author_email="admin@shinsegae.ai",
    description="SHINSEGAE DataFabric Python Package",
    long_description=read(README),
    long_description_content_type="text/markdown",
    url="https://github.com/emartddt/dataplaltform-python-dist",
    install_requires=install_requires,
    extras_require=EXTRAS_REQUIRE,
    license="MIT License",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={"console_scripts": ["nes = pydatafabric.nes:nescli"]},
)
