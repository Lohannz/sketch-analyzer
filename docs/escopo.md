# Escopo do TCC — v0.1 (em definição)

> Documento de trabalho. Registra decisões tomadas até 2026-11-06.
> Não é texto final de TCC. Ajustar conforme orientação do professor.

## 1. Objeto de estudo

Desenhos digitais de **personagens**, em dois estágios:

- line art (traço);
- pintura (com cor e valores tonais).

Fundo e estilo variados. O sistema não julga qualidade artística nem intenção
do autor; mede propriedades observáveis.

## 2. Pergunta de pesquisa (provisória)

É possível estimar, com técnicas de processamento digital de imagens e
detectores pré-treinados, métricas objetivas de **proporção**, **consistência
projetiva** e **distribuição tonal** em desenhos digitais de personagens?

## 3. O que o sistema mede

| Métrica | Como é obtida | Automático? |
| --- | --- | --- |
| Distância interocular / largura do rosto | detector facial + landmarks | sim |
| Posição da linha dos olhos (terços do rosto) | landmarks faciais | sim |
| Altura da cabeça / altura total | landmarks (corpo) | não (marcação) |
| Largura dos ombros / largura da cabeça | landmarks (corpo) | não (marcação) |
| Comprimento de braço / torso | landmarks (corpo) | não (marcação) |
| Simetria bilateral | espelhamento + diferença | sim |
| Consistência projetiva (proxy de 3D) | ponto de fuga dos eixos simétricos | parcial (cálculo automático sobre pontos) |
| Distribuição tonal | histograma + threshold multi-Otsu | sim |
| Direção da luz | centroides das regiões clara/escura | sim |
| Densidade de traço | bordas (Canny) por área | sim |

### 3.1. Decisão sobre os pontos anatômicos

Abordagem **híbrida** (decidida em 2026-11-06):

- **Rosto:** detecção automática com modelo pré-treinado (YuNet, disponível no
  OpenCV instalado). Se falhar em estilo estilizado, isso é resultado, não erro
  a esconder.
- **Corpo:** marcação manual (ou confirmação de sugestão automática) dos
  pontos: topo da cabeça, queixo, ombros, cotovelos, punhos, quadris, joelhos,
  tornozelos.

### 3.2. Decisão sobre "perspectiva"

"Perspectiva" foi definida como **coerência 3D do corpo**. Como isso não é
mensurável diretamente, o sistema mede **consistência projetiva** como proxy:

> As retas que ligam pares de pontos simétricos devem convergir para um ponto
> de fuga comum. Se forem paralelas, o caso é tratado como construção
> ortográfica (ponto de fuga no infinito), que é válido.

O sistema **não** afirma que o corpo está correto em 3D.

## 4. O que o sistema NÃO faz

- Não avalia se o desenho é bom ou ruim.
- Não infere intenção artística.
- Não reconstrói geometria 3D.
- Não garante anatomia correta ("braço fora de proporção" não é diagnóstico).
- Não funciona igual em todos os estilos; a limitação por estilo deve ser
  medida e relatada.

## 5. Ameaças à validade

1. **Detectores treinados em fotos** podem falhar em personagens estilizados.
   Medir a taxa de falha faz parte do trabalho.
2. **Marcação manual** introduz variabilidade. Medir repetibilidade
   (mesma pessoa marcando duas vezes; pessoas diferentes marcando).
3. **Estilo** altera a interpretação das métricas (anime × semi-realista).
4. **Amostra pequena** não permite generalização estatística.
5. **Proporções de referência** (cânone de 7–8 cabeças) são convenções
   artísticas, não verdades; servem de comparação, não de gabarito absoluto.

## 6. Próximos passos

1. Testar YuNet nas imagens de exemplo (funciona em estilo anime?).
2. Construir a ferramenta de marcação manual de pontos (OpenCV + mouse).
3. Calcular as métricas de proporção a partir dos pontos.
4. Implementar consistência projetiva.
5. Implementar análise tonal (histograma, Otsu, direção da luz).
6. Definir o conjunto de avaliação e o protocolo de medição.

## 7. Decisões registradas

| Data | Decisão |
| --- | --- |
| 2026-11-06 | Objeto: desenho digital de personagem (line art e pintura) |
| 2026-11-06 | Pontos anatômicos: abordagem híbrida |
| 2026-11-06 | Perspectiva = coerência 3D, medida por proxy projetivo |
| 2026-11-06 | Código anterior movido para `_legado/`; código novo escrito pelo estudante |
