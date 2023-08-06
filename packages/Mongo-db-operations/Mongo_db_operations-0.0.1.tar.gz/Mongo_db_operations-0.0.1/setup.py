from setuptools import setup, find_packages

setup(
    name="Mongo_db_operations",
    version="0.0.1",
    description="Mongo DB Operation",
    author="Harish Musti",
    download_url="https://github.com/hareshkm999/mongopi/archive/refs/tags/0.0.1.tar.gz",
    packages=find_packages(),
    install_requires=[
          'pymongo',
          'dnspython',
          'PyYAML',
          'pandas'],
    license="MIT"

)