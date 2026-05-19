# Trabajo Práctico N° 1 — Análisis Exploratorio de Datos

**Diplomatura en Inteligencia Artificial**  
**Autor:** Marcelo Vieira

## Objetivo

Realizar un análisis exploratorio de datos (EDA) sobre el dataset *Hotel Bookings*. El trabajo busca aplicar las técnicas de carga, limpieza, exploración y visualización vistas durante el cursado, y responder un conjunto de hipótesis de negocio formuladas previamente.

## Contexto del dataset

`hotel_bookings.csv` contiene 119.390 reservas de dos hoteles ubicados en Portugal entre julio de 2015 y agosto de 2017:

- **Resort Hotel** (hotel vacacional, zona turística costera).
- **City Hotel** (hotel urbano, viajeros de negocios y turistas de fin de semana).

Cada fila representa una reserva concreta con información sobre el cliente, el canal de venta, la estadía y si la reserva fue finalmente cancelada. Es un dataset público de referencia muy usado para EDA y modelos de predicción de cancelación.

**Tamaño:** 119.390 filas × 32 columnas (cumple holgadamente el mínimo del TP de 50.000 filas y 10 columnas).

## Diccionario de datos

| Columna | Tipo | Descripción |
|---|---|---|
| `hotel` | categórica | Tipo de hotel: `Resort Hotel` o `City Hotel`. |
| `is_canceled` | binaria (0/1) | 1 si la reserva fue cancelada. **Variable target.** |
| `lead_time` | entero | Días entre la fecha de reserva y la fecha de llegada. |
| `arrival_date_year` | entero | Año de llegada. |
| `arrival_date_month` | categórica | Mes de llegada (en inglés). |
| `arrival_date_week_number` | entero | Semana ISO del año. |
| `arrival_date_day_of_month` | entero | Día del mes. |
| `stays_in_weekend_nights` | entero | Noches en fin de semana (sábado-domingo). |
| `stays_in_week_nights` | entero | Noches entre lunes y viernes. |
| `adults` | entero | Cantidad de adultos. |
| `children` | entero | Cantidad de niños. |
| `babies` | entero | Cantidad de bebés. |
| `meal` | categórica | Régimen de comidas (BB, HB, FB, SC, Undefined). |
| `country` | categórica | País de origen del cliente (ISO-3). |
| `market_segment` | categórica | Segmento de mercado (Direct, Corporate, Online TA, Offline TA/TO, etc.). |
| `distribution_channel` | categórica | Canal de distribución (Direct, Corporate, TA/TO, GDS). |
| `is_repeated_guest` | binaria (0/1) | 1 si el cliente ya se había hospedado antes. |
| `previous_cancellations` | entero | Cancelaciones previas del cliente. |
| `previous_bookings_not_canceled` | entero | Reservas previas no canceladas del cliente. |
| `reserved_room_type` | categórica | Tipo de habitación reservada (codificada). |
| `assigned_room_type` | categórica | Tipo de habitación efectivamente asignada. |
| `booking_changes` | entero | Cantidad de modificaciones realizadas a la reserva. |
| `deposit_type` | categórica | Tipo de depósito: `No Deposit`, `Non Refund`, `Refundable`. |
| `agent` | entero | ID del agente de viaje (0 = sin agente). |
| `company` | entero | ID de la empresa que realizó la reserva (0 = sin empresa). |
| `days_in_waiting_list` | entero | Días que la reserva estuvo en lista de espera. |
| `customer_type` | categórica | Tipo de cliente: `Transient`, `Contract`, `Group`, `Transient-Party`. |
| `adr` | float | *Average Daily Rate*: precio medio diario pagado (€). |
| `required_car_parking_spaces` | entero | Plazas de parking solicitadas. |
| `total_of_special_requests` | entero | Cantidad de pedidos especiales (cuna, vista, etc.). |
| `reservation_status` | categórica | Estado final: `Check-Out`, `Canceled`, `No-Show`. |
| `reservation_status_date` | fecha | Fecha del último cambio de estado. |

**Columnas derivadas durante el análisis:**

| Columna | Descripción |
|---|---|
| `arrival_date` | Fecha de llegada construida a partir de año/mes/día. |
| `total_nights` | `stays_in_weekend_nights + stays_in_week_nights`. |
| `total_guests` | `adults + children + babies`. |
| `lead_time_bin` | `lead_time` discretizado en rangos. |

## Hipótesis planteadas

Las hipótesis fueron seleccionadas priorizando su **utilidad de negocio**: cada una habilita una decisión concreta que el hotel puede tomar a partir del resultado.

1. **H1. El canal de distribución (`market_segment`) predice la cancelación.** Las reservas vía OTAs (`Online TA`) cancelan más que las directas o corporativas. Permite revisar el mix de canales y la rentabilidad real una vez descontadas las cancelaciones.
2. **H2. A más pedidos especiales, menor cancelación.** El compromiso del cliente, medido por `total_of_special_requests`, predice la no-cancelación. Habilita un *scoring de riesgo* en el momento de la reserva.
3. **H3. Cuanto mayor es el `lead_time`, mayor es la probabilidad de cancelación.** Permite segmentar la cartera de reservas futuras por nivel de riesgo y planificar overbooking.
4. **H4. Los huéspedes repetidos cancelan menos que los no repetidos.** Justifica con números la inversión en programas de fidelización.
5. **H5. El `adr` tiene un patrón estacional marcado y difiere entre tipos de hotel.** Es la base del *revenue management*: cuándo subir tarifas, cuándo promocionar, cómo posicionar cada hotel.

