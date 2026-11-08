"""Passo 7 — Métricas de proporção a partir dos pontos anotados.

Lê data/annotations/<nome>.json e calcula razões entre os pontos.

Como rodar (dentro da pasta analyzer):
    python passo7_proporcoes.py
"""

import json
import math
from pathlib import Path

BASE = Path(__file__).parent.parent
ANOTACOES = BASE / "data" / "annotations"
NOME = "corpo_inteiro"


def carregar(nome):
    with open(ANOTACOES / f"{nome}.json", encoding="utf-8") as f:
        return json.load(f)["pontos"]


def dist(a, b):
    return math.dist(a, b)


def media_y(*pontos):
    return sum(p[1] for p in pontos) / len(pontos)

def media_x(*pontos):
    return sum(p[0] for p in pontos) / len(pontos)

def main():
    p = carregar(NOME)

    # 1) Altura da cabeça: do topo ao queixo.
    altura_cabeca = dist(p['topo_cabeca'], p['queixo'])

    # 2) Altura total: do topo ao tornozelo mais baixo.
    #    dica: max(tornozelo_esq.y, tornozelo_dir.y)
    tornozelo_mais_baixo = p['tornozelo_esq'] if p['tornozelo_esq'][1] > p['tornozelo_dir'][1] else p['tornozelo_dir']
    altura_total = dist(p['topo_cabeca'], tornozelo_mais_baixo) 

    # 3) Número de cabeças.
    n_cabecas = altura_total/altura_cabeca

    # 4) Largura dos ombros (distância entre os dois ombros).
    largura_ombros = dist(p['ombro_esq'], p['ombro_dir'])

    # 5) Comprimento dos braços (ombro->cotovelo + cotovelo->punho).
    braco_esq = dist(p['ombro_esq'], p['cotovelo_esq']) + dist(p['cotovelo_esq'], p['punho_esq'])
    braco_dir = dist(p['ombro_dir'], p['cotovelo_dir']) + dist(p['cotovelo_dir'], p['punho_dir'])

    # 6) Altura do tronco: média do quadril menos média dos ombros.
    media_quadril_y = media_y(p["quadril_esq"], p["quadril_dir"])
    media_ombros_y = media_y(p["ombro_esq"], p["ombro_dir"])
    tronco = abs(media_quadril_y - media_ombros_y)
    
    y_topo = p['topo_cabeca'][1]
    y_queixo = p['queixo'][1]
    y_olhos = media_y(p['olho_esq'], p['olho_dir'])
    
    # Este número puro vai de 0.0 (topo) a 1.0 (queixo). O centro ideal é 0.50
    linha_olhos = (y_olhos - y_topo) / (y_queixo - y_topo)
    
    # 8) Simetria dos braços (ideal ≈ 1.0).
    simetria_braco = braco_dir / braco_esq

    print(f"altura da cabeca : {altura_cabeca:.1f} px")
    print(f"altura total     : {altura_total:.1f} px")
    print(f"n de cabecas     : {n_cabecas:.2f}")
    print(f"largura ombros   : {largura_ombros:.1f} px")
    print(f"ombros / cabeca  : {largura_ombros / altura_cabeca:.2f}")
    print(f"braco esq        : {braco_esq:.1f} px")
    print(f"braco dir        : {braco_dir:.1f} px")
    print(f"braco / tronco   : {braco_esq / tronco:.2f}")
    print(f"linha dos olhos  : {linha_olhos:.2f}") 
    print(f"simetria braco   : {simetria_braco:.3f}")


if __name__ == "__main__":
    main()
