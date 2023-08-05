import setuptools


def load_long_description():
    with open("README.md", "r") as f:
        long_description = f.read()
    return long_description


# Start dependencies group
emart = [
    "seaborn>=0.11.0",
    "scipy>=1.8.0",
    "implicit>=0.5.0",
    "matplotlib>=3.5.0",
    "openpyxl>=3.0.0",
]

setuptools.setup(
    name="pydatafabric",
    version="0.1.2",
    author="SHINSEGAE DataFabric",
    author_email="admin@shinsegae.ai",
    description="SHINSEGAE DataFabric Python Package",
    long_description=load_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/emartddt/dataplaltform-python-dist",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8,<3.11",
    install_requires=[
        "thrift-sasl>=0.4.0",
        "hvac>=0.11.0",
        "pyhive[hive]>=0.6.4",
        "pyarrow>=7.0.0",
        "pandas>=1.4.0",
        "slackclient>=2.9.0",
        "httplib2>=0.20.0",
        "click",
        "PyGithub",
        "pycryptodome",
        "tabulate>=0.8.0",
        "pandas_gbq>=0.17.0",
        "google-cloud-bigquery>=2.32.0",
        "google-cloud-bigquery-storage>=2.11.0",
        "grpcio>=1.43.0",
        "sqlalchemy>=1.4.0",
        "packaging",
        "tqdm>=4.62.0",
        "ipywidgets",
        "hmsclient-hive-3",
        "google-cloud-monitoring>=2.8.0",
        "redis",
    ],
    extras_require={"emart": emart},
)
