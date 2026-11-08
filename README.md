# Sketch Proportions

Measuring objective properties of digital character drawings with **OpenCV**:
proportions between body landmarks, projective consistency (a proxy for 3D
coherence) and tonal distribution.

Undergraduate thesis (TCC) in Computer Science at UFRRJ — **early stage, no
results yet**. This repository is the experimental code and the scope document,
not a finished system.

## Research question (working)

Can image-processing techniques and pre-trained detectors estimate objective
metrics of **proportion**, **projective consistency** and **tonal
distribution** in digital drawings of characters?

The system does **not** judge artistic quality or infer the author's intention.
It measures observable properties and reports them with their limitations.

## What is being measured

| Metric | How | Automatic? |
| --- | --- | --- |
| Interocular distance / face width | facial detector + landmarks | planned |
| Eye line position (face thirds) | facial landmarks | planned |
| Head height / total height | landmarks (body) | no — manual annotation |
| Shoulder width / head width | landmarks (body) | no — manual annotation |
| Arm length / torso | landmarks (body) | no — manual annotation |
| Bilateral symmetry | mirroring + difference | yes |
| Projective consistency (3D proxy) | vanishing point of symmetric axes | partial |
| Tonal distribution | histogram + multi-Otsu | yes |
| Light direction | centroids of light/dark regions | yes |
| Stroke density | Canny edges per area | yes |

Methodological decisions so far:

- **Hybrid annotation.** The face will use a pre-trained detector (YuNet); the
  body uses manual landmarks. If the detector fails on stylized art, that is a
  result, not an error to hide.
- **"Perspective" means 3D coherence**, measured as a proxy: lines connecting
  symmetric body points should converge to a common vanishing point. Parallel
  lines are treated as an orthographic construction (vanishing point at
  infinity), which is valid.
- **Repeatability is part of the method.** Two annotations of the same image
  measure the noise floor; any metric must be larger than that noise to mean
  anything.

## What exists

```text
analyzer/
├── ferramenta_pontos.py      interactive landmark annotation (OpenCV + mouse)
├── passo1_ler.py             read the image and inspect the matrix
├── passo2_histograma.py      histograms
├── passo3_fundo.py           background separation
├── passo4_fundo_conectado.py connected background
├── passo5_tons_figura.py     tonal values of the figure
├── passo6_capturar_pontos.py point capture
├── passo7_proporcoes.py      proportion ratios from annotated points
├── passo8_perspectiva.py     projective consistency (vanishing point)
└── passo9_repetibilidade.py  repeatability between two annotations
data/
├── input/                    drawings (local only; not redistributed)
└── annotations/              landmark JSON files
docs/escopo.md                scope, threats to validity and decisions
```

The `passo*.py` files are incremental study scripts, each answering one
question. They are intentionally small and independent.

## Running the annotation tool

```powershell
pip install -r requirements.txt
python analyzer/ferramenta_pontos.py
python analyzer/ferramenta_pontos.py ..\data\input\corpo_inteiro.jpg
```

Controls: left click marks the current point and advances, `S` saves after all
points are marked, `Esc` exits without saving. Output goes to
`data/annotations/<image_name>.json`.

Then:

```powershell
cd analyzer
python passo7_proporcoes.py
python passo8_perspectiva.py
python passo9_repetibilidade.py
```

## Limitations

- Small sample; no statistical generalization.
- Detectors trained on photos may fail on stylized characters; the failure rate
  is something to measure.
- Manual annotation introduces variability; the protocol compares annotations
  of the same image.
- Reference proportions (the 7–8 head canon) are artistic conventions, not
  absolute truth.
- No final results have been produced yet. Nothing here should be read as a
  validated finding.

## Status

Scope defined (2026-11-06). Next steps: test YuNet on stylized images, finish
the annotation protocol, implement the projective and tonal metrics, and define
the evaluation set.

See `docs/escopo.md` for the full scope, threats to validity and recorded
decisions.
