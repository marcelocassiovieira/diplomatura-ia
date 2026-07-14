---
marp: true
theme: tp-diplomatura
paginate: true
size: 16:9
---

<!-- _class: cover -->
<!-- _paginate: false -->

# Prediccion de fumadores
## a partir de datos biometricos y de laboratorio

Analisis sobre ~50.000 personas evaluadas en un panel de salud

Marcelo Vieira  |  Diplomatura en Inteligencia Artificial

---

<!-- _class: section -->
<!-- _paginate: false -->

<span class="num">01</span>

# El problema y los datos

---

<!-- _class: content -->

# El problema

<div class="cols">
<div class="text-col">

## Que tenemos que predecir

- Si una persona **fuma o no** (`smoking` = 0/1), a partir de variables biometricas y de un panel de laboratorio.
- 50.000 personas etiquetadas para entrenar, 5.692 sin etiqueta para predecir.

## Como se mide el exito

- **F1-Score de la clase 1** (fumadores), no accuracy.
- El target esta desbalanceado (63% no fuma / 37% fuma): un modelo que dijera siempre "no fuma" tendria 63% de accuracy pero seria inutil.

</div>
<div class="img-col">

![](../imgs/dist_target.png)

</div>
</div>

---

<!-- _class: content -->

# Los datos

<div class="cols">
<div class="text-col">

## Dos archivos

- **Etiquetado**: 50.000 filas, 27 columnas, para entrenar y validar.
- **Sin etiquetar**: 5.692 filas, para la prediccion final.

## Variables

Demograficas, antropometria, presion arterial, panel de laboratorio (colesterol, trigliceridos, enzimas hepaticas) y salud dental.

</div>
<div class="text-col">

## Lo que encontramos al revisar

- El Excel trae ~200 filas vacias al final -> se eliminan.
- `oral` vale siempre "Y" -> no aporta nada, se descarta.
- `hearing_left` / `hearing_right` casi no varian.
- No hay nulos en ninguno de los dos archivos.

</div>
</div>

---

<!-- _class: section -->
<!-- _paginate: false -->

<span class="num">02</span>

# Analisis exploratorio

---

<!-- _class: content -->

# Que variables muestran senales por clase?

<div class="cols">
<div class="img-col">

![](../imgs/corr_heatmap.png)

</div>
<div class="text-col">

## Lo que encontramos

No sacamos conclusiones desde correlacion Pearson contra `smoking`, porque el target es binario.

Usamos distribuciones por clase y tasas por categoria como lectura exploratoria. Se observan diferencias en `hemoglobin`, `gtp`, `triglyceride`, `height_cm`, `weight_kg` y `gender`.

## Como lo usamos

Estas variables quedan como candidatas. La evidencia predictiva se valida despues con el modelo, la matriz de confusion y el F1 de fumadores.

</div>
</div>

---

<!-- _class: content -->

# Las variables de laboratorio tienen valores extremos

<div class="cols">
<div class="img-col">

![](../imgs/boxplots_labs.png)

</div>
<div class="text-col">

## Lo que encontramos

`triglyceride`, `gtp`, `alt` y `ast` tienen colas largas: la mayoria de las personas tiene valores bajos, pero hay un grupo con valores muy altos.

## Que decidimos hacer

No eliminamos esas filas. No seria replicable en el dataset de prediccion, y el modelo que elegimos (XGBoost) tolera bien este tipo de distribucion.

</div>
</div>

---

<!-- _class: content -->

# gender y tartar tambien marcan diferencia

<div class="cols">
<div class="img-col">

![](../imgs/bivariado_categoricas.png)

</div>
<div class="text-col">

## Lo que encontramos

La proporcion de fumadores varia bastante segun `gender` y, en menor medida, segun `tartar` (sarro dental).

## Que podemos hacer

Estas variables categoricas se incorporan al modelo con one-hot encoding, sin perder esta señal.

</div>
</div>

---

<!-- _class: section -->
<!-- _paginate: false -->

<span class="num">03</span>

# Preparacion de los datos

---

<!-- _class: content -->

# Limpieza y transformacion

<div class="cols">
<div class="text-col">

## Decisiones de limpieza

- Sacamos `id` (identificador) y `oral` (constante).
- Renombramos columnas a snake_case.
- Imputamos faltantes con mediana (numericas) y moda (categoricas), calculado solo con datos de entrenamiento.

</div>
<div class="text-col">

## Por que de esta forma

Todo el ajuste vive dentro de un `Pipeline` de scikit-learn que se entrena exclusivamente con el set de entrenamiento. Asi la validacion y la prediccion final no contaminan ningun calculo.

</div>
</div>

---

<!-- _class: content -->

# Variables nuevas con sentido biomedico

<div class="cols">
<div class="text-col">

| Variable | Calculo |
|---|---|
| `bmi` | peso / altura² |
| `waist_to_height` | cintura / altura |
| `pulse_pressure` | sistolica - diastolica |
| `map` | presion arterial media |

</div>
<div class="text-col">

| Variable | Calculo |
|---|---|
| `ast_alt_ratio` | indice de De Ritis |
| `non_hdl` | colesterol - hdl |
| `tg_hdl_ratio` | trigliceridos / hdl |
| `liver_enzymes_sum` | ast + alt + gtp |

