import requests
import time
import random

print("⏳ Gerando planilha virtual com 100.000 linhas de estoque...")

linhas = []
cardapio = [
    "Frango com Batata Doce", 
    "Patinho com Mandioca", 
    "Escondidinho de Carne Seca", 
    "Lasanha de Berinjela",
    "Strogonoff de Frango"
]

# Gera 100 MIL registros simulando itens de uma carga pesada
for i in range(100000):
    linhas.append({
        "prato": random.choice(cardapio),
        "lote": f"LOTE-NUT-{i}",
        "quantidade": random.randint(10, 500)
    })

# Monta o pacote final
payload = {
    "codigo_rastreio": "CARGA-BR-100K",
    "motorista": "Caminhão Frigorífico 01",
    "filial_origem": "Leme-SP",
    "itens": linhas
}

print(f"📦 Pacote montado! Enviando {len(linhas)} itens para a API...")

# Marca o tempo exato do envio
inicio = time.time()

resposta = requests.post("http://127.0.0.1:8000/processar/", json=payload)

tempo_gasto = time.time() - inicio

if resposta.status_code == 202:
    dados = resposta.json()
    print("\n✅ SUCESSO ABSOLUTO!")
    print(f"A API processou, validou 100.000 linhas no Pydantic e jogou no Redis em: {tempo_gasto:.3f} segundos!")
    print(f"🔑 Task ID gerado: {dados['task_id']}")
else:
    print(f"❌ Falha: {resposta.status_code}")
    print(resposta.text)