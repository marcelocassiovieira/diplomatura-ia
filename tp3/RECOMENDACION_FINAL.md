# TP3 - Recomendacion final de alcance

## Enfoque elegido

El TP3 se enfocara en construir un **clasificador binario de sentimiento en tweets** usando todos los datos disponibles del archivo de entrenamiento.

La tarea principal sera:

```text
tweet -> sentimiento negativo o positivo
```

Esto es lo mas consistente con el dataset, porque el archivo de entrenamiento contiene solamente dos clases:

- `0`: negativo;
- `4`: positivo.

La clase neutral (`2`) aparece en el archivo de test manual, pero no aparece en el training. Por eso no conviene plantear el modelo principal como clasificador de tres clases.

## Objetivo general

Desarrollar un flujo de NLP que permita predecir la polaridad de tweets y explicar que patrones del lenguaje diferencian tweets positivos y negativos.

## Objetivos especificos

- Cargar y validar los dos archivos del dataset.
- Confirmar el uso completo del dataset de entrenamiento.
- Realizar EDA basico sobre clases, longitud de textos y palabras frecuentes.
- Preprocesar los tweets.
- Entrenar un modelo base de clasificacion de sentimiento.
- Evaluar el modelo con metricas de clasificacion.
- Interpretar que palabras, topicos o patrones explican cada polaridad.
- Incorporar al menos una metrica vista en clase, preferentemente similitud coseno.
- Analizar errores y limitaciones, incluyendo ambiguedad y posible sarcasmo.

## Modelo recomendado

### Baseline principal

Usar:

```text
TF-IDF + Logistic Regression
```

Motivo:

- Es eficiente para 1.600.000 tweets.
- Funciona bien con texto corto.
- Es interpretable.
- Permite extraer palabras con mayor peso positivo y negativo.
- Es mas facil de defender que un modelo complejo.

### Alternativas si se quiere comparar

- `TF-IDF + Linear SVM`
- `Bag of Words + Naive Bayes`

Estas alternativas pueden agregarse solo si hay tiempo.

## Componentes mandatorios

### 1. Carga de datos

- Leer training y test manual.
- Asignar nombres de columnas:
  - `target`;
  - `id`;
  - `date`;
  - `query`;
  - `user`;
  - `text`.
- Confirmar cantidad de filas.
- Confirmar distribucion de clases.
- Dejar explicito que el entrenamiento final usa todos los datos.

### 2. EDA

Analisis minimo:

- Distribucion de `target`.
- Longitud de tweets en caracteres y palabras.
- Ejemplos de tweets positivos y negativos.
- Palabras frecuentes por clase.
- Frecuencia de menciones, URLs y hashtags.
- Duplicados y posible ruido de etiquetas.

### 3. Preprocesamiento

Minimo recomendado:

- Pasar texto a minusculas.
- Reemplazar URLs por token especial o eliminarlas.
- Reemplazar menciones `@usuario` por token especial o eliminarlas.
- Decidir tratamiento de hashtags.
- Mantener o tratar negaciones con cuidado (`not`, `can't`, `don't`), porque son importantes para sentimiento.

No conviene limpiar agresivamente al punto de perder informacion emocional.

### 4. Entrenamiento

- Vectorizar con `TfidfVectorizer`.
- Usar `ngram_range=(1, 2)` si los recursos lo permiten.
- Usar split estratificado con mezcla aleatoria, porque el archivo esta ordenado por clase.
- Entrenar Logistic Regression.

Importante:

```text
No hacer split secuencial.
```

El dataset tiene primero todos los negativos y despues todos los positivos.

### 5. Evaluacion

Reportar:

- accuracy;
- precision;
- recall;
- F1-score;
- matriz de confusion.

Tambien conviene mostrar algunos ejemplos de:

- falsos positivos;
- falsos negativos.

Eso permite conectar metricas con interpretacion.

### 6. Metrica vista en clase

Usar **similitud coseno**.

Opciones:

- similitud coseno entre tweets vectorizados con TF-IDF;
- similitud coseno entre palabras usando embeddings;
- similitud entre tweets positivos y negativos promedio.

Recomendacion:

