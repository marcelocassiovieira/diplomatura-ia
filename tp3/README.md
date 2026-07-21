# TP3 - Analisis de sentimiento en tweets (Sentiment140)

## Objetivo

Construir un flujo de NLP que prediga la **polaridad** (negativo/positivo) de un tweet
a partir de su texto, y complementarlo con un analisis interpretativo de que palabras
definen cada sentimiento y como interpretarlas con similitud coseno.

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
| [`01_carga_y_validacion.ipynb`](./notebooks/01_carga_y_validacion.ipynb) | Carga completa, distribucion de clases, y analisis de calidad de las etiquetas |
| [`02_eda.ipynb`](./notebooks/02_eda.ipynb) | Longitud de tweets, palabras/bigramas por clase, signos de puntuacion |
| [`03_preprocesamiento.ipynb`](./notebooks/03_preprocesamiento.ipynb) | Limpieza documentada (7 decisiones justificadas) y persistencia en parquet |
| [`04_entrenamiento.ipynb`](./notebooks/04_entrenamiento.ipynb) | TF-IDF (1-2 gramas) + Logistic Regression; split 90/10, chequeo de overfitting y reentrenamiento con el 100% |
| [`05_evaluacion.ipynb`](./notebooks/05_evaluacion.ipynb) | Metricas mandatorias, comparacion contra un baseline, matriz de confusion, test manual |
| [`06_interpretacion.ipynb`](./notebooks/06_interpretacion.ipynb) | Coeficientes del modelo y **similitud coseno** (metrica de clase obligatoria) |

`notebooks/utils.py` centraliza semilla, rutas y la funcion de limpieza. Los modelos
entrenados quedan en `models/` (se versionan, ~6 MB) y los graficos en `imgs/`.

Ejecutar en orden con el venv del proyecto:

```bash
.venv/bin/jupyter nbconvert --execute --to notebook --inplace notebooks/*.ipynb
```

## Analisis de calidad de datos (notebook 01)

El dataset se etiqueto automaticamente segun si el tweet original tenia un
emoticon (`:)` o `:(`), que despues fue borrado del texto. Eso genera errores que se
verificaron con ejemplos concretos: tweets con tono neutral o sarcastico etiquetados
como si tuvieran una polaridad clara (por ejemplo "Hiccups. Just what I need before
retiring to my reading room", etiquetado negativo).

Como evidencia dura, se buscaron textos identicos que aparecen mas de una vez con
etiquetas opuestas: 2.225 textos (~6.895 filas, 0,43% del dataset). Esa cifra se
trata como un **piso**, no como el total real del ruido: solo detecta duplicados
exactos, y ya se habian encontrado a mano otros casos ambiguos que no son duplicados
exactos. Por eso no se eliminan esos registros del dataset (ademas de que la consigna
exige usar todos los datos): sacar solo los duplicados exactos daria una falsa
sensacion de haber limpiado el ruido.

## Decisiones de preprocesamiento (notebook 03)

Cada decision se tomo despues de ver un ejemplo concreto del problema que resolvia:

| Elemento | Decision | Motivo |
| --- | --- | --- |
| Negaciones (`not`, `don't`, `no`) | Conservar | Sin ellas no se distingue `good` de `not good`. Confirmado despues con los coeficientes del modelo (ver mas abajo). |
| Apostrofes en contracciones | Pegar (`don't` -> `dont`), no expandir | El vectorizador de scikit-learn corta por el apostrofe y pierde la negacion (`don't` -> `don` + `t`, la `t` se descarta). |
| Menciones `@usuario` | Reemplazar por `usuariomencionado` | Borrar rompe la estructura de la oracion en tweets donde la mencion es sujeto (`@user loves @otro more` -> `loves more`). |
| URLs | Reemplazar por `linkweb` | Mismo criterio que las menciones. |
| HTML mal formado (`&amp;`, `&quot;`) | Corregir | No es contenido real del tweet, es un error de formato. |
| Hashtags | Sacar el `#`, conservar la palabra | Es contenido real del tweet, a diferencia de una mencion. |
| Mayusculas | Pasar todo a minusculas | `Good` y `good` deben contar como la misma palabra. |

## Resultados (notebook 05)

| Evaluacion | accuracy | precision | recall | F1 |
| --- | ---: | ---: | ---: | ---: |
| Train del modelo de desarrollo (1.440.000) | 0,8466 | 0,8399 | 0,8564 | 0,8481 |
| Validacion (160.000 tweets no vistos) | 0,8249 | 0,8188 | 0,8343 | 0,8265 |

**Por que el accuracy solo no alcanza**: un modelo que siempre predijera "positivo"
sin leer el tweet, en este dataset balanceado 50/50, acertaria 50% (acierta toda una
clase y falla toda la otra). El modelo entrenado saca 82%, muy por encima de ese
baseline, señal de que aprende algo real del texto.

**Matriz de confusion (validacion, 160.000 tweets)**: 132.011 tweets acertados y
27.989 errados. Los dos tipos de error (14.697 negativos predichos como positivos,
13.292 positivos predichos como negativos) son parecidos entre si, sin sesgo fuerte
hacia un lado — consistente con que precision y recall tambien salen parecidos entre
las dos clases (negativo: precision 0,8309/recall 0,8163; positivo: precision
0,8195/recall 0,8338).

**Chequeo de overfitting**: la brecha entre train y validacion es de ~2,2 puntos de
accuracy — no hay sobreajuste relevante.

## Interpretacion (notebook 06)

**Coeficientes del modelo**: entre los n-gramas que mas empujan a "positivo" aparecen
varios con negacion (`cant wait`, `not bad`, `no problem`, `no need`, `dont need`).
Esto confirma la decision de conservar las negaciones tomada antes de entrenar el
modelo: si se hubiera sacado el `not` de `not bad`, el bigrama hubiera quedado solo
como `bad`, aprendido como negativo.

**Similitud coseno** (metrica de clase obligatoria): mide que tan parecidos son dos
tweets segun el vocabulario que comparten (0 = nada en comun, 1 = mismo vocabulario).
Se aplico de dos formas:
- Buscar tweets vecinos de una consulta (ej. un tweet con "freakin cooool i love
  twitter" encontro vecinos por compartir la palabra "freakin" y otros por compartir
  la frase "i love twitter").
- Buscar posibles etiquetas mal puestas: sobre una muestra de 300 tweets negativos,
  se encontro 1 caso con similitud maxima (coseno=1,000) y etiqueta opuesta, pero
  resulto ser el mismo tipo de caso que los duplicados exactos de la notebook 01, no
  un hallazgo nuevo. Limitacion: 300 tweets es una muestra chica frente al total.

## Limitaciones

1. **Ruido de etiquetado automatico**: al menos 0,43% del dataset son textos
   identicos con etiquetas opuestas (piso, no total); eso pone un techo a cualquier
   modelo entrenado sobre este dataset.
2. **Clase neutral ausente en training**: el modelo principal es binario porque no
   hay ejemplos de la clase neutral para entrenar con ella.
3. **Alcance recortado**: por tiempo, esta entrega no incluye modelado de topicos,
   analisis de sarcasmo ni analisis por usuario, que habian sido explorados pero se
   priorizo profundizar el analisis obligatorio (calidad de datos, preprocesamiento,
   evaluacion, similitud coseno) en vez de cubrir mas superficie con menos detalle.

## Mejora futura

Extender el analisis de errores (sarcasmo, ironia) y el modelado de topicos con el
mismo nivel de profundidad que el resto del trabajo, y sumar datos neutrales reales
para plantear el problema de 3 clases.
