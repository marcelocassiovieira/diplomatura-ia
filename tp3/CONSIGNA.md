# Trabajo Practico 03 - Notas

## Consigna / material

Enlace provisto:

```text
https://docs.google.com/file/d/0B04GJPshIjmPRnZManQwWEdTZjg/edit?resourcekey=0-betyQkEmWZgp8z0DFxWsHw
```

El archivo de Google Drive se llama:

```text
trainingandtestdata.zip
```

## Fecha de entrega

- Fecha limite de entrega: **2026-07-16**.

## Presentacion

- La presentacion puede hacerse desde la misma notebook.
- Tambien se pueden usar otras herramientas de visualizacion o presentacion.
- La idea es que la presentacion incluya:
  - resultados obtenidos;
  - decisiones tomadas;
  - conclusiones principales.
- No es necesario explicar el codigo linea por linea.
- Es suficiente con mostrar los outputs relevantes de cada bloque y explicar que significan.

## Contenido del ZIP

El ZIP contiene dos archivos CSV:

```text
testdata.manual.2009.06.14.csv
training.1600000.processed.noemoticon.csv
```

## Dataset

- El archivo principal de entrenamiento contiene `1.600.000` tweets procesados.
- El archivo de test contiene tweets etiquetados manualmente.
- Es un dataset pensado para tareas de **analisis de sentimiento**.
- Los textos estan en ingles.
- Un objetivo posible es construir un modelo para predecir la **polaridad** de los tweets.
- Es decir, predecir si el sentimiento del texto es negativo, neutral o positivo.

## Consigna confirmada

- El analisis es libre.
- No tiene limites estrictos.
- Se pueden agregar todas las ideas que surjan durante el trabajo.
- Se pueden incluir:
  - analogias;
  - analisis de sensibilidad;
  - keywords;
  - extraccion de topicos;
  - modelos preentrenados;
  - graficos;
  - wordclouds;
  - UMAP;
  - otros algoritmos vistos en clase.
- Se debe usar al menos una de las metricas vistas, por ejemplo:
  - similitud coseno;
  - PMI;
  - PPMI.
- Los archivos estan orientados a un analisis de sentimiento.
- Si se elige ese enfoque, se pueden usar ambos archivos para evaluar que tan bien predice el modelo.
- El problema puede plantearse como una tarea de clasificacion supervisada:
  - entrada: texto del tweet;
  - salida: polaridad/sentimiento.

## Alcance propuesto

El TP se enfocara en construir y analizar un modelo de **clasificacion de sentimiento en tweets**.

### Objetivo general

- Desarrollar un flujo de trabajo de NLP que permita predecir la polaridad de un tweet a partir de su texto.

### Objetivos especificos

- Cargar y documentar el dataset de tweets.
- Realizar una exploracion inicial de clases, textos y palabras frecuentes.
- Preprocesar los tweets para dejarlos en un formato util para modelado.
- Entrenar al menos un modelo supervisado de clasificacion de sentimiento.
- Evaluar el desempeno del modelo con metricas de clasificacion.
- Usar al menos una metrica vista en clase, como similitud coseno, PMI o PPMI.
- Complementar el modelo con un analisis interpretativo de lenguaje:
  - topicos;
  - keywords;
  - embeddings;
  - analogias;
  - o patrones de error.

### Preguntas guia

- Que palabras aparecen con mas frecuencia en tweets positivos y negativos?
- Que tan bien se puede predecir la polaridad usando solo el texto del tweet?
- Que errores comete el modelo y que nos dicen sobre el lenguaje de los tweets?
- Los embeddings aprendidos capturan relaciones utiles entre palabras positivas y negativas?
- Hay indicios de sarcasmo o ambiguedad que dificulten la clasificacion?

### Dentro del alcance

- Analisis exploratorio del dataset.
- Limpieza y preprocesamiento de texto.
- Vectorizacion con Bag of Words, TF-IDF o embeddings.
- Entrenamiento de modelos clasicos de clasificacion.
- Evaluacion con metricas como accuracy, precision, recall, F1-score y matriz de confusion.
- Analisis complementario de topicos, keywords, similitudes o embeddings.
- Visualizaciones como barras, wordclouds, UMAP o matrices de confusion.

### Fuera del alcance

- Construir un sistema productivo o una API deployada.
- Etiquetar manualmente nuevos tweets.
- Resolver completamente la deteccion de sarcasmo.
- Entrenar modelos de deep learning pesados desde cero.
- Garantizar interpretacion causal de los resultados.

### Requisito mandatorio: uso completo de datos

- Es mandatorio usar **todos los datos disponibles**.
- No se admiten muestras como solucion final.
- El trabajo debe demostrar explicitamente que el modelo y las metricas finales fueron calculados sobre el dataset completo correspondiente.
- El dataset es grande, por lo que hay que planificar tiempos de ejecucion y recursos.
- Si la computadora local no alcanza, se debe buscar una alternativa:
  - optimizar el codigo;
  - usar procesamiento por chunks;
  - usar Google Colab;
  - usar Kaggle Notebooks;
  - usar otra plataforma con mas RAM/CPU;
  - guardar resultados intermedios para no repetir pasos costosos.
