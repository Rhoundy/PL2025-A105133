import ply.yacc as yacc
from lexer import tokens
from ast_nodes import *

precedence = (

    ('left', 'EQ', 'NEQ', 'LT', 'LE', 'GT', 'GE'),

    ('left', 'PLUS', 'MINUS', 'OR_OP'),

    ('left', 'TIMES', 'DIVIDE', 'DIV_OP', 'MOD_OP', 'AND_OP'),

    ('right', 'NOT_OP'),

    ('right', 'UMINUS'),
)

def p_program(p):
    'program : PROGRAM ID SEMICOLON block DOT'
    p[0] = ProgramNode(IDNode(p[2], p.lineno(2)), p[4])
    p[0].lineno = p.lineno(1) 

def p_block(p):
    '''block : declarations_opt compound_statement'''
    p[0] = BlockNode(p[1], p[2])

def p_declarations_opt(p):
    '''declarations_opt : declarations
                        | empty'''
    p[0] = p[1] if p[1] is not None else DeclarationsNode([]) 

def p_declarations(p):
    'declarations : declaration_item_list'
    p[0] = DeclarationsNode(p[1])

def p_declaration_item_list(p):
    '''declaration_item_list : declaration_item_list declaration_item
                             | declaration_item'''
    if len(p) == 3:

        if isinstance(p[2], list): 
            p[1].extend(p[2])
        else:
            p[1].append(p[2]) 
        p[0] = p[1]
    else:

        if isinstance(p[1], list):
            p[0] = p[1]
        else:
            p[0] = [p[1]] 

def p_declaration_item(p):
    '''declaration_item : var_declaration
                        | function_declaration'''
    p[0] = p[1] 

def p_var_declaration(p):
    '''var_declaration : VAR var_decl_list'''

    p[0] = p[2] 

def p_var_decl_list(p):
    '''var_decl_list : var_decl_list var_decl_item
                     | var_decl_item'''
    if len(p) == 3:
        p[1].append(p[2]) 
        p[0] = p[1]
    else:
        p[0] = [p[1]] 

def p_var_decl_item(p):
    '''var_decl_item : id_list COLON type_spec SEMICOLON'''

    p[0] = VarDeclNode(p[1], p[3])

    if p[1]:
        p[0].lineno = p[1][0].lineno
    else:
        p[0].lineno = p.lineno(2)

def p_id_list(p):
    '''id_list : id_list COMMA ID
               | ID'''
    if len(p) == 4:
        p[1].append(IDNode(p[3], p.lineno(3)))
        p[0] = p[1]
    else:
        p[0] = [IDNode(p[1], p.lineno(1))]

def p_type_spec(p):
    '''type_spec : INTEGER
                 | REAL
                 | BOOLEAN
                 | STRING
                 | ARRAY LBRACKET NUMBER DOTDOT NUMBER RBRACKET OF type_spec'''
    if len(p) == 2:
        p[0] = p[1].upper() 
    else:

        p[0] = {'type': 'ARRAY', 'low': p[3], 'high': p[5], 'of_type': p[8]}

def p_compound_statement(p):
    'compound_statement : BEGIN statement_list_opt END'
    p[0] = CompoundStatementNode(p[2])
    if p[2]:
        p[0].lineno = p.lineno(1) 
    else: 
        p[0].lineno = p.lineno(1)

def p_statement_list_opt(p):
    '''statement_list_opt : statement_list
                          | empty'''
    p[0] = p[1] if p[1] is not None else []

def p_statement_list(p):
    '''statement_list : statement_list SEMICOLON statement
                      | statement'''
    if len(p) == 4:
        if p[3] is not None: 
            p[1].append(p[3])
        p[0] = p[1]
    else:
        p[0] = [p[1]] if p[1] is not None else []

def p_statement(p):
    '''statement : assignment_statement
                 | procedure_call
                 | if_statement
                 | while_statement
                 | for_statement
                 | compound_statement
                 | empty'''
    p[0] = p[1]

def p_assignment_statement(p):
    'assignment_statement : var_access ASSIGN expr_bool'
    p[0] = AssignmentNode(p[1], p[3])
    p[0].lineno = p[1].lineno 

def p_var_access(p):
    '''var_access : ID
                  | ID LBRACKET expr_bool RBRACKET'''
    if len(p) == 2:
        p[0] = IDNode(p[1], p.lineno(1))
    else:
        p[0] = ArrayAccessNode(IDNode(p[1], p.lineno(1)), p[3])
        p[0].lineno = p.lineno(1) 

def p_readln_arg_list_opt(p):
    '''readln_arg_list_opt : readln_arg_list
                           | empty'''

    p[0] = p[1] if p[1] is not None else []

def p_readln_arg_list(p):
    '''readln_arg_list : readln_arg_list COMMA var_access
                       | var_access'''

    if len(p) == 4: 
        p[1].append(p[3]) 
        p[0] = p[1]
    else: 
        p[0] = [p[1]] 

def p_procedure_call(p):
    '''procedure_call : WRITELN LPAREN expr_list_opt RPAREN
                      | READLN LPAREN readln_arg_list_opt RPAREN 
                      | ID LPAREN expr_list_opt RPAREN'''
    call_name = p[1].lower()
    line_num = p.lineno(1)
    if call_name == 'writeln':
        p[0] = WriteLnCallNode(p[3])
    elif call_name == 'readln':

        p[0] = ReadLnCallNode(p[3])
    else:
        p[0] = FunctionCallNode(IDNode(p[1], line_num), p[3])
    p[0].lineno = line_num

