# TP3 - EDA preliminar del dataset de tweets

## Archivos

Dataset extraido en:

```text
entregas/tp3/data/raw/
```

Archivos:

- `training.1600000.processed.noemoticon.csv`
- `testdata.manual.2009.06.14.csv`

## Grano del dataset

- Cada fila representa un tweet.
- La variable objetivo es `target`.
- El texto a analizar esta en `text`.

Columnas:

| Columna | Descripcion |
| --- | --- |
| `target` | Polaridad/sentimiento |
| `id` | ID del tweet |
| `date` | Fecha |
| `query` | Query asociada |
| `user` | Usuario |
| `text` | Texto del tweet |

## Tamano

| Archivo | Filas | Columnas | Tamano aproximado |
| --- | ---: | ---: | ---: |
| Training | 1.600.000 | 6 | 228 MB |
| Test manual | 498 | 6 | 0,07 MB |

El training cargado con pandas usa aproximadamente `507 MB` en memoria.

## Distribucion de clases

### Training

| Target | Sentimiento | Filas |
| --- | --- | ---: |
| `0` | Negativo | 800.000 |
| `4` | Positivo | 800.000 |

Hallazgo importante:

- El training esta perfectamente balanceado entre negativo y positivo.
- El training **no tiene clase neutral (`2`)**.
- El archivo esta ordenado por target: primero todos los negativos y despues todos los positivos.
- Por eso, cualquier split debe hacerse con `shuffle=True` o con particion estratificada.

### Test manual

| Target | Sentimiento | Filas |
| --- | --- | ---: |
| `0` | Negativo | 177 |
| `2` | Neutral | 139 |
| `4` | Positivo | 182 |

Hallazgo importante:

- El test manual si tiene clase neutral.
- Como el training no tiene neutral, un modelo supervisado entrenado solo con training no aprende directamente esa clase.
- Para evaluar neutral hay que definir una estrategia especial.

## Calidad de datos

- No hay nulos en ninguna columna.
- `query` en training vale siempre `NO_QUERY`.
- `query` en test contiene temas especificos como `time warner`, `nike`, `kindle2`, `safeway`, etc.
- Hay `659.775` usuarios unicos en training.
- Hay `1.685` IDs duplicados en training.
- Hay `18.534` textos duplicados en training.
- Hay textos repetidos con etiquetas conflictivas: al menos `2.225` textos duplicados aparecen con mas de una etiqueta.

Interpretacion:

- Los duplicados conflictivos muestran ruido de etiquetado.
- No conviene borrar automaticamente sin justificar, porque la consigna exige usar todos los datos.
- Si se tratan duplicados, debe documentarse la decision.
- Una opcion conservadora es mantenerlos para el modelo base y analizar el ruido como limitacion.

## Longitud de tweets

### Training

- Longitud media en caracteres: `74`.
- Mediana: `69`.
- Percentil 95: `136`.
- Maximo: `374`.
- Promedio de palabras: `13`.
- Mediana de palabras: `12`.

Interpretacion:

- Son textos cortos.
- Modelos clasicos con TF-IDF o n-gramas deberian funcionar razonablemente bien.
- La limpieza de URLs, menciones, negaciones y expresiones informales puede impactar mucho.

## Senales del texto en training

| Senal | Cantidad | Porcentaje |
| --- | ---: | ---: |
| URLs | 76.584 | 4,79% |
| Menciones `@usuario` | 738.493 | 46,16% |
| Hashtags | 35.847 | 2,24% |
| Emoticones positivos simples | 9.639 | 0,60% |
| Emoticones negativos simples | 349 | 0,02% |

Interpretacion:

- Las menciones son muy frecuentes.
- Las URLs son poco frecuentes pero conviene limpiarlas.
- Los hashtags son pocos, pero pueden aportar informacion semantica.
- Los emoticones podrian ser una feature util, aunque este dataset fue procesado "noemoticon"; aun asi quedan algunos.

## Palabras frecuentes observadas

En tweets negativos aparecen terminos como:

- `work`
- `miss`
- `sad`
- `can't`
- `don't`
- `still`
- `want`

En tweets positivos aparecen terminos como:

- `good`
- `love`
- `thanks`
- `lol`
- `happy`
- `great`
- `new`

Interpretacion:

- Hay senales lexicas claras para sentimiento.
- Un baseline con TF-IDF + Logistic Regression o Linear SVM deberia ser fuerte.

## Riesgos para el modelado

1. **Clase neutral ausente en training**
   - El modelo base debe ser binario: negativo vs positivo.
   - Si se quiere predecir neutral, se puede usar umbral de incertidumbre.

2. **Training ordenado por clase**
   - No hacer split secuencial.
   - Usar `train_test_split(..., stratify=y, shuffle=True)`.

3. **Test manual pequeno y distinto**
   - Tiene solo 498 filas.
   - Tiene queries tematicas concretas.
   - Puede no representar completamente el training.

4. **Ruido de etiquetas**
   - Hay textos duplicados con targets conflictivos.
   - Esto limita el techo de performance.

5. **Uso mandatorio de todos los datos**
   - No se puede reportar una solucion final con muestra.
   - Se puede usar muestra solo para depurar codigo.

## Implicancias para el alcance

El TP puede tener un alcance solido si se plantea asi:

1. Modelo supervisado binario de sentimiento: negativo vs positivo.
2. Analisis de neutral como caso especial usando el test manual.
3. Analisis interpretativo con topicos, palabras frecuentes, similitud coseno o embeddings.
4. Discusion de errores: sarcasmo, ambiguedad, tweets muy cortos, ruido de etiquetas.
