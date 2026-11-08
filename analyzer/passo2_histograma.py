"""Passo 2 — Histograma: a distribuição de intensidade.

Objetivo: contar quantos pixels existem em cada nível de cinza (0 a 255)
e enxergar o formato dessa distribuição.

Como rodar (dentro da pasta analyzer):
    python passo2_histograma.py
"""

import cv2
import numpy as np
from pathlib import Path

BASE = Path(__file__).parent.parent
CAMINHO = BASE / "data" / "input" / "imagem3.jpg"


def main():
    img = cv2.imread(CAMINHO)
    if img is None:
        raise SystemExit(f"Não foi possível carregar: {CAMINHO}")

    # 1) Converta para escala de cinza.
    #    Dica: cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 2) Calcule o histograma com 256 caixas (uma por intensidade).
    #    Dica: np.histogram(gray.ravel(), bins=256, range=(0, 256))
    #    Ele devolve (contagens, bordas). Use só as contagens.
    contagens = np.histogram(gray.ravel(), bins=256, range=(0, 256))[0]

    # 3) Imprima: formato do gray, média e desvio padrão.
    #    Dica: gray.shape, gray.mean(), gray.std()
    # TODO
    print(gray.shape)
    print(gray.mean())
    print(gray.std())
    # 4) Descubra a intensidade que aparece mais e quantos pixels ela tem.
    #    Dica: np.argmax(contagens) devolve o ÍNDICE do maior valor
    mais_comum  = np.argmax(contagens)
    print(f"maior intensidade é {mais_comum}: {contagens[mais_comum]}")

    faixas = contagens.reshape(16, 16).sum(axis=1)
    maior = faixas.max()

    for i, valor in enumerate(faixas):
        inicio = i * 16
        barra = "#" * round(40 * valor / maior)
        print(f"{inicio:3d}-{inicio + 15:3d} {barra}")
    # 5) (Bônus) Desenhe um gráfico de barras em texto, com 16 faixas de 16 valores.
    #    Dica 1: contagens.reshape(16, 16).sum(axis=1) agrupa em 16 faixas
    #    Dica 2: para cada faixa, imprima "#" repetido proporcionalmente
    #            (use o maior valor das faixas como referência)
    # TODO


if __name__ == "__main__":
    main()