<p class="callout">Se calculan fila por fila, sin usar estadisticos globales: no generan ninguna filtracion de informacion entre conjuntos.</p>

</div>
</div>

---

<!-- _class: section -->
<!-- _paginate: false -->

<span class="num">04</span>

# Modelos y resultados

---

<!-- _class: content -->

# Comparamos tres modelos

<div class="cols">
<div class="text-col">

| Modelo | F1 clase 1 (CV) |
|---|---|
| **XGBoost** | **0.7301** |
| Regresion Logistica | 0.7058 |
| Arbol de Decision | 0.7018 |

</div>
<div class="text-col">

## Por que elegimos XGBoost

- Mejor F1 en validacion cruzada y en el hold-out.
- Tolera bien los valores extremos del panel de laboratorio.
- No necesita que las variables esten en la misma escala.
- El desbalance se compensa con `scale_pos_weight`.

</div>
</div>

---

<!-- _class: content -->

# Ajustamos el umbral de decision

<div class="cols">
<div class="img-col">

![](../imgs/threshold_f1.png)

</div>
<div class="text-col">

## Lo que encontramos

Con threshold 0.50 el F1 es 0.7348. Bajando a **0.4248** sube a **0.742**.

## Por que pasa esto

Con clases desbalanceadas, 0.5 rara vez es el punto optimo. Bajar el umbral hace que el modelo detecte mas fumadores (mas recall), que es justo lo que premia el F1 de clase 1.

</div>
</div>

---

<!-- _class: content -->

# Performance en train y validacion

| Threshold | Conjunto | Accuracy | Precision 1 | Recall 1 | F1 1 | ROC-AUC | PR-AUC |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 0.50 | Train | 0.9529 | 0.8925 | 0.9909 | 0.9391 | 0.9964 | 0.9939 |
| 0.50 | Validacion/test | 0.7832 | 0.6661 | 0.8194 | 0.7348 | 0.8745 | 0.7795 |
| 0.4248 | Train | 0.9254 | 0.8329 | 0.9963 | 0.9073 | 0.9964 | 0.9939 |
| 0.4248 | Validacion/test | 0.7757 | 0.6415 | 0.8797 | **0.7420** | 0.8745 | 0.7795 |

La diferencia entre train y validacion/test muestra sobreajuste. Por eso la metrica defendible es la de validacion/test, no la de entrenamiento.

---

<!-- _class: content -->

# Que tan bien distingue el modelo

<div class="cols">
<div class="img-col">

![](../imgs/curvas_roc_pr.png)

</div>
<div class="text-col">

## Lo que encontramos

ROC-AUC = 0.875: muy por encima del azar. PR-AUC = 0.779, muy por encima del baseline (0.37, la proporcion de fumadores).

## Que podemos hacer

Con esta capacidad de ranking, el modelo distingue bien fumadores de no fumadores en todo el rango de thresholds, no solo en el que elegimos.

</div>
</div>

---

<!-- _class: content -->

# Matriz de confusion final

<div class="cols">
<div class="img-col">

![](../imgs/confusion_matrix.png)

</div>
<div class="text-col">

## Metricas con threshold 0.4248

- F1 clase 1: **0.742**
- Precision clase 1: 0.6415
- Recall clase 1: 0.8797
- Accuracy: 0.7757

## Lectura

El modelo detecta casi 9 de cada 10 fumadores reales, a costa de algunas falsas alarmas. Es la decision correcta para maximizar F1.

</div>
</div>

---

<!-- _class: content -->

# Que variables usa mas el modelo

<div class="cols">
<div class="img-col">

![](../imgs/feature_importance.png)

</div>
<div class="text-col">

## Lo que encontramos

`ast_alt_ratio` (una variable que creamos) es la mas usada, seguida de `hemoglobin`, `fasting_blood_sugar` y `triglyceride`.

## Por que es interesante

Varias de las features que creamos (`ast_alt_ratio`, `tg_hdl_ratio`, `waist_to_height`) quedaron entre las mas usadas: el feature engineering aporto señal real, no solo redundancia.

</div>
</div>

---

<!-- _class: section -->
<!-- _paginate: false -->

<span class="num">05</span>

# Conclusiones

---

<!-- _class: content -->

# Conclusiones y proximos pasos

<div class="cols">
<div class="text-col">

## Que logramos

- F1 de clase 1 = **0.742** en validacion, con ROC-AUC de 0.875.
- La performance se reporta en train y validacion/test; train queda mas alto, lo que muestra sobreajuste parcial.
- Pipeline completo serializado: aplicar el modelo a datos nuevos no requiere reentrenar nada.
- Decisiones de preprocesamiento documentadas y sin riesgo de filtracion de datos.

</div>
<div class="text-col">

## Limitaciones y mejoras posibles

- El threshold se ajusto sobre el mismo set de validacion (resultado algo optimista).
- XGBoost sobreajusta parcialmente; se podria regularizar mas o usar una validacion adicional para elegir threshold.
- Las variables de laboratorio no estan en unidades clinicas reales.
- Se podria probar LightGBM, calibracion de probabilidades, o una busqueda de hiperparametros mas amplia.

</div>
</div>

---

<!-- _class: closing -->
<!-- _paginate: false -->

# Gracias

¿Preguntas?

<p class="footer">Marcelo Vieira  |  TP2 — Prediccion de fumadores (smoking)  |  Diplomatura en IA</p>
