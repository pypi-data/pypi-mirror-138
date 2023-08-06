"""
Normalize according to selection of normalizers to use.
"""

from typing import Sequence, Dict
from functools import wraps
from .processors.registry import registry

# import the processor modules to register them
from .processors import converters
from .processors import removers
from .processors import validators


def process_term(processors:str, term:str):
   "transform a single term according to given transformer chain"

   for key in processors.split('|'):
      transform = registry[key]
      term = transform(term)

   return term


def process_terms(processors:str, terms:Sequence):
   "transform a sequence of terms according to transformer chain"

   for term in terms:
      if result := process_term(processors, term):
         yield result


def valid(processors):
   ""
   if set(processors.split('|')).issubset(registry.keys()):
      return True
   else:
      return False