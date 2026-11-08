"""Passo 6a — Capturar cliques na imagem.

Objetivo: clicar em pontos do desenho e guardar as coordenadas (x, y).

Como rodar (dentro da pasta analyzer):
    python passo6_capturar_pontos.py

Controles:
    clique esquerdo -> adiciona um ponto
    ESC             -> fecha e imprime a lista
"""

import cv2
from pathlib import Path

BASE = Path(__file__).parent.parent
CAMINHO = BASE / "data" / "input" / "imagem.jpg"

pontos = []   # lista de tuplas (x, y)


def ao_clicar(evento, x, y, flags, param):
    # TODO: se o evento for cv2.EVENT_LBUTTONDOWN:
    #         - adicione (x, y) na lista `pontos`
    #         - imprima as coordenadas
    if evento == cv2.EVENT_LBUTTONDOWN:
        pontos.append((x, y))
        print((x, y))

def main():
    img = cv2.imread(CAMINHO)
    if img is None:
        raise SystemExit(f"Não foi possível carregar: {CAMINHO}")

    cv2.namedWindow("pontos")
    cv2.setMouseCallback("pontos", ao_clicar)

    # Laço de exibição: roda até você apertar ESC.
    while True:
        cv2.imshow("pontos", img)
        tecla = cv2.waitKey(20) & 0xFF
        # TODO: se tecla == 27 (ESC), pare o laço
        if tecla == 27:
            break

    
    cv2.destroyAllWindows()
    for i, p in enumerate(pontos):
        cv2.circle(img, p, 6, (0,0 , 255), -1)
        cv2.putText(img, str(i), (p[0] + 8, p[1] - 8),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    print("total de pontos:", len(pontos))
    print(pontos)
    cv2.imshow("pontos", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
