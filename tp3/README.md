# TP3 - Analisis de sentimiento en tweets (Sentiment140)

## Objetivo

Construir un flujo de NLP que prediga la **polaridad** (negativo/positivo) de un tweet
a partir de su texto, y complementarlo con un analisis interpretativo del lenguaje:
que palabras definen cada sentimiento, de que hablan los tweets de cada clase, que
errores comete el modelo y que dicen esos errores (sarcasmo, ambiguedad, ruido de
etiquetas).

## Dataset

Sentiment140 (`trainingandtestdata.zip`, link en [`CONSIGNA.md`](./CONSIGNA.md)):

| Archivo | Filas | Clases | Etiquetado |
| --- | ---: | --- | --- |
| `training.1600000.processed.noemoticon.csv` | 1.600.000 | negativo / positivo (50/50) | automatico por emoticones |
| `testdata.manual.2009.06.14.csv` | 498 | negativo / neutral / positivo | manual |

**El training no tiene clase neutral**, por eso el modelo principal es binario y la
clase neutral se trata como extension exploratoria.

> Los CSV van en `data/raw/`. El training (228 MB) no se versiona por superar el
> limite de GitHub; descargarlo del link de la consigna y descomprimirlo ahi.

## Requisito mandatorio de la consigna

El modelo final y todas las metricas reportadas se calculan sobre el **dataset
completo** (1.600.000 tweets). Las notebooks 01 y 04 lo verifican con `assert`.

## Estructura

| Notebook | Contenido |
| --- | --- |
| [`01_carga_y_validacion.ipynb`](./notebooks/01_carga_y_validacion.ipynb) | Carga completa, distribucion de clases, duplicados y ruido de etiquetas |
| [`02_eda.ipynb`](./notebooks/02_eda.ipynb) | Longitud de tweets, palabras y bigramas por clase, seniales de Twitter |
| [`03_preprocesamiento.ipynb`](./notebooks/03_preprocesamiento.ipynb) | Limpieza documentada y persistencia en parquet |
| [`04_entrenamiento.ipynb`](./notebooks/04_entrenamiento.ipynb) | TF-IDF (1-2 gramas) + Logistic Regression; split 90/10 y reentrenamiento con el 100% |
| [`05_evaluacion.ipynb`](./notebooks/05_evaluacion.ipynb) | Metricas mandatorias, test manual, extension neutral por umbral |
| [`06_interpretacion.ipynb`](./notebooks/06_interpretacion.ipynb) | Coeficientes, **similitud coseno**, topicos NMF, sarcasmo, analisis por usuario |

`notebooks/utils.py` centraliza semilla, rutas y la funcion de limpieza. Los modelos
entrenados quedan en `models/` (se versionan, ~6 MB) y los graficos en `imgs/`.

Ejecutar en orden con el venv del proyecto:

```bash
.venv/bin/jupyter nbconvert --execute --to notebook --inplace notebooks/*.ipynb
```

## Decisiones principales

- **Modelo binario**: el training no tiene neutral; forzar 3 clases seria entrenar
  sin datos de una clase.
- **TF-IDF + Logistic Regression**: eficiente para 1,6 M de textos cortos e
  interpretable (los coeficientes son pesos por n-grama).
- **Split con shuffle + estratificacion**: el archivo viene ordenado por clase.
- **Limpieza conservadora**: URLs y menciones se tokenizan (`xxurl`, `xxuser`),
  hashtags conservan la palabra, **no** se remueven stopwords y los apostrofes se
  pegan (`can't` -> `cant`) para no perder negaciones.
- **Duplicados con etiquetas conflictivas (~2.225 textos) se conservan**: la consigna
  exige datos completos; se documentan como techo de performance.

## Resultados

| Evaluacion | accuracy | precision | recall | F1 |
| --- | ---: | ---: | ---: | ---: |
| Validacion (160.000 tweets no vistos) | 0,8251 | 0,8195 | 0,8338 | 0,8266 |
| Test manual (359 tweets, dominio distinto) | 0,8329 | 0,8050 | 0,8846 | 0,8429 |
| Extension: 3 clases por umbral (498 tweets) | 0,558 | — | — | — |

- El desempenio **se sostiene fuera del dominio de entrenamiento** (test manual
  etiquetado a mano sobre marcas/productos), senial de que el modelo aprendio
  vocabulario de sentimiento general.
- Los n-gramas mas predictivos son emocionales e inequivocos (`sad`, `poor`,
  `gutted` vs `thanks`, `smiling`, `blessed`) y varios **bigramas con negacion**
  (`not happy`, `not bad`, `cant wait`), validando conservar negaciones y usar
  `ngram_range=(1,2)`.
- **Similitud coseno** (metrica vista en clase): los centroides de ambas clases son
  muy parecidos (cos = 0,894) — las polaridades comparten casi todo el vocabulario y
  solo una fraccion chica de terminos carga el sentimiento. Ademas permitio
  recuperar tweets casi identicos con etiquetas opuestas (ruido de etiquetado).
- **Topicos (NMF)**: los negativos giran alrededor de trabajo/estudio, salud, extraniar
  y fallas; los positivos alrededor de saludos, agradecimientos, humor y planes.
- **Neutral por umbral de incertidumbre**: recupera poco (recall neutral 0,19 con
  delta 0,15) — "dudar" no es lo mismo que "ser neutral"; queda como limitacion.

## Limitaciones

1. **Sarcasmo e ironia**: palabras positivas en contexto negativo (p. ej.
   *"Great. History. Yay..."*) son estructuralmente invisibles para bolsa de palabras;
   ~1.100 errores de validacion siguen ese patron.
2. **Clase neutral ausente en training**: no se puede aprender; la aproximacion por
   umbral tiene techo bajo.
3. **Ruido de etiquetado automatico**: tweets identicos con etiquetas opuestas y
   falsos positivos obvios (tweets de "thanks" etiquetados negativos) ponen un techo
   a cualquier modelo sobre este dataset.

## Mejora futura

Usar un modelo de lenguaje preentrenado (embeddings contextuales) para capturar
ironia y contexto, y sumar datos neutrales reales para plantear las 3 clases.
