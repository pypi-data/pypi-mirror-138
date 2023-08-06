"""
remover implementations.
"""

import re
from functools import wraps
from cleanco import basename
from .registry import remover


@remover("le")
def legal_entity_stripping(term):
   "use cleanco to remove legal entity abbreviations"
   return basename(term)

# regexps used in the following whitespace_removal transformer
ws_multi = re.compile(r"\ {2,}")
ws_dashes = re.compile(r"\ *-\ *")
ws_dots = re.compile(r"\ *\.\ *")

@remover("ws")
def whitespace_removal(term):
   "remove multiple whitespaces and whitespace around dashes or dots"
   term = re.sub(ws_multi, ' ', term)
   term = re.sub(ws_dashes,'-', term)
   term = re.sub(ws_dots,'.', term)
   return term

