"""Passo 3 — Separar fundo do personagem.

Objetivo: medir o desenho, não o fundo. O fundo desta imagem é uma cor
chapada, então definimos "fundo" como todo pixel parecido com a cor do
canto da imagem.

Como rodar (dentro da pasta analyzer):
    python passo3_fundo.py
"""

import cv2
import numpy as np
from pathlib import Path

BASE = Path(__file__).parent.parent
CAMINHO = BASE / "data" / "input" / "imagem4.png"
TOLERANCIA = 60   # quanto a cor pode variar e ainda ser considerada fundo


def main():
    img = cv2.imread(CAMINHO)
    if img is None:
        raise SystemExit(f"Não foi possível carregar: {CAMINHO}")

    h, w = img.shape[:2]

    # 1) Pegue a cor do fundo no canto superior esquerdo.
    #    Dica: img[0, 0] devolve um pixel BGR
    cor_fundo = img[0, 0]

    # 2) Calcule a diferença de cada pixel para essa cor.
    #    ATENÇÃO: converta para int antes de subtrair, senão o uint8 "dá a volta".
    #    Dica: np.abs(img.astype(int) - cor_fundo).sum(axis=2)
    #    (axis=2 soma os 3 canais, gerando uma matriz 2D de diferenças)
    diferenca = np.abs(img.astype(int) - cor_fundo).sum(axis=2)

    # 3) Gere as máscaras:
    #    fundo      = onde a diferença é pequena (< TOLERANCIA)
    #    personagem = o contrário
    #    As duas precisam ser uint8 com valores 0 ou 255.
    #    Dica: (.astype(np.uint8) * 255) e cv2.bitwise_not(...)
    fundo = (diferenca < TOLERANCIA).astype(np.uint8) * 255
    personagem = cv2.bitwise_not(fundo)

    # 4) Imprima quantos pixels são personagem e que fração da imagem isso é.
    #    Dica: (personagem > 0).sum() e divida por (h * w)
    numero_pixels_personagem = (personagem > 0).sum()
    fracao_personagem = numero_pixels_personagem/(h * w)
    print(f"Quantidade de pixels do personagem: {numero_pixels_personagem}")
    print(f"Fração da imagem ocupada pelo personagem: {fracao_personagem:.2%}")
  
  # 5) Salve uma imagem só com o personagem (fundo preto).
    #    Dica: cv2.bitwise_and(img, img, mask=personagem)
    #    e cv2.imwrite(str(BASE / "saida" / "passo3_personagem.png"), resultado)
    #    (crie a pasta saida antes, se não existir)
    # TODO

    img_personagem = cv2.bitwise_and(img, img, mask=personagem)
    SAIDA = BASE / "output"
    SAIDA.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(SAIDA / "personage.png"), img_personagem)

  

if __name__ == "__main__":
    main()
