#!/usr/bin/env python3
from ply import lex

# List of token names
tokens = [
    'NUMBER',
    'STR',
    'ID',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LESS',
    'LESSEQ',
    'GREATER',
    'GREATEREQ',
    'DOUBLEEQ',
    'NEQ',
    'AND',
    'OR',
    'BANG',
    'SEMICOL',
    'PERIOD',
    'COMMA',
    'EQ',
    'LPAREN',
    'RPAREN',
    'LBRACK',
    'RBRACK',
    'LBRACE',
    'RBRACE',
    'PRINT',
    'COMM'
]

# Reserved words which should not match any IDs
reserved = {
    'class' : 'CLASS',
    'public' : 'PUBLIC',
    'private' : 'PRIVATE',
    'static' : 'STATIC',
    'extends' : 'EXTENDS',
    'void' : 'VOID',
    'int' : 'INT',
    'float' : 'FLOAT',
    'boolean' : 'BOOLEAN',
    'ArrayList' : 'ARRAYLIST',
    'HashMap' : 'HASHMAP',
    'main' : 'MAIN',
    'true' : 'TRUE',
    'false' : 'FALSE',
    'this' : 'THIS',
    'new' : 'NEW',
    'null' : 'NULL',
    'String' : 'STRING',
    'if' : 'IF',
    'else' : 'ELSE',
    'while' : 'WHILE',
    # for statement
    'for' : "FOR",
    # try catch statement
    'try' : "TRY",
    'catch' : "CATCH",
    'finally' : "FINALLY",
    'return' : 'RETURN',
    'Exception': 'EXCEPTION',
    'add' : 'ADD',
    'put' : 'PUT',
    'remove' : 'REMOVE',
    'clear' : 'CLEAR'
}

# Add reserved names to list of tokens
tokens += list(reserved.values())

# output format
# LexToken(token, target', line #, index)
class Scanner:
    # A string containing ignored characters (spaces and tabs)
    t_ignore = ' \t'

    # Regular expression rule with some action code
    
    # Math Operator
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'

    # compare operator
    t_LESS = r'\<'
    t_LESSEQ = r'\<='
    t_GREATER = r'\>'
    t_GREATEREQ = r'\>='
    t_DOUBLEEQ = r'\=='
    t_NEQ = r'\!='

    # logic operator
    t_AND = r'\&&'
    t_OR = r'\|\|'
    t_BANG = r'\!'
    
    # assignments 
    t_SEMICOL = r';'
    t_PERIOD = r'\.'
    t_COMMA = r','
    t_EQ = r'\='
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LBRACE = r'\{'
    t_RBRACE = r'\}'
    t_LBRACK = r'\['
    t_RBRACK = r'\]'

    # A regular expression rule with some action code
    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t
        
    def t_STR(self, t):
        r'"(?:[^"\\]|\\.)*"'
        return t

    def t_PRINT(self, t):
        r'System.out.println'
        return t

    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = reserved.get(t.value, 'ID') # Check for reserved words
        return t
    
    def t_COMM(self, t):
        r"//.*"
        return t
    
    # MISSING:
    # regex for INTARRAY, CHARARRAY, STRINGARRAY, BOOLEANARRAY

    # Define a rule so we can track line numbers. DO NOT MODIFY
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # Error handling rule. DO NOT MODIFY
    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Build the lexer. DO NOT MODIFY
    def build(self, **kwargs):
        self.tokens = tokens
        self.lexer = lex.lex(module=self, **kwargs)

    # Test the output. DO NOT MODIFY
    def test(self, data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print(tok)

# Main function. DO NOT MODIFY
if __name__=="__main__":

    f = open('example.java', 'r')
    data = f.read()
    f.close()

    scanner = Scanner()
    scanner.build()
    scanner.test(data)

