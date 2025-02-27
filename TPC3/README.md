# Conversor de Markdown para HTML

## Autor

Pedro Afonso Guerra, A105133

## Resumo

Este programa em Python lê um ficheiro de texto em formato Markdown e converte-o para HTML. Suporta a conversão dos seguintes elementos:
- **Cabeçalhos** (`#`, `##`, `###`) → `<h1>`, `<h2>`, `<h3>`
- **Texto em negrito** (`**texto**`) → `<b>texto</b>`
- **Texto em itálico** (`*texto*`) → `<i>texto</i>`
- **Listas numeradas** (`1. item`) → `<ol><li>item</li></ol>`
- **Links** (`[texto](url)`) → `<a href="url">texto</a>`
- **Imagens** (`![alt](url)`) → `<img src="url" alt="alt"/>`

## Descrição

O objetivo deste projeto é criar um pequeno conversor de Markdown para HTML, capaz de interpretar e converter os elementos básicos descritos na "Basic Syntax" da cheat sheet de Markdown. O programa lê um ficheiro Markdown, processa os elementos através de expressões regulares e gera um ficheiro HTML correspondente.

A conversão é feita através das seguintes funções:
- `title_to_header(match)`: Converte cabeçalhos Markdown (`#`, `##`, `###`) para `<h1>`, `<h2>`, `<h3>`.
- `list_to_html(match)`: Converte listas numeradas para `<ol><li>...</li></ol>`.
- `image_to_html(match)`: Converte imagens no formato `![texto alternativo](url)` para `<img src="url" alt="texto alternativo"/>`.
- `link_to_html(match)`: Converte links `[texto](url)` para `<a href="url">texto</a>`.
- `markdown_to_html(file)`: Lê um ficheiro Markdown e aplica todas as conversões.

O código foi desenvolvido para ser robusto e evitar conversões incorretas, garantindo que os elementos Markdown são corretamente transformados para HTML.

## Utilização

Para executar o script, usa o seguinte comando no terminal:

```sh
python3 mk-html.py ficheiro.md
