# Guía de defensa — TP1: Análisis Exploratorio Hotel Bookings

> Documento pensado para que defiendas el trabajo con tus palabras. Cada sección
> incluye **qué decir**, **por qué se hizo así** y **preguntas anticipadas** del jurado.

---

## 0. Apertura (30-60 segundos)

**Qué decir:**
> "El trabajo es un análisis exploratorio sobre el dataset Hotel Bookings, que tiene
> 119.390 reservas de dos hoteles (uno urbano y un resort) entre 2015 y 2017.
> El objetivo no era solo describir los datos, sino responder cinco hipótesis
> elegidas por su utilidad de negocio: cada hipótesis termina en una acción
> concreta de gestión hotelera."

**Por qué arrancar así:** mostrás de entrada que entendiste el problema y que el
análisis tiene un norte (no es "exploré por explorar").

**Si preguntan "¿de dónde sacaste el dataset?":**
> "Es un dataset público muy usado en cursos de data science, originalmente
> publicado en el paper de Antonio, Almeida y Nunes (2019). Lo elegí porque
> combina variables numéricas, categóricas y temporales, y porque el negocio
> hotelero permite traducir cada hallazgo a una decisión clara."

---

## 1. Selección del dataset (consigna 1)

### Qué dice la consigna
Mínimo 50.000 filas, 10 columnas, diversidad de tipos de datos.

### Qué decir
> "El dataset original tiene 119.390 filas y 32 columnas, así que cumple el
> mínimo más del doble en filas y triplicado en columnas. Tiene 16 enteros,
> 4 decimales, 12 categóricas/strings, fechas y variables binarias."

### Por qué se cumple holgadamente
- **Filas:** 119.390 vs 50.000 mínimo → ~2,4×
- **Columnas:** 32 vs 10 mínimo → 3,2×
- **Tipos de datos presentes:**
  - Numéricos enteros: `lead_time`, `adults`, `children`, `booking_changes`...
  - Numéricos decimales: `adr`, `agent`, `company`
  - Categóricos: `hotel`, `meal`, `country`, `market_segment`, `customer_type`...
  - Fechas: `arrival_date_year/month/day`, `reservation_status_date`
  - Binarias: `is_canceled`, `is_repeated_guest`

### Preguntas anticipadas
- **"¿Qué representa cada fila?"** → Una reserva de hotel (no un huésped, no una estancia consumada — una reserva, que puede o no haberse cancelado).
- **"¿Por qué este dataset y no otro?"** → Por tres motivos: cumple ampliamente los mínimos, tiene variedad de tipos, y permite hipótesis con valor de negocio real (cancelaciones, pricing, fidelización).

---

## 2. Hipótesis (consigna 2)

### Qué dice la consigna
Entre 4 y 5 hipótesis de interés.

### Qué decir
> "Planteé cinco hipótesis. Cada una está formulada como una afirmación
> direccional (no una pregunta vaga), está anclada en variables del dataset,
> y termina en una acción de negocio concreta."

### Las cinco hipótesis explicadas

**H1 — El canal de distribución (`market_segment`) predice la cancelación.**
- *Variable usada:* `market_segment` vs `is_canceled`.
- *Razonamiento:* las OTAs (booking, expedia) suelen tener políticas más
  flexibles → el cliente cancela más fácil. Las reservas directas o
  corporativas implican un compromiso mayor.
- *Acción si se confirma:* revisar el mix de canales y la fórmula de margen
  real (no alcanza con la comisión nominal, hay que descontar el churn).

**H2 — A más pedidos especiales, menos cancelación.**
- *Variable usada:* `total_of_special_requests` vs `is_canceled`.
- *Razonamiento:* alguien que se tomó el trabajo de pedir cuna, vista al mar
  o un tipo de cama está mostrando intención real. Es una **proxy de
  compromiso disponible al momento de reservar**.
- *Acción:* scoring en tiempo real → tratar distinto las reservas con 0
  pedidos (recordatorios, ofertas, llamadas).

**H3 — A mayor `lead_time`, mayor cancelación.**
- *Variable usada:* `lead_time` (días entre reserva y llegada) vs `is_canceled`.
- *Razonamiento:* cuanto más lejos está la fecha, más probable que cambien
  los planes del cliente.
- *Acción:* segmentar la cartera de reservas futuras por riesgo y
  planificar overbooking con un % esperado por bin.