def p_id_list_opt(p):
    '''id_list_opt : id_list
                   | empty'''
    p[0] = p[1] if p[1] is not None else []

def p_if_statement(p):
    '''if_statement : IF expr_bool THEN statement
                    | IF expr_bool THEN statement ELSE statement'''
    if len(p) == 5: 
        p[0] = IfStatementNode(p[2], p[4], None)
    else: 
        p[0] = IfStatementNode(p[2], p[4], p[6])
    p[0].lineno = p.lineno(1) 

def p_while_statement(p):
    'while_statement : WHILE expr_bool DO statement'
    p[0] = WhileStatementNode(p[2], p[4])
    p[0].lineno = p.lineno(1) 

def p_for_statement(p):
    '''for_statement : FOR assignment_statement TO expr_bool DO statement
                     | FOR assignment_statement DOWNTO expr_bool DO statement'''

    p[0] = ForStatementNode(p[2], p[3].upper(), p[4], p[6])
    p[0].lineno = p.lineno(1) 

def p_function_declaration(p):
    '''function_declaration : FUNCTION ID LPAREN parameter_list_opt RPAREN COLON type_spec SEMICOLON block SEMICOLON'''
    func_id_node = IDNode(p[2], p.lineno(2))
    params = p[4]  
    return_type = p[7] 
    block_node = p[9]
    p[0] = FunctionDeclarationNode(func_id_node, params, return_type, block_node)
    p[0].lineno = p.lineno(1) 

def p_parameter_list_opt(p):
    '''parameter_list_opt : parameter_list
                          | empty'''
    p[0] = p[1] if p[1] is not None else []

def p_parameter_list(p):
    '''parameter_list : parameter_list SEMICOLON parameter
                      | parameter'''
    if len(p) == 4:
        p[1].append(p[3]) 
        p[0] = p[1]
    else:
        p[0] = [p[1]] 

def p_parameter(p):
    'parameter : id_list COLON type_spec'

    p[0] = ParameterNode(p[1], p[3])
    if p[1]:
        p[0].lineno = p[1][0].lineno
    else:
        p[0].lineno = p.lineno(2)

def p_expr_bool(p):
    '''expr_bool : expression
                 | expression EQ expression
                 | expression NEQ expression
                 | expression LT expression
                 | expression LE expression
                 | expression GT expression
                 | expression GE expression'''
    if len(p) == 2:
        p[0] = p[1]  
    else:

        p[0] = BinOpNode(p[1], p.slice[2].type, p[3], p.lineno(2))

def p_expression(p):
    '''expression : term
                  | expression PLUS term
                  | expression MINUS term
                  | expression OR_OP term'''
    if len(p) == 2:
        p[0] = p[1] 
    else:

        p[0] = BinOpNode(p[1], p.slice[2].type, p[3], p.lineno(2))

def p_term(p):
    '''term : factor
            | term TIMES factor
            | term DIVIDE factor     
            | term DIV_OP factor      
            | term MOD_OP factor
            | term AND_OP factor'''
    if len(p) == 2:
        p[0] = p[1] 
    else:

        p[0] = BinOpNode(p[1], p.slice[2].type, p[3], p.lineno(2))

def p_factor(p):
    '''factor : NUMBER
              | STRING_LITERAL
              | TRUE_LITERAL
              | FALSE_LITERAL
              | var_access
              | LPAREN expr_bool RPAREN
              | ID LPAREN expr_list_opt RPAREN
              | NOT_OP factor
              | MINUS factor %prec UMINUS'''  # %prec UMINUS para menos unário
    if len(p) == 2:
        if isinstance(p[1], Node): 
            p[0] = p[1]
        elif isinstance(p[1], (int, float)):
            p[0] = NumberNode(p[1], p.lineno(1))
        elif p.slice[1].type == 'STRING_LITERAL':
            p[0] = StringLiteralNode(p[1], p.lineno(1))
        elif p.slice[1].type == 'TRUE_LITERAL':
            p[0] = IDNode('TRUE', p.lineno(1)) 
        elif p.slice[1].type == 'FALSE_LITERAL':
            p[0] = IDNode('FALSE', p.lineno(1)) 
    elif p[1] == '(': 
        p[0] = p[2] 
    elif p.slice[1].type == 'ID' and p[2] == '(': 
        p[0] = FunctionCallNode(IDNode(p[1], p.lineno(1)), p[3])
        p[0].lineno = p.lineno(1)
    elif len(p) == 3: 
        op_token = p.slice[1].type 
        p[0] = UnaryOpNode(op_token, p[2], p.lineno(1))

def p_expr_list_opt(p):
    '''expr_list_opt : expr_list
                     | empty'''
    p[0] = p[1] if p[1] is not None else []

def p_expr_list(p):
    '''expr_list : expr_list COMMA expr_bool
                 | expr_bool'''
    if len(p) == 4: 
        if p[3] is not None: 
            p[1].append(p[3])
        p[0] = p[1]
    else: 
        p[0] = [p[1]] if p[1] is not None else []

def p_empty(p):
    'empty :'
    p[0] = None 

def p_error(p):
    if p:
        print(f"Erro de Sintaxe: Token '{p.value}' (Tipo: {p.type}) inesperado na linha {p.lineno}")

    else:
        print("Erro de Sintaxe: Fim de arquivo inesperado (EOF) ou erro irrecuperável.")

parser = yacc.yacc()