import os
import glob
import sys
from Plugin import Plugin

__all__ = [ os.path.basename(f)[:-3] for f in glob.glob(os.path.dirname(__file__)+"/*.py")]


sys.path.append("/Library/Frameworks/Python.framework/Versions/7.1/lib/python2.7/site-packages/tornado")
print sys.path