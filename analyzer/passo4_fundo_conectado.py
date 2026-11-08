"""Passo 4 — Fundo conectado: corrigindo o buraco no personagem.

No passo 3, todo pixel parecido com a cor do fundo virou fundo — inclusive
uma região dentro da personagem. Aqui acrescentamos CONECTIVIDADE: só é
fundo o que está ligado à borda da imagem.

Como rodar (dentro da pasta analyzer):
    python passo4_fundo_conectado.py
"""

import cv2
import numpy as np
from pathlib import Path

BASE = Path(__file__).parent.parent
CAMINHO = BASE / "data" / "input" / "imagem4.png"
TOLERANCIA = 60


def main():
  img = cv2.imread(str(CAMINHO))
  if img is None:
    raise SystemExit(f"Não foi possível carregar: {CAMINHO}")

  h, w = img.shape[:2]

  # --- igual ao passo 3: candidatos a fundo, só pela cor ---
  cor_fundo = img[0, 0]
  diferenca = np.abs(img.astype(int) - cor_fundo).sum(axis=2)
  fundo_candidato = (diferenca < TOLERANCIA).astype(np.uint8) * 255

  # 1) Crie a máscara do floodFill.
  # Ela precisa ser 2 pixels maior em cada lado: (h + 2, w + 2).
  mask = np.zeros((h + 2, w + 2), np.uint8)

  # 2) Derrame a partir do canto superior esquerdo (0, 0).
  # Sem loDiff/upDiff, ele só avança sobre pixels de valor IGUAL.
  cv2.floodFill(fundo_candidato, mask, (0, 0), 255)

  # 3) Recorte a borda extra da máscara.
  fundo_conectado = mask[1:-1, 1:-1] * 255

  # 4) Personagem = tudo que NÃO é fundo conectado.
  personagem = cv2.bitwise_not(fundo_conectado)

  # 5) Compare e salve.
  numero_pixels_personagem = (personagem > 0).sum()
  fracao_personagem = numero_pixels_personagem / (h * w)

  print(f"Quantidade de pixels do personagem: {numero_pixels_personagem}")
  print(f"Fração da imagem ocupada pelo personagem: {fracao_personagem:.2%}")

  img_personagem = cv2.bitwise_and(img, img, mask=personagem)
  SAIDA = BASE / "output"
  SAIDA.mkdir(parents=True, exist_ok=True)
  cv2.imwrite(str(SAIDA / "passo4_personagem.png"), img_personagem)


if __name__ == "__main__":
    main()
