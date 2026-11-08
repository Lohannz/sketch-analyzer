"""Passo 8 — Consistência projetiva (proxy de coerência 3D).

As retas que ligam pares simétricos do corpo deveriam convergir para um
mesmo ponto de fuga. Medimos o quanto elas concordam.

Como rodar (dentro da pasta analyzer):
    python passo8_perspectiva.py
"""

import json
import math
from pathlib import Path

BASE = Path(__file__).parent.parent
ANOTACOES = BASE / "data" / "annotations"
NOME = "corpo_inteiro_b"

# pares simétricos: (nome da reta, ponto esquerdo, ponto direito)
PARES = [
    ("olhos", "olho_esq", "olho_dir"),
    ("ombros", "ombro_esq", "ombro_dir"),
    ("quadris", "quadril_esq", "quadril_dir"),
    ("joelhos", "joelho_esq", "joelho_dir"),
    ("tornozelos", "tornozelo_esq", "tornozelo_dir"),
]


def carregar(nome):
    with open(ANOTACOES / f"{nome}.json", encoding="utf-8") as f:
        return json.load(f)["pontos"]


def reta(p1, p2):
    """Retorna (a, b, c) da reta a*x + b*y + c = 0 que passa por p1 e p2."""
    (x1, y1), (x2, y2) = p1, p2
    a = y1 - y2
    b = x2 - x1
    c = x1 * y2 - x2 * y1
    return a, b, c


def distancia_reta(p, r):
    """Distância do ponto p até a reta r = (a, b, c)."""
    x, y = p
    a, b, c = r
    return abs(a * x + b * y + c) / math.hypot(a, b)


def ponto_de_fuga(retas):
    """Ponto que minimiza a soma dos quadrados das distâncias às retas.

    Resolve o sistema normal de mínimos quadrados:
        [Sa2 Sab] [x]   [-Sac]
        [Sab Sb2] [y] = [-Sbc]
    com cada reta normalizada.
    Retorna None se as retas forem paralelas (determinante ~ 0).
    """
    sa2 = sab = sb2 = sac = sbc = 0.0
    for a, b, c in retas:
        n = math.hypot(a, b)
        a, b, c = a / n, b / n, c / n
        sa2 += a * a
        sab += a * b
        sb2 += b * b
        sac += a * c
        sbc += b * c

    det = sa2 * sb2 - sab * sab
    if abs(det) < 1e-9:
        return None

    x = (sab * sbc - sb2 * sac) / det
    y = (sab * sac - sa2 * sbc) / det
    return x, y


def main():
    p = carregar(NOME)

    # 1) Monte a lista de retas a partir de PARES.
    #    Dica: para cada (nome, esq, dir), use reta(p[esq], p[dir])
    lista_retas = []
    nomes_retas = []
    
    for nome, esq, dir in PARES:
        r = reta(p[esq], p[dir])
        lista_retas.append(r)
        nomes_retas.append(nome)
   
    # Altura do personagem, para deixar o erro adimensional.
    altura = max(p["tornozelo_esq"][1], p["tornozelo_dir"][1]) - p["topo_cabeca"][1]

    # Passamos a lista de tuplas (a, b, c) para a função matemática
    vp = ponto_de_fuga(lista_retas)
    
    if vp is None:
        print("linhas paralelas -> construcao ortografica (ponto no infinito)")
        return 

    print(f"ponto de fuga: ({vp[0]:.1f}, {vp[1]:.1f})")

    residuos = []
    for nome, r in zip(nomes_retas, lista_retas):
        dist = distancia_reta(vp, r)
        residuos.append(dist)
        print(f" residuo reta {nome}: {dist:.2f} px")    

    RMS = math.sqrt(sum(r*r for r in residuos) / len(residuos))
    resultado = RMS / altura
    print(f"\nRMS: {RMS:.2f} px")
    print(f"Erro relativo (RMS / altura): {resultado:.4f}")
    
 
if __name__ == "__main__":
    main()
    
