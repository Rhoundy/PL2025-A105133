# Analisador Léxico para Linguagem de Consulta Simples

## Autor

Pedro Afonso Guerra, A105133

## Resumo

Este programa em Python utiliza a biblioteca `ply.lex` para construir um analisador léxico para uma linguagem de consulta simples, semelhante a subconjuntos de SPARQL. Ele processa uma string de entrada contendo uma consulta e a divide numa sequência de tokens, identificando elementos como palavras-chave, variáveis, prefixos, strings, números e símbolos.

Os tokens reconhecidos incluem:
- **Palavras-chave:** `SELECT`, `WHERE`, `LIMIT`
- **Estruturais:** `VARIABLE` (ex: `?nome`), `PREFIX` (ex: `dbo:MusicalArtist`), `NAME` (ex: `a`), `STRING` (ex: `"Chuck Berry"@en`), `DOT` (`.`), `LBRACE` (`{`), `RBRACE` (`}`), `NUMBER` (ex: `1000`)
- **Outros:** `COMMENT` (linhas iniciadas por `#`, são ignoradas)

## Descrição

O objetivo principal deste script é demonstrar a construção de um analisador léxico usando a biblioteca `ply.lex` em Python. Um analisador léxico é o primeiro passo num compilador ou interpretador, responsável por converter uma sequência de caracteres num fluxo de tokens.

O processo de análise léxica neste script é definido da seguinte forma:
1.  **Definição de Tokens:** Uma lista `tokens` é definida contendo todos os possíveis tipos de tokens que o analisador pode reconhecer.
2.  **Regras de Tokenização:**
    *   **Tokens simples:** Para tokens com estruturas regulares simples (como `VARIABLE`, `STRING`, `DOT`, `LBRACE`, `RBRACE`), são usadas variáveis globais com expressões regulares (ex: `t_VARIABLE = r'\?[a-zA-Z_]\w*'`).
    *   **Tokens complexos e com prioridade:** Para tokens que requerem lógica mais elaborada ou para gerir a prioridade de correspondência (como `PREFIX`, `NUMBER`, `COMMENT`, e as palavras reservadas `SELECT`, `WHERE`, `LIMIT`), são definidas funções no formato `t_TOKENNAME(t)`. A ordem destas funções é importante para garantir que padrões mais específicos (ex: `PREFIX`, `SELECT`) sejam reconhecidos antes de padrões mais genéricos (ex: `NAME`).
    *   A regra `t_NAME` captura identificadores genéricos que não se encaixam noutras regras mais específicas.