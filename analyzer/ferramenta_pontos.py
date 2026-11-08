"""Ferramenta de marcação de pontos anatômicos — v1.

Uso:
    python ferramenta_pontos.py [caminho_da_imagem] [sufixo]

Exemplos:
    python ferramenta_pontos.py                                  # imagem3.jpg
    python ferramenta_pontos.py ../data/input/corpo_inteiro.jpg
    python ferramenta_pontos.py ../data/input/corpo_inteiro.jpg _b

Controles:
    clique esquerdo -> marca o ponto atual e avança
    S               -> salva (só depois de marcar todos)
    ESC             -> sai sem salvar

Saída:
    data/annotations/<nome_da_imagem>.json
"""

import cv2
import json
import sys
from pathlib import Path

BASE = Path(__file__).parent.parent
PASTA_SAIDA = BASE / "data" / "annotations"

# Ordem oficial de marcação. NÃO mude sem atualizar o protocolo em docs/.
# esquerda/direita = de quem olha a imagem.
PONTOS = [
    "topo_cabeca", "queixo", "olho_esq", "olho_dir", "nariz", "boca",
    "ombro_esq", "ombro_dir", "cotovelo_esq", "cotovelo_dir",
    "punho_esq", "punho_dir",
    "quadril_esq", "quadril_dir", "joelho_esq", "joelho_dir",
    "tornozelo_esq", "tornozelo_dir",
]

estado = {"i": 0, "pontos": {}}


def ao_clicar(evento, x, y, flags, param):
    if evento != cv2.EVENT_LBUTTONDOWN:
        return
    if estado["i"] >= len(PONTOS):
        return

    estado_atual = PONTOS[estado['i']]
    estado["pontos"][estado_atual] = (x, y)
    estado["i"] += 1


def desenhar(img):
    for i, nome in enumerate(PONTOS):
        if nome not in estado["pontos"]:
            continue
        x, y = estado["pontos"][nome]

        # TODO 4: desenhe um círculo vermelho (raio 5, preenchido) e
        #         escreva o número i ao lado
        #         dica: cv2.circle e cv2.putText
        cv2.circle(img, (x,y), 6, (0, 0, 255), 2)
        cv2.putText(img, str(nome), ((x + 8), (y- 8)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    if estado["i"] < len(PONTOS):
        texto = f"{estado['i'] + 1}/{len(PONTOS)}: {PONTOS[estado['i']]}"
    else:
        texto = "concluido - aperte S para salvar"
    cv2.putText(img, texto, (10, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 2)



def main():
    if len(sys.argv) > 1:
        caminho = Path(sys.argv[1])
    else:
        caminho = BASE / "data" / "input" / "corpo_inteiro.jpg"

    img = cv2.imread(str(caminho))
    if img is None:
        raise SystemExit(f"Não foi possível carregar: {caminho}")

    cv2.namedWindow("pontos")
    cv2.setMouseCallback("pontos", ao_clicar)
    for i, nome in enumerate(PONTOS):
        cv2.putText(img, str(str(i) + " - " + nome), ((10), (i * 20 + 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 2)
        
    salvar = False
    while True:
        tela = img.copy()
        desenhar(tela)
        cv2.imshow("pontos", tela)
        tecla = cv2.waitKey(20) & 0xFF
        if tecla == 27:                                  # ESC
            break
        if tecla == ord("s") and estado["i"] >= len(PONTOS):
            salvar = True
            break
    cv2.destroyAllWindows()

    if not salvar:
        print("nada salvo")
        return

    PASTA_SAIDA.mkdir(parents=True, exist_ok=True)
    sufixo = sys.argv[2] if len(sys.argv) > 2 else ""
    destino = PASTA_SAIDA / (caminho.stem + sufixo + ".json")

    # Nunca sobrescreve: se o nome já existe, acrescenta _2, _3, ...
    contador = 2
    while destino.exists():
        destino = PASTA_SAIDA / f"{caminho.stem}{sufixo}_{contador}.json"
        contador += 1
    if contador > 2:
        print(f"arquivo já existia; salvando como {destino.name}")

    with open(destino, "w", encoding="utf-8") as f:
        json.dump({"arquivo": caminho.name, "pontos": estado["pontos"]},
                  f, indent=2, ensure_ascii=False)
    print("salvo em", destino)


if __name__ == "__main__":
    main()
