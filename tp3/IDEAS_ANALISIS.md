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

## Lineas de analisis posibles mas alla de sentimiento

El TP no tiene que quedar limitado a "predecir positivo o negativo". El dataset permite armar varias preguntas complementarias usando texto, usuario, fecha y patrones linguisticos.

### A. Analisis de topicos generales

Pregunta:

```text
De que temas habla el corpus de tweets?
```

Ideas:

- entrenar NMF o LDA sobre tweets limpios;
- identificar topicos globales sin mirar inicialmente la etiqueta de sentimiento;
- despues cruzar cada topico con la polaridad;
- ver si algunos topicos concentran mas negatividad o positividad.

Salida posible:

- topicos principales del corpus;
- palabras representativas por topico;
- proporcion de tweets positivos/negativos dentro de cada topico.

### B. Segmentacion o clustering de tweets

Pregunta:

```text
Existen grupos naturales de tweets con vocabulario parecido?
```

Ideas:

- vectorizar con TF-IDF;
- aplicar clustering sobre una representacion reducida;
- interpretar clusters por palabras frecuentes;
- comparar clusters con sentimiento.

Salida posible:

- grupos de tweets por tema o estilo;
- descripcion manual de cada cluster;
- distribucion de sentimiento por cluster.

### C. Analisis de usuarios

Pregunta:

```text
Hay usuarios con patrones de lenguaje o polaridad distintos dentro del dataset?
```

Ideas:

- calcular cantidad de tweets por usuario;
- medir proporcion de tweets negativos y positivos;
- analizar usuarios con suficiente volumen;
- comparar vocabulario de usuarios mas negativos y mas positivos.

Cuidados:

- no afirmar rasgos psicologicos generales;
- hablar de tendencia observada en este corpus;
- filtrar usuarios con pocos tweets para evitar conclusiones inestables.

### D. Analisis temporal

Pregunta:

```text
Cambia el sentimiento o el vocabulario segun fecha, dia u horario?
```

Ideas:

- parsear la columna `date`;
- analizar volumen de tweets por fecha u hora;
- comparar proporcion de sentimiento por franja horaria;
- detectar momentos con mayor negatividad o positividad.

Salida posible:

- serie temporal de volumen;
- sentimiento promedio por hora/dia;
- top palabras en momentos mas negativos o positivos.

### E. Analisis de lenguaje, estilo y ruido

Pregunta:

```text
Que caracteristicas formales tienen los tweets y como se relacionan con la polaridad?
```

Ideas:

- medir uso de menciones, URLs y hashtags;
- contar signos de exclamacion o interrogacion;
- detectar mayusculas, emoticones o alargamientos de palabras;
- comparar longitud de texto por sentimiento;
- ver si ciertos recursos expresivos aparecen mas en tweets negativos o positivos.

Salida posible:

- features linguisticas simples;
- comparacion por clase;
- explicacion de que senales textuales ayudan o confunden.

### F. Busqueda de tweets similares

Pregunta:

```text
Dado un tweet, que otros tweets se le parecen semanticamente?
```

Ideas:

- usar similitud coseno sobre TF-IDF;
- buscar vecinos mas cercanos;
- comparar si tweets similares comparten sentimiento;
- detectar casos donde tweets parecidos tienen etiquetas distintas.

Salida posible:

- ejemplos de tweets similares;
- analisis de coherencia de etiquetas;
- posibles casos ambiguos o mal etiquetados.

### G. Calidad de etiquetas y casos ambiguos

Pregunta:

```text
Hay tweets dificiles, ambiguos o posiblemente mal etiquetados?
```

Ideas:

- revisar errores del clasificador;
- buscar tweets con probabilidad cercana a 0.5;
- buscar duplicados con etiquetas conflictivas;
- analizar sarcasmo o lenguaje ironico como limitacion.

Salida posible:

- ejemplos de ambiguedad;
- errores representativos;
- discusion sobre limites del analisis automatico.

### H. Comparacion de representaciones

Pregunta:

```text
Que representacion captura mejor los patrones del corpus?
```

Ideas:

- comparar Bag of Words vs TF-IDF;
- comparar unigramas vs unigramas + bigramas;
- opcionalmente entrenar embeddings propios;
- evaluar no solo performance, sino interpretabilidad.

Salida posible:

- comparacion de metricas;
- diferencias en palabras relevantes;
- decision justificada de representacion.

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
- Mezclar analisis de sentimiento con analisis de topicos para entender no solo la polaridad, sino tambien de que se habla en cada polaridad.

Metodos posibles:

- palabras frecuentes por clase;
- bigramas/trigramas;
- TF-IDF por clase;
- NMF sobre matriz TF-IDF;
- LDA;
- clustering de tweets vectorizados.

Salida posible:

- top palabras positivas;
- top palabras negativas;
- topicos negativos y positivos interpretados manualmente;
- wordcloud por clase;
- topicos interpretados manualmente.

Enfoque recomendado:

- Mantener sentimiento como eje principal del TP.
- Usar topicos/keywords como analisis interpretativo complementario.
- Si se entrena un modelo de topicos propio, preferir NMF con TF-IDF por ser mas practico para texto corto e interpretable.

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

### 5. Modelo propio para buscar patrones

Idea:

- Entrenar un modelo propio de sentimiento y usarlo no solo para predecir, sino tambien para descubrir patrones.

Modelo principal:

- `TF-IDF + Logistic Regression`.

Patrones a extraer:

- terminos con mayor peso positivo;
- terminos con mayor peso negativo;
- bigramas predictivos;
- errores frecuentes del modelo;
- diferencias entre palabras frecuentes y palabras realmente utiles para clasificar.

Complemento posible:

- Entrenar NMF o LDA por separado sobre tweets positivos y negativos para obtener topicos dentro de cada polaridad.

### 6. Sarcasmo como analisis de errores

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

### 7. Analisis por usuario: tendencia de polaridad

Idea:

- Usar la columna `user` para agregar tweets por usuario y comparar proporcion de tweets negativos y positivos.

Pregunta posible:

```text
Hay usuarios con mayor proporcion de tweets negativos dentro del dataset?
```

Score simple:

```text
pesimismo_observado = tweets_negativos / total_tweets_del_usuario
```

Cuidados metodologicos:

- Filtrar usuarios con pocos tweets, por ejemplo exigir al menos 5, 10 o 20 tweets.
- No afirmar que una persona "es pesimista" en general.
- Presentarlo como tendencia observada en este corpus.
- Revisar ejemplos de tweets de usuarios extremos para evitar conclusiones automaticas.

Salida posible:

- ranking de usuarios con mayor proporcion negativa;
- ranking de usuarios con mayor proporcion positiva;
- distribucion del score de polaridad por usuario;
- ejemplos anonimizados o tratados con cuidado.

### 8. Visualizacion con UMAP o PCA

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
6. Analisis agregado por usuario como extension, con cautela en la interpretacion.

Embeddings y analogias pueden quedar como extension si el tiempo alcanza.