- La limitacion de hardware no deberia ser una excusa para no completar el trabajo.
- Siempre conviene empezar probando el flujo con pocas filas para depurar errores, pero la ejecucion final y los resultados reportados deben usar el dataset completo.

### Entregable esperado

- Una notebook principal con el analisis completo.
- Un resumen final con conclusiones, metricas y limitaciones.
- Opcionalmente, graficos o imagenes exportadas para acompanar la presentacion.

## Minimo obligatorio propuesto

Para que el TP tenga un alcance manejable, el minimo a realizar deberia ser:

1. **Carga del dataset**
   - Leer el archivo de entrenamiento y el archivo de test.
   - Asignar nombres de columnas.
   - Verificar cantidad de filas, columnas y clases disponibles.
   - Confirmar que la ejecucion final utiliza todos los registros disponibles. Este punto es mandatorio.

2. **EDA basico**
   - Mostrar distribucion de la variable `target`.
   - Mostrar ejemplos de tweets positivos, negativos y neutrales si estan disponibles.
   - Analizar longitud de tweets.
   - Mostrar palabras mas frecuentes por clase.

3. **Preprocesamiento**
   - Pasar texto a minusculas.
   - Limpiar URLs.
   - Limpiar menciones `@usuario`.
   - Decidir que hacer con hashtags.
   - Tokenizar o preparar el texto para vectorizacion.

4. **Modelo base de sentimiento**
   - Vectorizar los tweets con `TF-IDF` o Bag of Words.
   - Entrenar un modelo clasico, por ejemplo:
     - Logistic Regression;
     - Naive Bayes;
     - Linear SVM.
   - Predecir la polaridad de los tweets del conjunto de test o validacion.
   - Entrenar y evaluar el flujo final con todos los datos, no solamente con una muestra. Este punto es mandatorio.

5. **Evaluacion**
   - Reportar al menos:
     - accuracy;
     - precision;
     - recall;
     - F1-score;
     - matriz de confusion.

6. **Metrica de NLP vista en clase**
   - Incluir al menos una:
     - similitud coseno;
     - PMI;
     - PPMI;
     - similitud entre embeddings.
   - Explicar que se interpreta con esa metrica.

7. **Conclusion**
   - Resumir que tan bien funciono el modelo.
   - Mencionar principales errores o limitaciones.
   - Proponer una mejora futura.

Todo lo demas queda como **extension opcional**: topicos, embeddings, analogias, sarcasmo, UMAP, wordclouds o modelos preentrenados.

## Estructura de columnas

Los CSV no vienen con encabezado. Las columnas observadas son:

| Posicion | Campo | Descripcion |
| --- | --- | --- |
| 0 | `target` | Etiqueta de sentimiento. |
| 1 | `id` | Identificador del tweet. |
| 2 | `date` | Fecha del tweet. |
| 3 | `query` | Query asociada. En training suele aparecer `NO_QUERY`. |
| 4 | `user` | Usuario que publico el tweet. |
| 5 | `text` | Texto del tweet. |

## Etiquetas de sentimiento

En este dataset, la columna `target` suele interpretarse asi:

| Valor | Sentimiento |
| --- | --- |
| `0` | Negativo |
| `2` | Neutral |
| `4` | Positivo |

En el archivo de entrenamiento observado aparecen ejemplos con `0` al inicio. En el archivo de test observado aparecen ejemplos con `4`.

## Ejemplo de lectura con pandas

```python
import pandas as pd

columnas = ["target", "id", "date", "query", "user", "text"]

train = pd.read_csv(
    "training.1600000.processed.noemoticon.csv",
    encoding="latin-1",
    header=None,
    names=columnas
)

test = pd.read_csv(
    "testdata.manual.2009.06.14.csv",
    encoding="latin-1",
    header=None,
    names=columnas
)
```

## Consideraciones

- Conviene usar `encoding="latin-1"` para evitar errores de lectura por caracteres especiales.
- El dataset es grande, por lo que conviene optimizar lectura, limpieza y vectorizacion.
- Se puede usar una muestra solo para depurar codigo rapidamente, pero no como resultado final.
- Los resultados finales deben calcularse usando todos los datos. Esto es mandatorio para la consigna.
- Para modelado de sentimiento se deberia separar:
  - variable objetivo: `target`;
  - texto de entrada: `text`.
- Antes de entrenar modelos conviene aplicar preprocesamiento:
  - pasar a minusculas;
  - limpiar URLs;
  - limpiar menciones `@usuario`;
  - limpiar hashtags o decidir si conservarlos;
  - tokenizar;
  - vectorizar con Bag of Words, TF-IDF o embeddings.

## Enfoque sugerido

1. Cargar el dataset.
2. Hacer una exploracion inicial:
   - cantidad de tweets por clase;
   - ejemplos positivos y negativos;
   - longitud de textos;
   - palabras frecuentes por clase.