**H4 — Los huéspedes repetidos cancelan menos que los nuevos.**
- *Variable usada:* `is_repeated_guest` vs `is_canceled`.
- *Razonamiento:* el cliente repetido ya conoce el hotel y eligió volver.
- *Acción:* justificar inversión en programas de fidelización con métrica
  de retención esperada.

**H5 — El `adr` (precio medio diario) tiene patrón estacional y difiere
entre hoteles.**
- *Variable usada:* `adr` × `arrival_date_month` × `hotel`.
- *Razonamiento:* el resort vive del verano, el hotel urbano de viajes de
  negocios → los picos deberían ser distintos.
- *Acción:* pricing dinámico y revenue management diferenciado por hotel.

### Preguntas anticipadas
- **"¿Por qué estas y no otras?"** → Porque combinan tres criterios: aplicabilidad
  de negocio, variedad de variables (categóricas, numéricas, temporales) y
  posibilidad de respuesta cuantitativa con el dataset.
- **"¿Qué pasaría si una hipótesis no se confirma?"** → También es un hallazgo
  válido. El valor del EDA es la evidencia, no confirmar lo que uno cree.

---

## 3. Carga y limpieza (consigna 3)

### Qué dice la consigna
Importar + chequeo y limpieza: nulos, duplicados, inconsistencias, tipos.

### Qué decir
> "La limpieza fue tan importante como el análisis. El dataset traía
> 26,8% de duplicados y 94% de nulos en una columna. Cualquier KPI calculado
> sobre los datos crudos hubiera estado sesgado."

### Paso a paso

**3.1 — Importación (celda 5e8547bd)**
- `pd.read_csv('../../hotel_bookings.csv')` → 119.390 × 32.
- `df.head()` → primer vistazo.
- `df.dtypes.value_counts()` → confirma diversidad de tipos.
- `df.describe().T` → estadísticos rápidos para detectar valores raros (ej:
  `adr` máximo de 5400 ya delata un outlier).

**3.2 — Nulos (celdas 42073629 y 17778fb5)**

| Columna | Nulos | % | Decisión | Por qué |
|---|---|---|---|---|
| `company` | 112.593 | 94,3% | Reemplazar por 0 | El nulo *significa* "sin empresa", no falta el dato |
| `agent` | 16.340 | 13,7% | Reemplazar por 0 | Mismo razonamiento: reserva sin agente |
| `country` | 488 | 0,4% | `'Unknown'` | Preserva la fila sin asumir país |
| `children` | 4 | <0,01% | Imputar 0 | La mediana es 0, son casos aislados |

**Lo importante para la defensa:** cada decisión está justificada por el
**significado del dato**, no por una regla automática.

**Si preguntan "¿por qué no descartar `company` con 94% nulos?":**
> "Porque ese 94% no es ausencia de dato: significa que la reserva la hizo una
> persona física, no una empresa. Descartarla sería perder la información de
> que el resto sí son reservas corporativas."

**3.3 — Duplicados (celda 58cce33b)**
- 31.994 duplicados (26,8%).
- Decisión: eliminarlos con `drop_duplicates()`.
- Razón: el dataset no tiene un ID único de reserva; filas idénticas
  inflan artificialmente todas las métricas.
- Resultado: 87.396 filas.

**3.4 — Inconsistencias (celda 2977dd55)**

| Inconsistencia | Cantidad | Decisión |
|---|---|---|
| Reservas con 0 huéspedes (adults+children+babies=0) | 166 | Eliminar — no tienen sentido de negocio |
| `adr` negativo | 1 | Eliminar — precio negativo inválido |
| `adr > 1000` | 1 | Eliminar — outlier extremo no realista |

**Resultado final: 87.228 filas** (de 119.390 originales).

**3.5 — Tipos y variables auxiliares (celda fce3e987)**
- Construyo `arrival_date` (datetime) combinando año, mes y día → habilita
  análisis temporales.
- Convierto `reservation_status_date` a datetime.
- Ordeno `arrival_date_month` como categórica ordenada (enero→diciembre)
  → los gráficos salen en orden cronológico, no alfabético.
- Creo `total_nights` (= weekend + week nights) y `total_guests`
  (= adults + children + babies).

**Si preguntan "¿por qué crear `total_nights` y `total_guests`?":**
> "Para que el análisis hable el lenguaje del negocio. Hotelería piensa en
> 'noches' y 'huéspedes', no en cuatro columnas separadas."

### Preguntas anticipadas adicionales
- **"¿Cómo verificaste que la limpieza funcionó?"** → `df.isnull().sum().sum()`
  devolvió 0 al final, y el conteo de filas se reportó en cada paso
  (119.390 → 87.396 → 87.228).