- Usar similitud coseno sobre vectores TF-IDF para mostrar tweets parecidos.
- Es simple, directo y conectado con la vectorizacion del modelo.

### 7. Interpretacion

Interpretar:

- palabras con mayor peso positivo;
- palabras con mayor peso negativo;
- top keywords por clase;
- diferencias entre palabras frecuentes y palabras realmente predictivas.

Esto es importante porque un buen TP no deberia quedarse solo en metricas.

## Extensiones recomendadas

### A. Topicos / keywords por sentimiento

Agregar analisis de topicos liviano:

- top palabras por clase;
- top bigramas por clase;
- TF-IDF promedio por clase;
- wordcloud por sentimiento si suma visualmente.

Objetivo:

- Entender de que hablan los tweets positivos y negativos.

### B. Analisis de errores y sarcasmo

No construir un detector de sarcasmo completo.

Usar sarcasmo como limitacion:

- revisar tweets mal clasificados;
- buscar positivos literales usados en contexto negativo;
- mostrar casos ambiguos;
- explicar por que el modelo puede fallar.

Ejemplo conceptual:

```text
Great, my phone died again. Amazing.
```

### C. Neutral como caso especial

El test manual tiene clase neutral, pero el training no.

Opcion:

- entrenar modelo binario;
- usar probabilidad cercana a `0.5` como zona de incertidumbre;
- clasificar esa zona como neutral solo a modo exploratorio.

Esto debe presentarse como extension, no como modelo principal.

## Extensiones opcionales si sobra tiempo

### Embeddings y analogias

Se puede entrenar Word2Vec o FastText sobre los tweets para analizar:

- palabras similares a `love`, `happy`, `great`;
- palabras similares a `hate`, `sad`, `bad`;
- asociaciones entre marcas/productos y sentimiento;
- analogias simples.

Utilidad:

- Interpretar el lenguaje del corpus.
- Mostrar relaciones semanticas aprendidas.

Riesgo:

- Puede consumir tiempo.
- No necesariamente mejora el clasificador principal.

Por eso queda como extension optativa.

### UMAP o PCA

Se puede usar para visualizar tweets o palabras en 2D.

Riesgo:

- Puede ser pesado con todos los datos.
- Si se usa una muestra para visualizacion, hay que aclarar que es solo visual y que el entrenamiento/evaluacion final usa todos los datos.

## Fuera de alcance

- Detector completo de sarcasmo.
- Modelo profundo entrenado desde cero.
- API o sistema productivo.
- Clasificador principal de tres clases entrenado desde cero, porque falta neutral en training.
- Reportar resultados finales usando muestras.

## Narrativa sugerida para la presentacion

1. **Problema**
   - Queremos clasificar sentimiento en tweets.

2. **Datos**
   - Dataset grande, 1.600.000 tweets de training.
   - Training balanceado: negativo vs positivo.
   - Test manual tiene neutral, pero training no.

3. **Decisiones**
   - Modelo principal binario.
   - TF-IDF por eficiencia e interpretabilidad.
   - Logistic Regression como baseline robusto.
   - Uso de todos los datos por requisito mandatorio.

4. **Resultados**
   - Metricas del modelo.
   - Matriz de confusion.
   - Palabras mas predictivas.

5. **Interpretacion**
   - Que lenguaje caracteriza sentimientos positivos y negativos.
   - Similitud coseno para tweets/palabras parecidas.
   - Keywords o topicos principales.

6. **Limitaciones**
   - Neutral no esta en training.
   - Sarcasmo y ambiguedad.
   - Ruido de etiquetas y duplicados conflictivos.

7. **Mejoras futuras**
   - Modelos preentrenados.
   - Mejor tratamiento de neutral.
   - Embeddings por sentimiento.
   - Analisis mas profundo de sarcasmo.

## Decision final recomendada

Hacer:

```text
TF-IDF + Logistic Regression + interpretacion + similitud coseno + topicos/keywords + errores
```

No hacer como nucleo principal:

```text
sarcasmo completo, deep learning pesado, embeddings como modelo principal, clasificacion real de 3 clases
```

Esta combinacion cumple la consigna, usa todos los datos, es tecnicamente defendible y permite una presentacion clara.