3. Limpiar y preprocesar los tweets.
4. Vectorizar los textos.
5. Entrenar un modelo de clasificacion de sentimiento.
6. Evaluar el modelo con metricas de clasificacion:
   - accuracy;
   - precision;
   - recall;
   - F1-score;
   - matriz de confusion.
7. Incorporar al menos una metrica de similitud vista en clase:
   - similitud coseno entre palabras o documentos;
   - PMI/PPMI sobre co-ocurrencias;
   - comparacion de embeddings.
8. Agregar visualizaciones opcionales:
   - wordcloud por sentimiento;
   - UMAP de embeddings o vectores;
   - barras de palabras mas frecuentes.

## Ideas posibles de analisis

### Extraccion de topicos

- Una linea interesante es extraer **topicos** de los tweets.
- El objetivo seria identificar de que temas hablan los tweets positivos, negativos o neutrales.
- Esto puede ayudar a responder preguntas como:
  - que temas aparecen mas en tweets negativos;
  - que temas aparecen mas en tweets positivos;
  - si hay topicos asociados a productos, marcas, personas, problemas tecnicos, emociones o eventos;
  - si los topicos cambian segun la polaridad.
- Enfoques posibles:
  - usar palabras mas frecuentes por clase;
  - usar n-gramas frecuentes por clase;
  - aplicar TF-IDF para detectar terminos distintivos;
  - usar clustering sobre embeddings de tweets;
  - usar modelos de topicos como LDA;
  - usar embeddings y luego reducir dimensionalidad con UMAP para visualizar grupos.
- Una salida posible seria:
  - top 10 palabras por sentimiento;
  - top 10 bigramas por sentimiento;
  - wordcloud por sentimiento;
  - clusters de tweets y descripcion manual de cada cluster;
  - comparacion entre topicos positivos y negativos.

### Entrenar embeddings y buscar analogias

- Otra linea posible es entrenar **embeddings** sobre los tweets.
- El objetivo seria aprender representaciones vectoriales de palabras usando el propio corpus.
- Luego se podrian analizar relaciones entre palabras y buscar analogias utiles para interpretar el contenido.
- Por ejemplo:
  - palabras cercanas a terminos positivos como `love`, `great`, `happy`;
  - palabras cercanas a terminos negativos como `hate`, `bad`, `sad`;
  - palabras cercanas a marcas, productos, personas o eventos mencionados;
  - diferencias entre palabras asociadas a emociones positivas y negativas.
- Tambien se podrian probar analogias del estilo:

```text
palabra_A - palabra_B + palabra_C ≈ palabra_D
```

- La utilidad no seria solamente encontrar sinonimos, sino entender que palabras aparecen en contextos parecidos.
- Esto puede servir para:
  - descubrir asociaciones inesperadas;
  - encontrar palabras representativas de cada sentimiento;
  - comparar lenguaje positivo y negativo;
  - detectar comunidades semanticas dentro del corpus;
  - generar features para un modelo de clasificacion.
- Enfoque posible:
  - limpiar y tokenizar los tweets;
  - entrenar Word2Vec o FastText;
  - buscar palabras mas similares a terminos clave;
  - calcular similitud coseno entre palabras;
  - comparar embeddings entrenados en tweets positivos vs negativos;
  - visualizar palabras con UMAP o PCA.
- Una variante interesante seria entrenar dos modelos:
  - uno solo con tweets positivos;
  - otro solo con tweets negativos.
- Luego se puede comparar si una misma palabra aparece cerca de contextos distintos segun el sentimiento.

### Detector de sarcasmo

- Otra idea posible, mas avanzada, es intentar construir o analizar un **detector de sarcasmo**.
- Es una tarea compleja porque el significado literal del texto puede ser distinto de la intencion real.
- Por ejemplo, un tweet puede usar palabras positivas pero expresar una opinion negativa:

```text
Great, my phone died again. Amazing.
```

- Literalmente aparecen palabras como `great` y `amazing`, pero el sentido real es negativo.
- Esto puede confundir a modelos simples basados solo en palabras frecuentes o polaridad directa.
- Para detectar sarcasmo podria ser necesario usar informacion adicional:
  - contexto conversacional;
  - signos de puntuacion;
  - emojis;
  - hashtags como `#sarcasm`;
  - contraste entre palabras positivas y situaciones negativas;
  - modelos preentrenados mas fuertes.
- En el TP podria plantearse como analisis exploratorio:
  - buscar tweets donde aparezcan palabras positivas en textos etiquetados como negativos;
  - revisar manualmente ejemplos;
  - detectar patrones de ironia o sarcasmo;
  - comparar errores del modelo de sentimiento y ver si algunos parecen sarcasticos.
- No seria necesario resolverlo completamente, pero puede servir como limitacion interesante del analisis de sentimiento.

## Idea de entrega

- Una notebook reproducible con:
  - carga de datos;
  - EDA;
  - preprocesamiento;
  - entrenamiento;
  - evaluacion;
  - interpretacion de resultados.
- Un breve resumen final explicando:
  - que modelo se uso;
  - que resultados obtuvo;
  - que palabras o patrones diferencian sentimientos;
  - limitaciones del enfoque.
