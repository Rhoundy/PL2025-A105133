import ply.lex as lex

states = (
    ('pstarcomment', 'exclusive'),
)

tokens = (

    'PROGRAM', 'BEGIN', 'END', 'VAR',
    'INTEGER', 'REAL', 'BOOLEAN', 'STRING', 
    'IF', 'THEN', 'ELSE', 'FOR', 'TO', 'DOWNTO', 'DO', 'WHILE', 
    'WRITELN', 'READLN', 'FUNCTION', 'ARRAY', 'OF', 

    'DIV_OP', 'MOD_OP', 'AND_OP', 'OR_OP', 'NOT_OP',

    'ID',

    'NUMBER',
    'STRING_LITERAL',
    'TRUE_LITERAL',
    'FALSE_LITERAL',

    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',

    'EQ', 'NEQ', 'LT', 'LE', 'GT', 'GE',

    'ASSIGN', 'SEMICOLON', 'DOTDOT', 'DOT', 'COMMA', 'LPAREN', 'RPAREN',
    'COLON', 'LBRACKET', 'RBRACKET',
)

def t_PROGRAM(t):
    r'[Pp][Rr][Oo][Gg][Rr][Aa][Mm](?![a-zA-Z0-9_])'
    return t

def t_BEGIN(t):
    r'[Bb][Ee][Gg][Ii][Nn](?![a-zA-Z0-9_])'
    return t

def t_END(t):
    r'[Ee][Nn][Dd](?![a-zA-Z0-9_])'
    return t

def t_VAR(t):
    r'[Vv][Aa][Rr](?![a-zA-Z0-9_])'
    return t

def t_INTEGER(t):
    r'[Ii][Nn][Tt][Ee][Gg][Ee][Rr](?![a-zA-Z0-9_])'
    return t

def t_REAL(t):
    r'[Rr][Ee][Aa][Ll](?![a-zA-Z0-9_])'
    return t

def t_BOOLEAN(t):
    r'[Bb][Oo][Oo][Ll][Ee][Aa][Nn](?![a-zA-Z0-9_])'
    return t

def t_STRING(t):
    r'[Ss][Tt][Rr][Ii][Nn][Gg](?![a-zA-Z0-9_])'
    return t

def t_IF(t):
    r'[Ii][Ff](?![a-zA-Z0-9_])'
    return t

def t_THEN(t):
    r'[Tt][Hh][Ee][Nn](?![a-zA-Z0-9_])'
    return t

def t_ELSE(t):
    r'[Ee][Ll][Ss][Ee](?![a-zA-Z0-9_])'
    return t

def t_FOR(t):
    r'[Ff][Oo][Rr](?![a-zA-Z0-9_])'
    return t

def t_TO(t):
    r'[Tt][Oo](?![a-zA-Z0-9_])'
    return t

def t_DOWNTO(t):
    r'[Dd][Oo][Ww][Nn][Tt][Oo](?![a-zA-Z0-9_])'
    return t

def t_DO(t):
    r'[Dd][Oo](?![a-zA-Z0-9_])'
    return t

def t_WHILE(t):
    r'[Ww][Hh][Ii][Ll][Ee](?![a-zA-Z0-9_])'
    return t

def t_WRITELN(t):
    r'[Ww][Rr][Ii][Tt][Ee][Ll][Nn](?![a-zA-Z0-9_])'
    return t

def t_READLN(t):
    r'[Rr][Ee][Aa][Dd][Ll][Nn](?![a-zA-Z0-9_])'
    return t

def t_FUNCTION(t):
    r'[Ff][Uu][Nn][Cc][Tt][Ii][Oo][Nn](?![a-zA-Z0-9_])'
    return t

def t_ARRAY(t):
    r'[Aa][Rr][Rr][Aa][Yy](?![a-zA-Z0-9_])'
    return t

def t_OF(t):
    r'[Oo][Ff](?![a-zA-Z0-9_])'
    return t

def t_DIV_OP(t):
    r'[Dd][Ii][Vv]_[Oo][Pp]|[Dd][Ii][Vv](?![a-zA-Z0-9_])'
    t.type = 'DIV_OP'
    return t

def t_MOD_OP(t):
    r'[Mm][Oo][Dd]_[Oo][Pp]|[Mm][Oo][Dd](?![a-zA-Z0-9_])'
    t.type = 'MOD_OP'
    return t

