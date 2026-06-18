# TP2 - Modulo 2: Prediccion de fumadores (`smoking`)

Trabajo Practico 2 de la Diplomatura en Inteligencia Artificial. El objetivo es predecir si una persona fuma o no a partir de variables biometricas y de laboratorio.

> Convencion del proyecto: todo en castellano sin acentos ni egnes.

> Los notebooks fueron ejecutados de punta a punta; las metricas reportadas corresponden a esa corrida con semilla `SEED = 42`.

## Objetivo

Predecir si una persona fuma (`smoking` = 1) o no (`smoking` = 0). La metrica principal es el **F1-Score de la clase 1** (fumadores), que es la que se usa para el ranking entre trabajos.

## Datasets

| Dataset | Archivo | Filas | Columnas | Uso |
|---|---|---|---|---|
| Etiquetado | `data/raw/smoking_prediction.xlsx` | ~50.000 | 27 (incluye `smoking`) | Entrenamiento y validacion |
| Sin etiquetar | `data/raw/smoking_prediction_entrega.xlsx` | ~5.692 | 26 (sin `smoking`) | Prediccion final |

Variables: `id`, datos demograficos (`gender`, `age`), antropometria (`height_cm`, `weight_kg`, `waist_cm`), vision/audicion (`eyesight_*`, `hearing_*`), presion (`systolic`, `relaxation`), panel de laboratorio (`fasting_blood_sugar`, `cholesterol`, `triglyceride`, `hdl`, `ldl`, `hemoglobin`, `urine_protein`, `serum_creatinine`, `ast`, `alt`, `gtp`), salud dental (`dental_caries`, `tartar`) y `oral`.

**Variable objetivo:** `smoking` (0 = no fuma, 1 = fuma).

## Estructura del repositorio

```
tp2/
├── data/
│   ├── raw/          # Datos originales (.xlsx).
│   ├── processed/    # CSVs procesados, splits de validacion y predicciones.
│   └── external/     # Sin uso en este TP.
├── imgs/             # Graficos del EDA y de la validacion.
├── models/
│   ├── DTCs/         # Carpeta reservada para arboles de decision.
│   ├── XGBOOSTs/     # Pipeline de XGBoost.
│   ├── best_model.joblib          # Modelo final.
│   ├── decision_threshold.json    # Threshold optimo.
│   └── cv_results.csv             # Resultados del entrenamiento.
├── notebooks/
│   ├── utils.py                       # Semilla, rutas y funciones compartidas.
│   ├── 01_lectura_y_discovery.ipynb
│   ├── 02_eda.ipynb
│   ├── 03_preprocesamiento.ipynb
│   ├── 04_entrenamiento_y_optimizacion.ipynb
│   ├── 05_validacion.ipynb
│   └── 06_prediccion.ipynb
├── README.md
├── requirements.txt
└── CONSIGNA.md
```

## Instalacion

