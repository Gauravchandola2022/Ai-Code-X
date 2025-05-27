import ply.lex as lex

# List of token names
tokens = [
    'ID', 'NUMBER',
    'PLUS', 'MINUS', 'MULT', 'DIVIDE',
    'ASSIGN', 'EQ', 'LT', 'GT',
    'LPAREN', 'RPAREN',
    'LBRACE', 'RBRACE',
    'SEMICOLON', 'COMMA', 'COLON',
    'STRING',
]

# Reserved words (keywords)
reserved = {
    'int': 'INT',
    'float': 'FLOAT',
    'char': 'CHAR',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'return': 'RETURN',
    'void': 'VOID',
}

# Merge reserved with tokens
tokens += list(reserved.values())

# Regular expressions for simple tokens
t_PLUS      = r'\+'
t_MINUS     = r'-'
t_MULT      = r'\*'
t_DIVIDE    = r'/'
t_ASSIGN    = r'='
t_EQ        = r'=='
t_LT        = r'<'
t_GT        = r'>'
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_LBRACE    = r'\{'
t_RBRACE    = r'\}'
t_SEMICOLON = r';'
t_COMMA     = r','
t_COLON     = r':'

# Strings in double quotes
def t_STRING(t):
    r'\".*?\"'
    t.value = t.value[1:-1]
    return t

# Identifier and keywords
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

# Numbers
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Ignored spaces/tabs
t_ignore = ' \t\r'

# Line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Error
def t_error(t):
    raise SyntaxError(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")

# Create the lexer
lexer = lex.lex()
