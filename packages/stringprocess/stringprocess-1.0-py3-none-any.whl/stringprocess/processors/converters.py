"""
transformer implementations.
"""

import re
from functools import wraps
from unidecode import unidecode
from .registry import converter

# Normalization options that can be enabled by including the first letter of
# the function in the normalization selector string.

@converter("lc")
def case_normalization(term):
   "normalize (to lower-) case"
   return term.lower()

@converter("as")
def diacritics_conversion(term):
   "remove diacritics, turning e.g. umlauts into ascii counterparts"
   return unidecode(term)
