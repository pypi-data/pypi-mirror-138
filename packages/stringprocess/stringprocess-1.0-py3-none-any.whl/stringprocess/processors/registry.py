"""
Provide global transformer registry and registration decorators.
"""

from typing import Dict, Callable, Union
from enum import Enum
from functools import wraps


class TYPES(Enum):
    "transformer types categorization"
    CONVERTER = 1
    REMOVER = 2
    VALIDATOR = 3


registry: Dict[str, Callable] = {}


def converter(registration_key:str):
   "outer args decorator"

   from stringprocess.processors.registry import registry

   def registrationdecorator(func):
      "the actual decorator"

      # register the converter
      registry[registration_key] = func

      @wraps(func)
      def transform(term:str):
         return func(term)

      return transform

   return registrationdecorator


def remover(registration_key:str):
   "outer args decorator"

   from stringprocess.processors.registry import registry

   def registrationdecorator(func):
      "the actual decorator"

      # register the remover
      registry[registration_key] = func

      @wraps(func)
      def transform(term:str):
         return func(term)

      return transform

   return registrationdecorator


def validator(registration_key:str):
   "outer args decorator"

   from stringprocess.processors.registry import registry

   def registrationdecorator(func):
      "the actual decorator"

      # register the remover
      registry[registration_key] = func

      @wraps(func)
      def transform(term:str):
         return func(term)

      return transform

   return registrationdecorator