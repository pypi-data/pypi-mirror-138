import os
from setuptools import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


PROJECT_NAME = "ast_drawer_ses"

setup(
    name=PROJECT_NAME,
    version="0.0.4",
    author="Egor Sheremetov",
    author_email="egor.sheremetov@yandex.ru",
    description="Simple project that lets tou draw an AST",
    license="BSD",
    keywords="ast render",
    url=f'http://packages.python.org/{PROJECT_NAME}',
    packages=[PROJECT_NAME],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
