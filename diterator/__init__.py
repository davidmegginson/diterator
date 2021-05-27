import logging, sys

logger = logging.getLogger(__name__)


if sys.version_info < (3,):
    raise RuntimeError("diterator requires Python 3 or higher")

__version__="0.6"

from diterator.iterator import Iterator, XMLIterator