- **"¿No es mucho perder el 27% de las filas?"** → Sí, pero lo perdido eran
  duplicados literales, no observaciones distintas. La información de
  negocio se preserva.

---

## 4. EDA (consigna 4)

### Qué dice la consigna
Tipos, distribuciones, outliers, correlaciones. Mínimo: 3 histogramas + KDE,
3 boxplots, 2 scatterplots, 3 visualizaciones adicionales.

### Qué decir
> "El EDA está organizado en cinco subsecciones que cubren los cuatro ejes
> pedidos. En total son 14 visualizaciones, 11 era el mínimo."

### 4.1 Tipos de variables (celda 505104f7)

Tabla con tres columnas: tipo, cantidad de valores únicos, ejemplo.
- Sirve para detectar variables categóricas con muchos niveles
  (`country` tiene 178 únicos → cuidado con dummy variables).
- También para confirmar los binarios (`is_canceled`, `is_repeated_guest`
  tienen 2 únicos).

### 4.2 Histogramas con KDE — distribuciones (celda 86bc60f6)

**Tres distribuciones clave de las hipótesis:**

1. **`lead_time`** → fuerte sesgo a la derecha. La mayoría reserva con poca
   anticipación, pero hay cola larga (gente que reserva con +6 meses).
2. **`adr`** → concentrado entre €50 y €150, cola derecha (reservas premium).
3. **`total_nights`** → preferencia por estadías cortas (1-4 noches).

**¿Qué es KDE?** Kernel Density Estimation. Es la curva suave encima del
histograma. Estima la distribución continua de la variable → permite ver
la forma sin depender del tamaño de los bins.

**Si preguntan "¿por qué estas tres y no otras?":**
> "Son las tres variables que más uso en las hipótesis: lead_time en H3,
> adr en H5, total_nights aparece en el comportamiento de estadías."

### 4.3 Boxplots — outliers (celda 888f1ee3)

Tres boxplots, cada uno con un objetivo:

1. **`adr` × `hotel`** → compara distribución de precios entre City y Resort.
   Detecta outliers de tarifa por hotel.
2. **`lead_time` × `hotel`** → ¿reservan con más anticipación en uno que
   en otro? Spoiler: sí, el Resort.
3. **`lead_time` × `is_canceled`** → primer indicio visual de H3.
   La mediana del grupo "canceladas" está claramente arriba del grupo "no canceladas".

**¿Qué es un outlier en un boxplot?** Cualquier punto fuera de
`Q1 − 1.5·IQR` o `Q3 + 1.5·IQR`. Son los puntitos sueltos arriba/abajo del
"bigote".

**Si preguntan "¿por qué no eliminaste todos los outliers?":**
> "Porque muchos son válidos. Una reserva con `adr` alto puede ser una
> suite real. Solo eliminé los técnicamente imposibles: `adr` negativo y
> el extremo de 5400 que era un error de carga. Los outliers legítimos
> son parte de la realidad del negocio."

### 4.4 Scatterplots — relaciones (celda d96c7ea7)

1. **`lead_time` vs `adr`** con color por cancelación → busca patrones
   bidimensionales.
2. **`total_nights` vs `adr`** con color por hotel → ver si los hoteles
   se comportan distinto.

**Detalle técnico:** uso `df.sample(5000, random_state=42)` para no saturar
el gráfico (87k puntos serían un manchón ilegible). El `random_state` fija
la semilla → resultado reproducible.

### 4.5 Heatmap de correlación (celda 37dc5d8e)

Matriz de Pearson sobre 10 variables numéricas seleccionadas.

**Lectura clave para `is_canceled`:**
- `lead_time` → correlación positiva (refuerza H3)
- `total_of_special_requests` → correlación negativa (refuerza H2)
- `required_car_parking_spaces` → negativa (proxy de compromiso)
- `previous_cancellations` → positiva (quien canceló antes vuelve a hacerlo)

**Si preguntan "¿qué es Pearson?":**
> "Mide correlación lineal entre dos variables numéricas, va de -1 a +1.
> 0 = sin relación lineal. No detecta relaciones no lineales: por eso el
> heatmap es un punto de partida, no un veredicto final."

### Conteo de visualizaciones (vs mínimo)

| Tipo | Mínimo | Notebook |
|---|---|---|
| Histogramas + KDE | 3 | 3 |
| Boxplots | 3 | 3 |
| Scatterplots | 2 | 2 |
| Adicionales | 3 | 6 |
| **Total** | **11** | **14** |

