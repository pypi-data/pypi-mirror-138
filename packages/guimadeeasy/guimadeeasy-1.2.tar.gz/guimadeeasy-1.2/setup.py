from setuptools import setup, find_packages
from sys import exit, stderr
import os

try:
    import tkinter
except:
    print("tkinter not found.", file=stderr)
    if os.name == "posix":
        print('use "apt intall python3-tk" to install.')
    exit(1)

setup(
    name="guimadeeasy",
    version="1.2",
    description="this is just a fun challenge for my friend",
    packages=["guimadeeasy"],
    long_description="""

    This is my first package, I think these GUIs are super safe. Prove me wrong :->

    Examples - 

    >>> from guimadeeasy import *
    >>> clock()
    
    >>> from guidmadeasy import *
    >>> wheather()

    >>> from guimadeeasy import *
    >>> calculator()

    >>> from guimadeeasy import *
    >>> notepad()

    >>> from guimadeeasy import *
    >>> todo()

    >>> from guimadeeasy import *
    >>> snake()""",
)