def t_AND_OP(t):
    r'[Aa][Nn][Dd]_[Oo][Pp]|[Aa][Nn][Dd](?![a-zA-Z0-9_])'
    t.type = 'AND_OP'
    return t

def t_OR_OP(t):
    r'[Oo][Rr]_[Oo][Pp]|[Oo][Rr](?![a-zA-Z0-9_])'
    t.type = 'OR_OP'
    return t

def t_NOT_OP(t):
    r'[Nn][Oo][Tt]_[Oo][Pp]|[Nn][Oo][Tt](?![a-zA-Z0-9_])'
    t.type = 'NOT_OP'
    return t

def t_TRUE_LITERAL(t):
    r'[Tt][Rr][Uu][Ee]_[Ll][Ii][Tt][Ee][Rr][Aa][Ll]|[Tt][Rr][Uu][Ee](?![a-zA-Z0-9_])'
    t.type = 'TRUE_LITERAL'
    return t

def t_FALSE_LITERAL(t):
    r'[Ff][Aa][Ll][Ss][Ee]_[Ll][Ii][Tt][Ee][Rr][Aa][Ll]|[Ff][Aa][Ll][Ss][Ee](?![a-zA-Z0-9_])'
    t.type = 'FALSE_LITERAL'
    return t

def t_PSTAR_OPEN_INITIAL(t):
    r'\(\*'

    if not hasattr(t.lexer, 'comment_nesting_level'): 
        t.lexer.comment_nesting_level = 0
    t.lexer.comment_nesting_level += 1
    t.lexer.push_state('pstarcomment')

def t_BRACE_COMMENT(t):
    r'\{.*?\}'
    t.lexer.lineno += t.value.count('\n')
    pass

def t_DOTDOT(t):
    r'\.\.'
    return t

def t_DOT(t):
    r'\.'
    return t

t_ASSIGN = r':='
t_NEQ = r'<>'
t_LE = r'<='
t_GE = r'>='

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQ = r'='
t_LT = r'<'
t_GT = r'>'
t_SEMICOLON = r';'
t_COMMA = r','
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COLON = r':'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

def t_NUMBER(t):
    r'\d+(\.\d+([Ee][+-]?\d+)?)?|\d+[Ee][+-]?\d+|\.\d+([Ee][+-]?\d+)?'
    try:
        t.value = int(t.value)
    except ValueError:
        t.value = float(t.value)
    return t

def t_STRING_LITERAL(t):
    r"'([^']|'')*'"
    t.value = t.value[1:-1].replace("''", "'")
    return t

def t_pstarcomment_OPEN(t):
    r'\(\*'
    t.lexer.comment_nesting_level += 1

def t_pstarcomment_CLOSE(t):
    r'\*\)'
    t.lexer.comment_nesting_level -= 1

    if t.lexer.comment_nesting_level == 0:

        t.lexer.pop_state()

def t_pstarcomment_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_pstarcomment_CONTENT(t):
    r'([^*()\n]+|\((?!\*)|\*(?!\))|\n(?!\(\*|\*\)) )+'

    t.lexer.lineno += t.value.count('\n') 
    pass

def t_pstarcomment_error(t):

    t.lexer.skip(1) 

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def t_error(t):
    print(f"Erro Léxico (Estado INITIAL): Caractere ilegal '{t.value[0]}' na linha {t.lexer.lineno}")
    t.lexer.skip(1)

def t_eof(t):
    if t.lexer.current_state() == 'pstarcomment':
        print(f"Erro: Fim de arquivo inesperado dentro de um comentário (*...*) não fechado.")
        return None
    return None

lexer = lex.lex()

def test_lexer(data):
    lexer.input(data)
    print("--- Tokens Gerados ---")
    line_tokens = []
    current_line = 1
    while True:
        tok = lexer.token()
        if not tok:
            if line_tokens:
                print(f"Linha {current_line}: {' '.join(map(str,line_tokens))}")
            break
        if tok.lineno != current_line:
            if line_tokens:
                print(f"Linha {current_line}: {' '.join(map(str,line_tokens))}")
            line_tokens = []
            current_line = tok.lineno
        line_tokens.append(tok)

    print("----------------------")