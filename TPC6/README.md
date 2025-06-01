# Parser LL(1) Recursivo Descendente para Expressões Aritméticas

## Autor(a)

Pedro Afonso Guerra, A105133

## Resumo

Este programa é um parser LL(1) recursivo descendente em Python que analisa e calcula o valor de expressões aritméticas. Suporta números inteiros e de ponto flutuante, operadores `+`, `-`, `*`, `/`, parênteses `()` e menos unário, respeitando a precedência e associatividade padrão dos operadores.

## Descrição

O programa opera em duas etapas principais:

1.  **Análise Léxica (Tokenizer):** A string de entrada é convertida numa sequência de tokens (números, operadores, parênteses) por um lexer. Espaços são ignorados e caracteres inválidos geram erro.
2.  **Análise Sintática (Parser):** Um parser recursivo descendente processa os tokens. Funções dedicadas (`_expr`, `_term`, `_factor`) implementam as regras de uma gramática LL(1) para expressões aritméticas.
    *   A estrutura das chamadas entre estas funções garante a correta **precedência de operadores** (`*`, `/` antes de `+`, `-`).
    *   **Associatividade à esquerda** é tratada por loops internos.
    *   O **menos unário** é suportado.
    *   Durante a análise, o valor da expressão é calculado. Erros de sintaxe ou de execução (como divisão por zero) são detetados e reportados.

*NOTA:* O script executa exemplos pré-definidos. Para ver mais casos, para além dos definidos, temos de adicionar mais chamadas a `calculate_expression("EXPRESSAO")` para testar outras.

## Resultados

O resultado esperado da utilização deste programa, é:

*   **Para Expressões Válidas:**
    A expressão original e o seu valor numérico calculado.
    Exemplo:
    ```
    Expressão: "67-(2+3*4)"
    Resultado: 53.0
    ```

*   **Para Expressões Inválidas:**
    A expressão original e uma mensagem de erro.
    Exemplos:
    *   Erro Sintático:
        ```
        Expressão: "(2+3"
        Erro: Erro de Sintaxe: Esperado token RPAREN mas encontrou EOF...
        ```
    *   Erro de Execução (Divisão por Zero):
        ```
        Expressão: "10 / 0"
        Erro: Divisão por zero detectada.
        ```
    *   Multiplicação Implícita (não suportada):
        ` (9-2)(13-4)` causará erro; use `(9-2)*(13-4)`.

*   **Para Entrada Vazia:**
    Uma mensagem de erro a indicar que a entrada está vazia.