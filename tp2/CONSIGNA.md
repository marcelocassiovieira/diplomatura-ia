# Trabajo Practico N° 2 - Consigna

## Trabajo Practico 2 - Modulo 2

Llegamos al final del modulo 2 y estamos en condiciones de analizar un dataset, entrenar un modelo de clasificacion y evaluar sus resultados.

## Objetivo del Proyecto

El objetivo de este trabajo practico es construir, entrenar y validar un modelo de Machine Learning capaz de predecir si una persona fuma o no, utilizando la variable objetivo `smoking`.

Para lograrlo, deberan seguir un flujo de trabajo completo de ciencia de datos:

1. **Entrenamiento y validacion:** utilizar el dataset etiquetado, que contiene aproximadamente 50.000 registros, para entrenar y validar el modelo.
2. **Prediccion sobre datos nuevos:** utilizar el modelo entrenado y el mismo pipeline de preparacion de datos para procesar el segundo dataset, que no contiene la variable objetivo.
3. **Generacion de predicciones:** generar un archivo final con dos columnas: `id` y `smoking`. La columna `smoking` debe contener valores `0` o `1`, donde:
   - `0`: persona no fumadora.
   - `1`: persona fumadora.

## Conjuntos de Datos

- **Dataset etiquetado para entrenamiento y validacion:** https://docs.google.com/spreadsheets/d/1335AaFI1WufJkv56b9u-JwdLKifenolp/edit?pli=1&gid=1669368870#gid=1669368870
- **Dataset sin etiquetar para prediccion final:** https://docs.google.com/spreadsheets/d/1dpTMd0R0-YJ6psx8egWNR-IL5g6QPraL/edit?gid=759094407#gid=759094407

La limpieza, transformacion y preparacion de datos debe definirse a partir del dataset de entrenamiento. Luego, ese mismo proceso debe aplicarse al dataset sin etiquetar para generar las predicciones finales.

Todo lo trabajado en el TP1 sobre limpieza, analisis y preparacion de datos tambien debe aplicarse en este trabajo. Esto incluye revisar calidad de datos, tipos de variables, valores faltantes, duplicados, inconsistencias, outliers, distribuciones, relaciones entre variables y cualquier transformacion necesaria antes de entrenar el modelo.

Tambien se espera que el trabajo refleje los contenidos y criterios vistos durante las clases del modulo: buenas practicas de exploracion, preparacion de datos, separacion entrenamiento/validacion, seleccion de metricas, entrenamiento de modelos, validacion, comparacion de resultados y comunicacion clara de hallazgos.

## Etapas Esperadas

El trabajo debe incluir, como minimo, las siguientes etapas:

1. Lectura y carga de datos.
2. Analisis exploratorio de datos (**EDA obligatorio**).
3. Limpieza y tratamiento de datos faltantes, duplicados, outliers o inconsistencias, siguiendo las practicas trabajadas en el TP1.
4. Preparacion de features.
5. Separacion de datos de entrenamiento y validacion.
6. Entrenamiento de uno o mas modelos de clasificacion.
7. Validacion del modelo elegido.
8. Comparacion de metricas y justificacion de la seleccion final.
9. Prediccion sobre el dataset sin etiquetar.
10. Exportacion del archivo final con las columnas `id` y `smoking`.

Todo el codigo debe ser reproducible. Deben utilizar semillas fijas en las operaciones aleatorias, por ejemplo en separacion train/test, modelos y validacion cruzada.

El codigo que genera las predicciones finales sera ejecutado por el profesor. Por este motivo, debe poder correr de punta a punta sin modificaciones manuales, utilizando rutas relativas dentro del repositorio, dependencias declaradas en `requirements.txt` y una salida final deterministica.

## Formato de Entrega y Requisitos

La entrega debe simular un entorno de trabajo real. Se espera un trabajo lo mas profesional posible: ordenado, reproducible, documentado, trazable y sin errores de ejecucion.

El objetivo no es solamente obtener una buena metrica, sino tambien demostrar buenas practicas de trabajo en ciencia de datos:

- Codigo claro, legible y organizado.
- Uso de semillas para garantizar reproducibilidad.
- Separacion clara entre datos crudos, datos procesados, notebooks, modelos y resultados.
- Mismo pipeline de preprocesamiento para entrenamiento y prediccion final.
- Justificacion de decisiones tecnicas.
- Registro de descubrimientos, pruebas realizadas y conclusiones.
- Entrega final facil de ejecutar por otra persona.

### 1. Repositorio de GitHub

Deberan entregar el enlace a un repositorio publico que contenga todo el proyecto.

### 2. Estructura del Proyecto

