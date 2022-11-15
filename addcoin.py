import json
import os

while True:
    name = input("Enter coin name: ")
    symbol = input("Symbol ($USDC): ")
    addr   = input("Contract Address (0xB97...a6E): ")
    chainId = 137
    chainName = "Polygon"
    decimals = input("Decimals (18): ")
    
    tokens = {
        "tokenName": name,
        "tokenSymbol": symbol,
        "tokenDecimal": int(decimals),
        "contractAddress": addr,
        "chainId": int(chainId),
        "chainName": chainName,
        "native": False,
    }

    with open("./assets/json/tokens.json", "r") as file:
        emps = json.load(file)
        emps.append(tokens)
    jsonOb = json.dumps(emps, indent = 4)
    with open("./assets/json/tokens.json", "w") as file:
        file.write(jsonOb)