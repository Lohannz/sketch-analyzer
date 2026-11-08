"""Passo 5 — Histograma só da figura.

Objetivo: comparar a distribuição tonal da imagem inteira com a distribuição
tonal apenas da figura (fundo removido no passo 4).

Como rodar (dentro da pasta analyzer):
    python passo5_tons_figura.py
"""

import cv2
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
BASE = Path(__file__).parent.parent
CAMINHO = BASE / "data" / "input" / "imagem4.png"
TOLERANCIA = 60


def main():
    img = cv2.imread(CAMINHO)
    if img is None:
        raise SystemExit(f"Não foi possível carregar: {CAMINHO}")
    h, w = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # --- segmentação (a mesma do passo 4) ---
    diferenca = np.abs(img.astype(int) - img[0, 0]).sum(axis=2)
    fundo_candidato = (diferenca < TOLERANCIA).astype(np.uint8) * 255
    mask = np.zeros((h + 2, w + 2), np.uint8)
    cv2.floodFill(fundo_candidato, mask, (0, 0), 255)
    fundo = mask[1:-1, 1:-1] * 255
    personagem = cv2.bitwise_not(fundo)

    # 1) Selecione só os pixels da figura (boolean indexing).
    #    Dica: gray[personagem > 0]

    pixels_figura = gray[personagem > 0]

    # 2) Calcule o histograma desses pixels (256 caixas, 0 a 255).
    #    Dica: np.histogram(pixels_figura, bins=256, range=(0, 256))[0]
    hist, bin_edges = np.histogram(pixels_figura, bins=256, range=(0, 256))

    # 3) Imprima, lado a lado, média e desvio da imagem inteira e da figura.
    #    Dica: gray.mean(), gray.std(), pixels_figura.mean(), pixels_figura.std()
    #    Imprima também quantos pixels tem a figura.
    media_image = gray.mean()
    desvio_image = gray.std()
    media_figura = pixels_figura.mean()
    desvio_figura = pixels_figura.std()

    media_image = gray.mean()
    desvio_image = gray.std()
    media_figura = pixels_figura.mean()
    desvio_figura = pixels_figura.std()
    pixels_total = h * w
    pixels_fig = len(pixels_figura)

    print(f"{'Métrica':<10} | {'Imagem Inteira':<15} | {'Só Figura':<15}")
    print("-" * 50)
    print(f"{'Média':<10} | {media_image:<15.2f} | {media_figura:<15.2f}")
    print(f"{'Desvio':<10} | {desvio_image:<15.2f} | {desvio_figura:<15.2f}")
    print(f"{'Pixels':<10} | {pixels_total:<15} | {pixels_fig:<15}")
    
    hist_16, bin_edges_16 = np.histogram(pixels_figura, bins=16, range=(0, 256))
    # 4) Desenhe o gráfico de barras (16 faixas) do histograma da figura.
    #    Mesmo código do passo 2, mas usando `contagens` acima.
    plt.bar(bin_edges_16[:-1], hist_16, width=14, color='skyblue', edgecolor='black', align='edge')

    plt.title('Histograma de Tons da Figura (16 Faixas)')
    plt.xlabel("Valor de Intensidade (Tom de Cinza)")
    plt.ylabel("Qtd Pixels")
    plt.grid(axis='y', alpha=0.75)

    plt.show()
if __name__ == "__main__":
    main()
