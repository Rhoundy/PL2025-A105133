import re
from collections import namedtuple

Token = namedtuple('Token', ['type', 'value'])

TOKEN_SPECIFICATION = [
    ('NUMBER',   r'\d+(\.\d*)?'),
    ('PLUS',     r'\+'),
    ('MINUS',    r'-'),
    ('MULTIPLY', r'\*'),
    ('DIVIDE',   r'/'),
    ('LPAREN',   r'\('),
    ('RPAREN',   r'\)'),
    ('SKIP',     r'[ \t]+'),
    ('MISMATCH', r'.'),
]

TOKEN_REGEX = re.compile('|'.join('(?P<%s>%s)' % pair for pair in TOKEN_SPECIFICATION))

class LexerError(Exception):
    """Erro durante a análise léxica."""
    pass

def tokenize(code_string):
    """Converte uma string em uma lista de tokens."""
    tokens = []
    for mo in TOKEN_REGEX.finditer(code_string):
        kind = mo.lastgroup
        value = mo.group()

        if kind == 'NUMBER':
            value = float(value) if '.' in value else int(value)
        elif kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise LexerError(f'Caractere inesperado: {value}')
        
        tokens.append(Token(kind, value))
    
    tokens.append(Token('EOF', None))
    return tokens

class ParserError(Exception):
    """Erro durante a análise sintática."""
    pass

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos]

    def _advance(self):
        """Avança o ponteiro de token."""
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = Token('EOF', None) 

    def _eat(self, token_type):
        """Consome o token atual se for do tipo esperado, senão levanta erro."""
        if self.current_token.type == token_type:
            token_value = self.current_token.value
            self._advance()
            return token_value
        else:
            raise ParserError(
                f"Erro de Sintaxe: Esperado token {token_type} mas encontrou {self.current_token.type} ('{self.current_token.value}') na posição {self.pos}"
            )

    def _factor(self):
        token = self.current_token
        if token.type == 'NUMBER':
            self._eat('NUMBER')
            return token.value
        elif token.type == 'LPAREN':
            self._eat('LPAREN')
            result = self._expr()
            self._eat('RPAREN')
            return result
        elif token.type == 'MINUS':
            self._eat('MINUS')

            return -self._factor() 
        else:
            raise ParserError(
                f"Erro de Sintaxe: Fator inválido. Esperado NUMBER, LPAREN ou MINUS unário, mas encontrou {token.type} ('{token.value}')"
            )

    def _term(self):
        node_value = self._factor()

        while self.current_token.type in ('MULTIPLY', 'DIVIDE'):
            op_token_type = self.current_token.type
            if op_token_type == 'MULTIPLY':
                self._eat('MULTIPLY')
                right_factor_value = self._factor()
                node_value *= right_factor_value
            elif op_token_type == 'DIVIDE':
                self._eat('DIVIDE')
                right_factor_value = self._factor()
                if right_factor_value == 0:
                    raise ZeroDivisionError("Divisão por zero detectada.")
                node_value /= right_factor_value
        return node_value

    def _expr(self):
        node_value = self._term()

        while self.current_token.type in ('PLUS', 'MINUS'):
            op_token_type = self.current_token.type
            if op_token_type == 'PLUS':
                self._eat('PLUS')
                right_term_value = self._term()
                node_value += right_term_value
            elif op_token_type == 'MINUS':
                self._eat('MINUS')
                right_term_value = self._term()
                node_value -= right_term_value
        return node_value

    def parse(self):
        """Método principal para iniciar o parsing."""
        if not self.tokens or self.tokens[0].type == 'EOF':
            raise ParserError("Não é possível analisar uma entrada vazia.")
        
        result = self._expr()
        
        if self.current_token.type != 'EOF':
            raise ParserError(
                f"Erro de Sintaxe: Token inesperado {self.current_token.type} ('{self.current_token.value}') após o fim da expressão."
            )
        return result

def calculate_expression(expression_string):
    print(f"Expressão: \"{expression_string}\"")
    try:
        tokens = tokenize(expression_string)
        parser = Parser(tokens)
        result = parser.parse()
        print(f"Resultado: {result}")
        return result
    except (LexerError, ParserError, ZeroDivisionError) as e:
        print(f"Erro: {e}")
        return None
    finally:
        print("-" * 30)

if __name__ == '__main__':
    calculate_expression("2+3")
    calculate_expression("10 - 4 + 2") # Teste de associatividade: (10-4)+2 = 8
    calculate_expression("67-(2+3*4)") # 67 - (2 + 12) = 67 - 14 = 53
    
    # O exemplo (9-2)(13-4) sugere multiplicação implícita.
    # Este parser requer operadores explícitos. Vamos usar (9-2)*(13-4).
    calculate_expression("(9-2)*(13-4)") # 7 * 9 = 63

    # Testando o exemplo "67-(2+34)" onde 34 é um número
    calculate_expression("67-(2+34)") # 67 - 36 = 31

    print("\n--- Testes Adicionais ---")
    calculate_expression("5")
    calculate_expression("-5")
    calculate_expression("--5") # -(-5) = 5
    calculate_expression("-(-5 + 2)") # -(-3) = 3
    calculate_expression("2 * 3 + 4")    # Precedência: (2*3)+4 = 10
    calculate_expression("2 + 3 * 4")    # Precedência: 2+(3*4) = 14
    calculate_expression("10 / 2 * 5")   # Associatividade: (10/2)*5 = 25
    calculate_expression("100 / (2 * 5)")# Parênteses: 100 / 10 = 10
    calculate_expression("((2+3)*4)-((5-1)/2)") # ((5)*4)-((4)/2) = 20 - 2 = 18
    calculate_expression("2.5 * 4")      # Números de ponto flutuante
    calculate_expression("7 / 2")        # Divisão resultando em float
    calculate_expression("3 * -2")       # Multiplicação com número negativo
    calculate_expression("3 * (-2)")     # Idem com parênteses

    print("\n--- Testes de Erro ---")
    calculate_expression("2+")           # Erro: fim inesperado
    calculate_expression("(2+3")         # Erro: falta parêntese de fecho
    calculate_expression("2 * / 3")      # Erro: operador inesperado
    calculate_expression("10 / 0")       # Erro: divisão por zero
    calculate_expression("abc")          # Erro: token inválido (LexerError)
    calculate_expression("5 5")          # Erro: token inesperado após expressão
    calculate_expression("(9-2)(13-4)")  # Erro: multiplicação implícita não suportada (o '(' é inesperado)
    calculate_expression("")             # Erro: entrada vazia
    calculate_expression("   ")          # Erro: entrada vazia (após ignorar espaços)