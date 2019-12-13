from .base import *

# this will override the base.py
from .production import *

try:
    from .local import *
except:
    pass

