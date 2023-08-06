"""
validator implementations.
"""
import re
from .registry import validator


find_letters = re.compile("[\w]+")

@validator("rl")
def require_letter_content(term):
   """see https://docs.python.org/3/library/re.html for what '\w' matches"""

   return term if re.match(find_letters, term) else False