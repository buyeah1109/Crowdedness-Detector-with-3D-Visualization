from setuptools import setup, find_packages

setup(
    name="crowdcountmcnn",
    version="0.0.1",
    description="A crowd counting application",
    author="Lixun Zhang",
    author_email="lxzhang@gmail.com",
    packages=find_packages(),
    install_requires=[
        "numpy"
    ]
)