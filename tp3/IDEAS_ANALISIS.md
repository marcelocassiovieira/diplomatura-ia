# TP3 - Ideas de analisis a partir del dataset

## Lectura del problema

El dataset sirve principalmente para **analisis de sentimiento en tweets**.

La estructura real condiciona el alcance:

- Training: solo negativo (`0`) y positivo (`4`).
- Test manual: negativo (`0`), neutral (`2`) y positivo (`4`).
- Por lo tanto, el modelo base natural es **binario**: negativo vs positivo.
- La clase neutral puede tratarse como extension mediante una estrategia de incertidumbre.

## Propuesta recomendada

### Objetivo principal

Entrenar un modelo que prediga si un tweet expresa sentimiento negativo o positivo.

### Objetivo secundario

Interpretar el lenguaje del corpus para entender que palabras, topicos o relaciones semanticas caracterizan cada polaridad.

## Minimo defendible

Este seria el camino mas seguro para cumplir bien la consigna:

1. Cargar todos los datos.
2. Hacer EDA:
   - distribucion de clases;
   - longitud de tweets;
   - palabras frecuentes por clase;
   - ejemplos por clase.
3. Preprocesar texto:
   - minusculas;
   - limpieza de URLs;
   - reemplazo o limpieza de menciones;
   - manejo de hashtags;
   - normalizacion basica.
4. Entrenar modelo base:
   - `TfidfVectorizer`;
   - Logistic Regression o Linear SVM.
5. Evaluar:
   - accuracy;
   - precision;
   - recall;
   - F1-score;
   - matriz de confusion.
6. Interpretar:
   - palabras con mayor peso para positivo;
   - palabras con mayor peso para negativo;
   - ejemplos de errores.
7. Usar una metrica vista en clase:
   - similitud coseno entre vectores TF-IDF de tweets;
   - o similitud coseno entre embeddings de palabras.

## Ideas de extension

### 1. Neutral por umbral de incertidumbre

Como el training no tiene clase neutral, se puede entrenar un clasificador binario y definir:

```text
si P(positivo) esta cerca de 0.5 -> neutral
si P(positivo) es alta -> positivo
si P(positivo) es baja -> negativo
```

Utilidad:

- Permite usar el test manual con clase neutral.
- Convierte el problema binario en una aproximacion a tres clases.

Riesgo:

- Neutral no se aprende directamente.
- El umbral debe justificarse.

### 2. Topicos por sentimiento

Objetivo:

- Identificar temas frecuentes en tweets positivos y negativos.

Metodos posibles:

- palabras frecuentes por clase;
- bigramas/trigramas;
- TF-IDF por clase;
- LDA;
- clustering de tweets vectorizados.

Salida posible:

- top palabras positivas;
- top palabras negativas;
- wordcloud por clase;
- topicos interpretados manualmente.

### 3. Embeddings entrenados sobre tweets

Objetivo:

- Aprender relaciones semanticas del propio corpus.

Metodos:

- Word2Vec;
- FastText.

Analisis:

- palabras similares a `love`, `happy`, `great`;
- palabras similares a `hate`, `sad`, `bad`;
- similitud coseno entre terminos positivos y negativos;
- analogias simples.

Utilidad:

- Sirve para interpretar lenguaje del dataset.
- Puede mostrar asociaciones que no aparecen mirando solo frecuencias.

### 4. Comparar embeddings positivos vs negativos

Idea:

- Entrenar un embedding con tweets positivos.
- Entrenar otro embedding con tweets negativos.
- Comparar el contexto de una misma palabra en ambos modelos.

Ejemplo conceptual:

```text
phone en positivos -> love, new, great
phone en negativos -> broken, died, problem
```

Utilidad:

- Muestra como cambia el contexto de una palabra segun polaridad.
- Es una extension interesante y explicable.

Riesgo:

- Requiere cuidar que ambos modelos tengan vocabularios comparables.

### 5. Sarcasmo como analisis de errores

No conviene prometer un detector completo de sarcasmo.

Si conviene usarlo como analisis de limitacion:

- buscar tweets negativos con palabras positivas;
- revisar falsos positivos y falsos negativos;
- identificar frases ironicas;
- explicar por que el modelo falla.

Ejemplo:

```text
Great, my phone died again. Amazing.
```

Utilidad:

- Enriquece la conclusion.
- Muestra criterio critico sobre limitaciones de analisis de sentimiento.

### 6. Visualizacion con UMAP o PCA

Objetivo:

- Visualizar separacion entre tweets positivos y negativos.

Opciones:

- reducir vectores TF-IDF;
- reducir embeddings promedio por tweet;
- graficar puntos coloreados por target.

Riesgo:

- Con 1.600.000 tweets puede ser pesado.
- Se puede entrenar/modelar con todos los datos y usar visualizacion agregada o una proyeccion calculada cuidadosamente.
- Si se usa una muestra solo para visualizacion, aclarar que no corresponde al entrenamiento/evaluacion final.

## Recomendacion final de alcance

Para maximizar calidad sin sobredimensionar:

1. Modelo base TF-IDF + Logistic Regression usando todos los datos.
2. Interpretacion de features positivas/negativas.
3. Similitud coseno entre tweets o palabras.
4. Topicos/keywords por sentimiento.
5. Analisis breve de errores y sarcasmo.

Embeddings y analogias pueden quedar como extension si el tiempo alcanza.