Las 6 adicionales: heatmap, 3 barras (H1/H2/H3), torta (H4), serie temporal (H5).

---

## 5. Verificación de hipótesis (sección 5 del notebook)

### Estructura
Para cada H: tabla/cálculo + visualización + lectura de resultado.

### H1 — Canal de distribución (celda 354af202)

**Cálculo:** `groupby('market_segment').agg(reservas, tasa_cancel)`.
Tasa = media de `is_canceled` × 100.

**Resultados:**
- `Online TA` → **35,4%** de cancelación (canal con más volumen)
- `Direct` → 14,8%
- `Offline TA/TO` → 14,8%
- `Corporate` → 12,1%

**Veredicto:** Confirmada. Las OTAs cancelan más del doble que el canal directo.

**Visualización:** barras horizontales ordenadas, con porcentaje encima de cada barra.

**Si preguntan "¿por qué `Online TA` cancela más?":**
> "Hipótesis: políticas de cancelación más flexibles, comparación entre
> hoteles desde la misma plataforma, menor compromiso emocional con la
> marca del hotel. Pero el dataset no permite confirmarlo, solo medir el efecto."

### H2 — Pedidos especiales (celda 20e06541)

**Cálculo:** tasa de cancelación por cada valor de `total_of_special_requests` (0-5).

**Resultados:**
- 0 pedidos → 33,3% cancela
- 1 pedido → 22,1%
- 2 pedidos → 14,1%
- 5 pedidos → 5,6%

**Caída monótona y muy fuerte.** A más pedidos → menos cancelación, sin excepciones.

**Veredicto:** Confirmada.

**Por qué es la hipótesis más accionable:** la variable está disponible al
**momento de la reserva**. Permite scoring en tiempo real, sin esperar.

### H3 — Lead time (celda 42728442)

**Cálculo:** discretizo `lead_time` en bins (0-7, 8-30, 31-90, 91-180, 181-365, >365)
con `pd.cut()`. Calculo tasa por bin.

**Resultados:**
- 0-7 días → 8,4%
- 8-30 días → ~18%
- 31-90 días → ~28%
- 91-180 días → ~36%
- 181-365 días → ~40%
- >365 días → >40%

**Relación monótona creciente.** Veredicto: confirmada.

**Si preguntan "¿por qué discretizar y no usar la variable continua?":**
> "Para que el resultado sea accionable. El negocio no puede operar sobre
> 'lead_time = 247'. Sí puede operar sobre 'reservas con más de 6 meses
> de anticipación cancelan ~40% → planificá overbooking para ese segmento'."

### H4 — Huéspedes repetidos (celda 9557d28b)

**Cálculo:** `groupby('is_repeated_guest').is_canceled.mean() * 100`.

**Resultados:**
- No repetidos → 28,3% cancela
- Repetidos → 7,7% cancela

**~20 puntos porcentuales menos.** Veredicto: confirmada.

**Visualización extra (torta):** muestra que los repetidos son apenas el
3,9% del total → el efecto es real pero el segmento es chico.

**Si preguntan "¿entonces no vale la pena fidelizar?":**
> "Al revés: ese 3,9% tiene ~4× menos churn. Si ese segmento creciera,
> bajaría la tasa global de cancelación. La torta justifica invertir en
> hacer crecer ese segmento, no en ignorarlo."

### H5 — Estacionalidad de ADR (celda 210567ff)

**Cálculo:** `groupby(['arrival_date_month', 'hotel']).adr.mean()`.

**Resultados:**
- **Resort Hotel:** €49 (noviembre) → €188 (agosto). Casi cuadruplica
  en pico de verano.
- **City Hotel:** €85 (enero) → €128 (mayo). Mucho más estable, picos
  suaves en primavera y otoño.
- En julio-agosto, el Resort **supera** al City → invierte la jerarquía
  habitual.

**Veredicto:** confirmada en sus dos partes (estacionalidad + diferencia
entre hoteles).

**Visualización:** gráfico de líneas con dos series, una por hotel.
Marker `o` en cada mes para que se vean los puntos.

---

## 6. Conclusiones finales (sección 6 del notebook)

### Hallazgos relevantes (lo que hay que saber decir de memoria)

**Hallazgo 1 — Hay un perfil de reserva de alto riesgo identificable:**
> "Si combinás los cuatro predictores que dieron significativos —canal
> Online TA, sin pedidos especiales, lead_time alto, cliente nuevo— tenés
> un perfil de reserva con probabilidad de cancelación muy por encima del
> 27,5% promedio. Eso habilita un modelo simple de risk scoring sin
> necesidad de machine learning."

