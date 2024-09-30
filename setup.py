from setuptools import setup

setup(
    name="blackparam",
    version="1.0.0",
    description="Tool to use the web archive to get all URLs",
    author="xzero",
    author_email="xzero@fbi.com",  
    url="https://github.com/sudo-xzero/blackparam",  
    packages=["blackparam"],
    install_requires=[
        "requests",
        "colorama",
        "beautifulsoup4",
    ],)
