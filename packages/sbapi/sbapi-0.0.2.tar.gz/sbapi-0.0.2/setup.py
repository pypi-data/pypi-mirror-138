from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.2'
DESCRIPTION = 'API Wrapper for Hypixel Skyblock.'

# Setting up
setup(
    name="sbapi",
    version=VERSION,
    author="carreb, drawbridge",
    author_email="<gabemackta@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['python', 'requests', 'api', 'hypixel', 'skyblock'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)