"""Passo 9 — Repetibilidade da marcação.

Compara duas anotações da MESMA imagem, feitas em momentos diferentes.
Isso mede o ruído do método: qualquer métrica futura precisa ser maior
que esse ruído para significar alguma coisa.

Como rodar (dentro da pasta analyzer):
    python passo9_repetibilidade.py
"""

import json
import math
from pathlib import Path

BASE = Path(__file__).parent.parent
ANOTACOES = BASE / "data" / "annotations"
NOME_A = "corpo_inteiro"
NOME_B = "corpo_inteiro_b"


def carregar(nome):
    with open(ANOTACOES / f"{nome}.json", encoding="utf-8") as f:
        return json.load(f)["pontos"]


def main():
    a = carregar(NOME_A)
    b = carregar(NOME_B)

    # 1) Para cada ponto, calcule a distância entre a marcação A e a B.
    #    Dica: math.dist(a[nome], b[nome])
    deslocamentos = {}
    for nome in a.keys():
        if nome in b:  # Garante que o ponto existe em ambas as anotações
            deslocamentos[nome] = math.dist(a[nome], b[nome])
    for nome, ponto in a.items():
        deslocamentos[nome] = math.dist(a[nome], b[nome])

    # 2) Imprima ponto a ponto, do maior para o menor.
    deslocamentos_ordenados = sorted(deslocamentos.items(), key=lambda item: item[1], reverse=True)
    
    print("--- Diferença Ponto a Ponto (Maior para Menor) ---")
    for nome, valor in deslocamentos_ordenados:
        print(f"Diferença {nome}: {valor:.2f} px")    # 3) Imprima média, máximo e o percentual em relação à altura do corpo.
    #    Altura: max(tornozelos em y) - topo em y
    # TODO


if __name__ == "__main__":
    main()
