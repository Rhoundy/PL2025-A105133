# Análise de um Dataset de Obras Musicais

## Autor

Pedro Afonso Guerra, A105133

## Resumo

Este programa em Python processa um dataset de obras musicais sem recorrer ao módulo `csv`. O programa extrai informações relevantes do ficheiro de entrada, incluindo a lista ordenada de compositores, a distribuição das obras por período e um dicionário com a lista de títulos ordenados alfabeticamente para cada período.

## Descrição

O objetivo deste projeto é processar um ficheiro CSV contendo informações sobre obras musicais. O programa realiza as seguintes tarefas:

1. Lê o ficheiro CSV sem utilizar o módulo `csv`, fazendo a separação manual dos campos com expressões regulares.
2. Extrai e ordena alfabeticamente a lista de compositores presentes no dataset.
3. Calcula a distribuição das obras por período, determinando quantas obras pertencem a cada período catalogado.
4. Cria um dicionário associando cada período à sua respetiva lista de títulos de obras, ordenada alfabeticamente.

A implementação garante a integridade dos dados, lidando com eventuais erros no ficheiro de entrada e assegurando que os resultados são gerados corretamente.

## Resultados

Os ficheiros relativos à resolução deste projeto estão disponíveis nos seguintes links: o ficheiro principal [tpc2.py](https://github.com/Rhoundy/PL2025-A105133/blob/main/TPC2/tpc2.py), bem como o ficheiro de entrada utilizado para testes [dataset.csv](https://github.com/Rhoundy/PL2025-A105133/blob/main/TPC2/dataset.csv).