**Hallazgo 2 — La calidad de datos es un hallazgo en sí mismo:**
> "El dataset traía 26,8% de duplicados y 94% de nulos en `company`.
> Cualquier KPI calculado sobre los datos crudos hubiera estado sesgado.
> En un proyecto real, este sería el primer issue a levantar antes de
> sacar conclusiones."

**Hallazgo 3 — La oportunidad operativa está en el City Hotel:**
> "El City concentra mayor volumen, mayor exposición a OTAs y cancelaciones
> materiales. Es donde el ROI de un programa de retención sería más alto.
> El Resort tiene su propio juego: revenue management estacional."

### Cierre (cómo terminar la defensa)

> "El trabajo confirmó las cinco hipótesis con evidencia cuantitativa. Las
> cinco terminan en una acción concreta: revisar mix de canales, scoring de
> riesgo, planificación de overbooking, fidelización con KPI claro y
> pricing dinámico por hotel. No es solo un EDA: es un EDA orientado a
> decisión."

---

## Anexo — Glosario rápido (por si preguntan)

| Término | Definición corta |
|---|---|
| EDA | Análisis exploratorio de datos. Primer paso antes de modelar. |
| KDE | Kernel Density Estimation. Estima la distribución continua de una variable. |
| Outlier | Valor atípico, fuera del rango esperado. En boxplot: fuera de Q1−1.5·IQR o Q3+1.5·IQR. |
| IQR | Rango intercuartil = Q3 − Q1. |
| Pearson | Coeficiente de correlación lineal, va de -1 a +1. |
| `is_canceled` | Variable binaria target: 1 = la reserva fue cancelada. |
| ADR | Average Daily Rate. Precio medio diario de la habitación. |
| OTA | Online Travel Agency. Booking, Expedia, etc. |
| `lead_time` | Días entre la fecha de reserva y la fecha de llegada. |
| `market_segment` | Canal por el que llegó la reserva. |
| Churn | Tasa de cancelación / abandono. |

---

## Anexo — Preguntas trampa habituales en defensas

**"¿Hiciste algún test estadístico para confirmar las hipótesis?"**
> "No formalmente. Es un EDA, no un análisis confirmatorio. Las diferencias
> que mostré son tan grandes (35% vs 14%, 33% vs 5%, 28% vs 7%) que un test
> chi-cuadrado o de proporciones seguramente daría significativo, pero el
> objetivo del TP era exploratorio, no inferencial. Sería el siguiente paso."

**"¿Hay sesgo en el dataset?"**
> "Sí, hay que tenerlo en cuenta: el dataset es de Portugal (la mayoría de
> reservas son `country = PRT`), de 2015-2017, y de dos hoteles específicos.
> Los hallazgos no son extrapolables sin más a otros mercados o épocas."

**"¿Qué harías si tuvieras más tiempo?"**
> "Tres cosas: (1) tests de significancia estadística por hipótesis,
> (2) un modelo de clasificación simple —regresión logística— para validar
> los predictores combinados, y (3) análisis de cohortes temporales para
> ver si los patrones cambiaron entre 2015 y 2017."

**"¿Por qué eliminaste duplicados si no había ID único?"**
> "Porque filas literalmente idénticas en todas las columnas no aportan
> información nueva: o son errores de carga, o son reservas que el dataset
> no logró distinguir. En cualquier caso, contarlas dos veces sesga
> cualquier métrica agregada hacia arriba."

**"¿`is_canceled` es la mejor variable target?"**
> "Para predicción de cancelación, sí. Para análisis de revenue real
> existe `reservation_status` que distingue 'No-Show' de 'Canceled', y
> ambos son distintos del 'Check-Out'. Para este TP me concentré en
> `is_canceled` porque es binaria y permite tasas comparables."

---

## Cómo prepararte (checklist práctico)

- [ ] Correr el notebook entero al menos una vez antes de la defensa
      (`Run All` en VS Code o `jupyter nbconvert --execute --inplace`).
- [ ] Saber decir de memoria: 27,5% (tasa global), 35,4% (Online TA),
      ~20 pp (gap repetidos vs nuevos).
- [ ] Tener abierta la sección 6 del notebook como respaldo visual.
- [ ] Si te preguntan algo del código que no recordás: abrir la celda y
      leer en voz alta. Es válido.
- [ ] Ensayar la apertura (sección 0 de este doc) hasta que salga natural.
