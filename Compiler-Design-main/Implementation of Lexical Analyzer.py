import re
from typing import NamedTuple, Iterable

# 1. Define the Token Structure
class Token(NamedTuple):
    type: str
    value: str
    line: int
    column: int

def tokenize(code: str) -> Iterable[Token]:
    # 2. Define Token Specifications (Regex Patterns)
    # The order matters! Specific patterns (keywords) must come before general ones (identifiers).
    token_specification = [
        ('NUMBER',   r'\d+'),             # Integer
        ('ASSIGN',   r'='),               # Assignment operator
        ('END',      r';'),               # Statement terminator
        ('ID',       r'[A-Za-z_]\w*'),    # Identifiers (vars)
        ('OP',       r'[+\-*/]'),         # Arithmetic operators
        ('LPAREN',   r'\('),              # (
        ('RPAREN',   r'\)'),              # )
        ('NEWLINE',  r'\n'),              # Line endings
        ('SKIP',     r'[ \t]+'),          # Skip over spaces and tabs
        ('MISMATCH', r'.'),               # Any other character
    ]

    # Combine into a single regex pattern using named groups: (?P<NAME>...)
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    
    # 3. Iterate over the input string
    line_num = 1
    line_start = 0
    
    # re.finditer finds all matches in the string
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start
        
        if kind == 'NUMBER':
            value = int(value) # Convert to integer
        elif kind == 'ID':
            # Check if the Identifier is actually a Keyword
            keywords = {'if', 'else', 'while', 'print'}
            if value in keywords:
                kind = value.upper() # e.g., 'if' becomes token type 'IF'
        elif kind == 'NEWLINE':
            line_start = mo.end()
            line_num += 1
            continue
        elif kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'{value!r} unexpected on line {line_num}')
        
        # Yield the token object
        yield Token(kind, value, line_num, column)

# --- Testing the Lexer ---

# Sample Source Code
source_code = """
x = 10;
if (x) {
    print x + 5;
}
"""

print(f"{'TYPE':<12} {'VALUE':<10} {'LOC':<10}")
print("-" * 35)

try:
    for token in tokenize(source_code):
        print(f"{token.type:<12} {str(token.value):<10} {token.line}:{token.column}")
except RuntimeError as e:
    print(f"Error: {e}")