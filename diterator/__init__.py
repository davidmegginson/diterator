import sys

if sys.version_info < (3,):
    raise RuntimeError("diterator requires Python 3 or higher")

__version__="0.3.1"

from diterator.iterator import Iterator, XMLIterator