```bash
python -m venv .venv
source .venv/bin/activate          # en Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Ejecucion

Los notebooks estan numerados y hay que correrlos en orden porque cada uno usa los archivos que genera el anterior.

```bash
cd notebooks
jupyter lab            # o: jupyter notebook
```

Ejecutar en orden: `01` -> `02` -> `03` -> `04` -> `05` -> `06`.

Para **reproducir solo las predicciones** (con el modelo ya entrenado): ejecutar directamente `notebooks/06_prediccion.ipynb`. Genera `data/processed/predicciones_smoking.csv` con columnas `id` y `smoking_prediction`.

## Flujo de trabajo

1. **01 - Lectura y discovery**: carga los dos datasets, les da formato (snake_case, tipos correctos) y hace un primer reconocimiento de los datos (nulos, duplicados, columnas constantes, balance del target).
2. **02 - EDA**: distribuciones, correlaciones con el target, analisis por categorias. Las figuras se guardan en `imgs/`.
3. **03 - Preprocesamiento**: define la receta de transformacion (imputacion, one-hot) pero sin aplicarla todavia. El ajuste ocurre en el paso 4, solo con datos de entrenamiento.
4. **04 - Entrenamiento y optimizacion**: separacion train/validacion, busqueda de hiperparametros de XGBoost con validacion cruzada optimizando F1 de clase 1.
5. **05 - Validacion**: evaluacion en el set de validacion, ajuste del threshold y graficos de curvas ROC/PR e importancia de variables.
6. **06 - Prediccion**: aplica el modelo a los datos sin etiquetar y exporta `predicciones_smoking.csv`.

## Principales hallazgos del EDA

- El target tiene un desbalance leve: 63% no fuma, 37% fuma. No es extremo pero hay que tenerlo en cuenta.
- `oral` vale siempre "Y" en todos los registros, no aporta nada.
- `hearing_left` y `hearing_right` casi no varian (95% tiene el mismo valor).
- Las variables mas correlacionadas con fumar son `hemoglobin`, `gtp`, `triglyceride`, `height_cm` y `gender`. En este dataset los fumadores tienden a ser hombres.
- Las variables de laboratorio tienen valores extremos marcados pero no los eliminamos (ver decision abajo).

Figuras en `imgs/`: `dist_target.png`, `hist_numericas.png`, `boxplots_labs.png`, `corr_heatmap.png`, `bivariado_categoricas.png`, `kde_predictores.png`.

## Decisiones de limpieza y preprocesamiento

- El Excel trae unas 200 filas vacias al final que se eliminan al cargar.
- Sacamos `id` (solo es un numero de fila) y `oral` (constante).
- Renombramos columnas a snake_case para trabajar mas comodo (`height(cm)` -> `height_cm`, etc.).
- Imputamos faltantes con mediana para numericas y moda para categoricas, calculando esos valores solo con los datos de entrenamiento.
- No eliminamos outliers: XGBoost los tolera bien y no hay una forma limpia de replicar esa eliminacion en el set de prediccion.
- `gender` y `tartar` son texto y las convertimos a numeros con one-hot encoding.
- Todo el preprocesamiento esta dentro del pipeline para que no haya riesgo de contaminar la validacion o la prediccion con informacion del entrenamiento.

## Features y transformaciones

Se usan todas las columnas menos `id`, `oral` y `smoking`. Ademas creamos 8 variables nuevas combinando las originales con logica biomedica:

| Variable | Calculo | Por que |
|---|---|---|
| `bmi` | peso / altura^2 | Indice de masa corporal. |
| `waist_to_height` | cintura / altura | Marcador de grasa abdominal. |
| `pulse_pressure` | sistolica - diastolica | Indicador cardiovascular. |
| `map` | diastolica + (sist - diast)/3 | Presion arterial media. |
| `ast_alt_ratio` | ast / alt | Indice de De Ritis, relacionado con el higado. |
| `non_hdl` | colesterol - hdl | Fraccion de colesterol "malo". |
| `tg_hdl_ratio` | trigliceridos / hdl | Proxy de resistencia a la insulina. |
| `liver_enzymes_sum` | ast + alt + gtp | Carga total de enzimas hepaticas. |

Estas variables se calculan fila por fila a partir de columnas existentes, asi que no generan ninguna filtracion de informacion entre conjuntos. La mejora en F1 fue pequegna (el modelo ya encontraba algunas de estas relaciones solo), pero varias quedaron entre las mas usadas segun la feature importance.

## Modelos evaluados y comparacion

Evaluamos tres modelos con validacion cruzada de 5 folds, optimizando F1 de clase 1:

| Modelo | F1 clase 1 (CV) | Notas |
|---|---|---|
| **XGBoost** | **0.7301** | `scale_pos_weight` para el desbalance, `tree_method='hist'`. |
| LogisticRegression | 0.7058 | Baseline lineal, `class_weight='balanced'`. |
| DecisionTree | 0.7018 | Baseline de arbol, `class_weight='balanced'`. |

Elegimos **XGBoost** por tener el mejor F1 tanto en validacion cruzada como en el hold-out. Es un ensamble de arboles que tolera bien los valores extremos del panel de laboratorio y no necesita que las variables esten en la misma escala.

## Metricas obtenidas

Evaluacion de XGBoost en el hold-out de validacion (20% de los datos, 10.000 registros):

| Metrica | Valor |
|---|---|
| F1 clase 1 (threshold 0.50) | 0.7348 |
| F1 clase 1 (threshold optimo) | **0.742** |
| Threshold optimo | 0.4248 |
| ROC-AUC | 0.8745 |
| PR-AUC | 0.7795 |
| Accuracy | 0.7757 |
| Precision clase 1 | 0.6415 |
| Recall clase 1 | 0.8797 |

Bajar el threshold de 0.50 a 0.4248 hace que el modelo sea mas agresivo detectando fumadores, lo que sube el F1. El recall de 0.88 significa que el modelo detecta casi 9 de cada 10 fumadores reales.

Sobre los 5.692 registros sin etiquetar el modelo predice 53% no fumadores y 47% fumadores. El resultado esta en `data/processed/predicciones_smoking.csv` con columnas `id` y `smoking_prediction`.

## Conclusiones

- XGBoost con hiperparametros optimizados logra un F1 de clase 1 de 0.742 y un ROC-AUC de 0.875 en el set de validacion.
- Las variables mas usadas por el modelo son `ast_alt_ratio`, `hemoglobin`, `triglyceride` y `fasting_blood_sugar`, lo que tiene sentido biologico con el tabaquismo.
- El pipeline queda serializado y puede aplicarse a datos nuevos sin reentrenar nada.

## Limitaciones y posibles mejoras

- El threshold lo ajustamos sobre el mismo set de validacion, asi que esa mejora de 0.7348 a 0.742 es un poco optimista.
- Las variables de laboratorio vienen en una escala que no corresponde a sus unidades clinicas reales, lo que limita la interpretacion de los valores absolutos.
- Se podria explorar LightGBM, calibracion de probabilidades o una busqueda de hiperparametros mas amplia para mejorar el F1.

## Reproducir las predicciones

1. `pip install -r requirements.txt`
2. Ejecutar `notebooks/06_prediccion.ipynb`.
3. El resultado queda en `data/processed/predicciones_smoking.csv`.

Para reentrenar desde cero, ejecutar primero los notebooks `01` a `05`. Toda la aleatoriedad esta fijada con `SEED = 42`.
