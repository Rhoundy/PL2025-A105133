import json
import re
from datetime import datetime

def carregar_stock(ficheiro):
    try:
        with open(ficheiro, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def guardar_stock(ficheiro, stock):
    with open(ficheiro, 'w', encoding='utf-8') as f:
        json.dump(stock, f, indent=4, ensure_ascii=False)

def listar_produtos(stock):
    print("cod | nome | quantidade | preço")
    print("-" * 40)
    for produto in stock:
        print(f"{produto['cod']} | {produto['nome']} | {produto['quant']} | {produto['preco']}€")

def inserir_moeda(saldo, entrada):
    valores = {"1E": 100, "50C": 50, "20C": 20, "10C": 10, "5C": 5, "2C": 2, "1C": 1}
    moedas = re.findall(r'\d+[EC]', entrada.upper())
    for moeda in moedas:
        if moeda in valores:
            saldo += valores[moeda]
    return saldo

def selecionar_produto(stock, codigo, saldo):
    for produto in stock:
        if produto["cod"] == codigo:
            if produto["quant"] > 0:
                if saldo >= int(produto["preco"] * 100):
                    produto["quant"] -= 1
                    saldo -= int(produto["preco"] * 100)
                    print(f"maq: Pode retirar o produto dispensado \"{produto['nome']}\"")
                else:
                    print(f"maq: Saldo insuficiente para satisfazer o seu pedido")
                    print(f"maq: Saldo = {saldo}c; Pedido = {int(produto['preco'] * 100)}c")
            else:
                print("maq: Produto esgotado")
            return saldo
    print("maq: Produto inexistente")
    return saldo

def calcular_troco(saldo):
    moedas = {"1E": 100, "50C": 50, "20C": 20, "10C": 10, "5C": 5, "2C": 2, "1C": 1}
    troco = {}
    for moeda, valor in moedas.items():
        if saldo >= valor:
            troco[moeda] = saldo // valor
            saldo %= valor
    return troco

def adicionar_produto(stock, entrada):
    match = re.match(r'ADICIONAR (\w+) "([^"]+)" (\d+) (\d+\.\d+)', entrada)
    if match:
        codigo, nome, quantidade, preco = match.groups()
        quantidade, preco = int(quantidade), float(preco)
        for produto in stock:
            if produto["cod"] == codigo:
                produto["quant"] += quantidade
                print("maq: Produto atualizado.")
                return
        stock.append({"cod": codigo, "nome": nome, "quant": quantidade, "preco": preco})
        print("maq: Produto adicionado.")
    else:
        print("maq: Comando inválido. Use: ADICIONAR <código> \"<nome>\" <quantidade> <preço>")

def main():
    ficheiro_stock = "stock.json"
    stock = carregar_stock(ficheiro_stock)
    saldo = 0
    print(f"maq: {datetime.today().strftime('%Y-%m-%d')}, Stock carregado, Estado atualizado.")
    print("maq: Bom dia. Estou disponível para atender o seu pedido.")
    
    while True:
        comando = input(">> ").strip().upper()
        if comando == "LISTAR":
            listar_produtos(stock)
        elif comando.startswith("MOEDA"):
            saldo = inserir_moeda(saldo, comando[6:])
            print(f"maq: Saldo = {saldo // 100}e{saldo % 100}c")
        elif comando.startswith("SELECIONAR"):
            codigo = comando.split()[1]
            saldo = selecionar_produto(stock, codigo, saldo)
            print(f"maq: Saldo = {saldo // 100}e{saldo % 100}c")
        elif comando.startswith("ADICIONAR"):
            adicionar_produto(stock, comando)
        elif comando == "SAIR":
            troco = calcular_troco(saldo)
            if troco:
                print("maq: Pode retirar o troco:", ", ".join([f"{v}x {k}" for k, v in troco.items()]))
            print("maq: Até à próxima")
            guardar_stock(ficheiro_stock, stock)
            break
        else:
            print("maq: Comando não reconhecido.")

if __name__ == "__main__":
    main()
