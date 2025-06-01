import ply.lex as lex

tokens = [
    'VARIABLE',
    'PREFIX',
    'NAME',
    'STRING',
    'DOT',
    'LBRACE',
    'RBRACE',
    'NUMBER',
    'COMMENT',
    'SELECT',
    'WHERE',
    'LIMIT',
]

t_VARIABLE = r'\?[a-zA-Z_]\w*'
t_STRING = r'\".*?\"(@[a-z]+)?'
t_DOT = r'\.'
t_LBRACE = r'\{'
t_RBRACE = r'\}'

t_ignore = ' \t\n'

def t_PREFIX(t):
    r'[a-zA-Z_]+:[a-zA-Z_]\w*'
    return t

def t_COMMENT(t):
    r'\#.*'
    pass

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_SELECT(t):
    r'select'
    return t

def t_WHERE(t):
    r'where'
    return t

def t_LIMIT(t):
    r'LIMIT'
    return t

def t_NAME(t):
    r'[a-zA-Z_]\w*'
    return t

def t_error(t):
    print(f"Caractere ilegal: '{t.value[0]}' na linha {t.lineno}, posição {t.lexpos}")
    t.lexer.skip(1)

lexer = lex.lex()

if __name__ == "__main__":
    data = '''
    # DBPedia: obras de Chuck Berry

    select ?nome ?desc where {
        ?s a dbo:MusicalArtist.
        ?s foaf:name "Chuck Berry"@en .
        ?w dbo:artist ?s.
        ?w foaf:name ?nome.
        ?w dbo:abstract ?desc
    } LIMIT 1000
    '''

    lexer.input(data)
    
    print("Resultado da análise léxica:")
    for tok in lexer:
        print(tok)