"""Passo 1 — Ler uma imagem e entender a matriz.

Objetivo: carregar o desenho, confirmar que carregou e inspecionar a matriz.

Como rodar (no terminal, dentro da pasta analyzer):
    python passo1_ler.py
"""

import cv2
from pathlib import Path

BASE = Path(__file__).parent.parent          # pasta TCC
CAMINHO = BASE / "data" / "input" / "imagem4.png"


def main():
    # 1) Carregue a imagem em BGR.
    #    Dica: cv2.imread
    img = cv2.imread(CAMINHO)
    if img is None:
        raise SystemExit("Não foi possivel carregar a imagem")
    
    print(img.shape)
    print(img.dtype)
    print(img.min())
    print(img.max())

    print(img[0, 0])


if __name__ == "__main__":
    main()