## Metodología aplicada

1. **Carga** del dataset con `pandas` y revisión inicial de tipos y forma.
2. **Limpieza:**
   - Imputación de nulos: `children` → 0, `country` → `'Unknown'`, `agent`/`company` → 0 (interpretados como ausencia).
   - Eliminación de duplicados exactos (~26,8 % del total).
   - Filtrado de inconsistencias: reservas con 0 huéspedes y `adr` fuera del rango `[0, 1000]`.
3. **Construcción de variables auxiliares** (`arrival_date`, `total_nights`, `total_guests`, `lead_time_bin`).
4. **EDA:**
   - Inspección de tipos y estadísticos descriptivos.
   - Análisis de distribuciones y outliers.
   - Análisis de correlaciones sobre variables numéricas.
5. **Visualizaciones (todas las requeridas por la consigna):**
   - 3 histogramas con KDE: `lead_time`, `adr`, `total_nights`.
   - 3 boxplots: `adr` por hotel, `lead_time` por hotel, `lead_time` según cancelación.
   - 2 scatterplots: `lead_time` vs. `adr` coloreado por cancelación; `total_nights` vs. `adr` por hotel.
   - 3 visualizaciones adicionales: barras (tasa de cancelación por `lead_time_bin`), líneas (`adr` mensual por hotel), torta (proporción de huéspedes repetidos).
   - Visualizaciones complementarias: barras de cancelación por hotel y por pedidos especiales, heatmap de correlaciones.
6. **Verificación de las hipótesis** con métricas y gráficos específicos para cada una.

## Conclusiones y hallazgos relevantes

Tasa global de cancelación tras limpieza: **27,5 %** sobre 87.228 reservas.

- **H1 — Confirmada.** `Online TA` cancela el **35,4 %**, contra **14,8 %** de `Direct`, **14,8 %** de `Offline TA/TO` y **12,1 %** de `Corporate`. Las OTAs cancelan más del doble que los canales directos.
- **H2 — Confirmada.** A más pedidos especiales, menor cancelación: pasa de **33,3 %** con 0 pedidos a **5,6 %** con 5 pedidos, en una caída monótona.
- **H3 — Confirmada.** Las reservas con `lead_time` corto (0-7 días) cancelan apenas **8,4 %**, mientras que las hechas con más de un año superan el **40 %**.
- **H4 — Confirmada.** Los huéspedes repetidos cancelan solo el **7,7 %** vs. **28,3 %** de los nuevos (~20 puntos porcentuales menos), aunque solo representan el **3,9 %** del total.
- **H5 — Confirmada.** El `adr` muestra estacionalidad fuerte: el *Resort* va de **€49 (noviembre)** a **€188 (agosto)** — casi cuadruplica su tarifa en verano. El *City* es más estable: de **€85 (enero)** a **€128 (mayo)**.

**Hallazgos accionables para el negocio:**

1. **Mix de canales:** revisar la inversión en OTAs comparando margen real (precio - comisión - costo asociado a la cancelación) frente al canal directo.
2. **Scoring de riesgo:** combinar `lead_time`, `total_of_special_requests`, `is_repeated_guest` y `previous_cancellations` para clasificar reservas como bajo / medio / alto riesgo y disparar acciones diferenciadas (recordatorios, ofertas, confirmaciones).
3. **Pricing dinámico:** capitalizar la temporada alta del Resort (julio-agosto) con tarifas más agresivas y diseñar paquetes para los meses flojos del City.
4. **Fidelización con métrica clara:** un huésped repetido cancela ~20 puntos porcentuales menos. Eso permite calcular el retorno esperado de un programa de loyalty.
5. **Calidad de datos:** el dataset tenía 26,8 % de duplicados y 94 % de nulos en `company`. Limpiar fue crítico: cualquier KPI calculado sobre los datos crudos habría estado sesgado.

## Estructura del repositorio

```
.
├── README.md                   # Descripción, metodología y conclusiones del TP1
├── TP1_hotel_bookings.ipynb    # Notebook con el desarrollo completo
└── data/
    └── hotel_bookings.csv      # Dataset utilizado
```

## Cómo reproducir el análisis

```bash
pip install pandas numpy matplotlib seaborn jupyter
jupyter notebook TP1_hotel_bookings.ipynb
```

Ejecutar todas las celdas en orden. El notebook lee el CSV desde `data/hotel_bookings.csv`.

## Fuente del dataset

Dataset público *Hotel Booking Demand*, originalmente publicado por Antonio, Almeida y Nunes (2019) en *Data in Brief*. Disponible en Kaggle: <https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand>.
