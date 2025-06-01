# Vending Machine

## Autor(a)

Pedro Afonso Guerra, A105133

## Resumo

Este TPC implementa uma aplicação para simular o funcionamento de uma máquina de _vending_. A máquina gere o stock de produtos, aceita moedas como forma de pagamento e permite que os utilizadores selecionem produtos para comprar. O estado da máquina é mantido entre execuções através do armazenamento de dados num ficheiro JSON.

## Descrição

A aplicação funciona como um sistema interativo baseado em comandos. O stock de produtos é carregado de um ficheiro JSON no arranque do programa e atualizado quando o programa termina. Os principais recursos incluem:

1. **Listagem de produtos**: Exibe todos os produtos disponíveis na máquina, com código, nome, quantidade e preço.
2. **Inserção de moedas**: O utilizador pode inserir moedas de diferentes valores para acumular saldo.
3. **Seleção de produtos**: O utilizador pode escolher um produto, desde que tenha saldo suficiente e haja stock disponível.
4. **Devolução de troco**: Ao sair, a máquina devolve o troco de forma otimizada.
5. **Persistência de dados**: O stock é armazenado e atualizado num ficheiro JSON para manter os dados entre execuções.
6. **Adição de produtos**: Permite a reposição do stock ou a adição de novos produtos através de comandos específicos.

## Resultados

**Exemplo de Interação:**
```
maq: 2024-03-08, Stock carregado, Estado atualizado.
maq: Bom dia. Estou disponível para atender o seu pedido.
>> LISTAR
maq:
cod | nome | quantidade | preço
---------------------------------
A23 | água 0.5L | 8 | 0.7€
...
>> MOEDA 1E, 20C, 5C, 5C
maq: Saldo = 1E30C
>> SELECIONAR A23
maq: Pode retirar o produto dispensado "água 0.5L"
maq: Saldo = 60C
>> SAIR
maq: Pode retirar o troco: 1x 50C, 1x 10C
maq: Até à próxima
```