El repositorio debe estar organizado de la siguiente manera:

```text
tp2/
├── data/
│   ├── raw/          # Datos originales, tal como se descargaron.
│   ├── processed/    # Datos limpios y procesados listos para modelar.
│   └── external/     # Cualquier otro dato externo utilizado.
├── imgs/             # Imagenes, graficos o capturas usadas en la presentacion.
├── models/           # Modelos entrenados y guardados, por ejemplo .pkl o .joblib.
│   ├── DTCs/         # Ejemplo: modelos de arbol de decision.
│   └── XGBOOSTs/     # Ejemplo: modelos XGBoost.
├── notebooks/        # Notebooks del proyecto.
│   ├── 01_lectura_y_discovery.ipynb
│   ├── 02_eda.ipynb
│   ├── 03_preprocesamiento.ipynb
│   ├── 04_entrenamiento_y_optimizacion.ipynb
│   ├── 05_validacion.ipynb
│   └── 06_prediccion.ipynb
├── README.md
├── requirements.txt # Listado de librerias necesarias para ejecutar el proyecto.
└── CONSIGNA.md
```

La estructura puede adaptarse si el equipo lo considera necesario, pero debe mantenerse clara, profesional y facil de ejecutar.

### 3. README.md

El repositorio debe incluir un archivo `README.md` claro y detallado que documente:

- Descripcion del proyecto y objetivo.
- Descripcion de los datasets utilizados.
- Variable objetivo.
- Estructura del repositorio.
- Pasos para instalar dependencias.
- Pasos para ejecutar notebooks o scripts.
- Resumen del flujo de trabajo realizado.
- Principales descubrimientos del analisis exploratorio.
- Decisiones tomadas durante la limpieza y el preprocesamiento.
- Features utilizadas y transformaciones aplicadas.
- Modelos entrenados y comparacion entre ellos.
- Explicacion resumida del modelo elegido.
- Metricas obtenidas.
- Conclusiones finales.
- Limitaciones conocidas o posibles mejoras.
- Instrucciones para reproducir las predicciones finales.

El README debe funcionar como una guia completa del proyecto: una persona externa debe poder entender que se hizo, por que se tomaron esas decisiones, cuales fueron los principales hallazgos y como reproducir el resultado final.

### 4. Notebooks

El trabajo debe incluir notebooks ordenadas logicamente. La notebook final de prediccion debe contener el codigo que genera las predicciones sobre el dataset sin etiquetar y exporta el archivo resultante con las columnas `id` y `smoking`.

Todos los notebooks deben ejecutarse sin errores.

La notebook o script de prediccion final debe ser especialmente cuidada, ya que sera ejecutada por el profesor para validar la entrega. Debe cargar los datos, aplicar el mismo preprocesamiento usado durante el entrenamiento, cargar o entrenar el modelo segun corresponda y generar el archivo final sin requerir pasos manuales adicionales.

### 5. Requirements

El archivo `requirements.txt` debe incluir el listado de librerias utilizadas en el proyecto, con sus versiones cuando sea posible. Por ejemplo:

```text
pandas
numpy
scikit-learn
matplotlib
seaborn
xgboost
joblib
jupyter
```

Este archivo debe permitir recrear el entorno de ejecucion del proyecto mediante:

```bash
pip install -r requirements.txt
```

### 6. Presentacion

La entrega debe incluir una presentacion que resuma:

- Problema a resolver.
- Datasets utilizados.
- Principales hallazgos del analisis exploratorio.
- Decisiones de limpieza y preprocesamiento.
- Modelos evaluados.
- Modelo final seleccionado.
- Metricas de validacion.
- Conclusiones.

## Metrica de Exito

La metrica principal para evaluar el rendimiento del modelo sera el **F1-Score para la clase 1**, correspondiente a personas fumadoras.

El resultado final se evaluara sobre las predicciones generadas para el segundo dataset, que no contiene la variable objetivo.

Ademas, se podra utilizar un **leaderboard** o ranking comparativo entre trabajos, calculado a partir de la metrica definida sobre el dataset de evaluacion final. Este ranking permitira comparar el rendimiento de los modelos entregados, pero no reemplaza la evaluacion de la calidad general del trabajo, la documentacion, la reproducibilidad y las decisiones tomadas durante el proceso.

## Fecha de Entrega

La fecha de entrega es el **23 de junio**.

## Entregables

Deberan entregar:

- Link al repositorio publico de GitHub.
- Codigo completo y ejecutable sin errores.
- `README.md` completo.
- Notebooks del flujo de trabajo.
- Modelo entrenado, si corresponde.
- Archivo final con las columnas `id` y `smoking`.
- Presentacion del trabajo.
