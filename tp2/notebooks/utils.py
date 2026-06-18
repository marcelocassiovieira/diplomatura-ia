"""Utilidades compartidas del TP2 - Clasificacion smoking.

Centraliza la semilla, las rutas del proyecto y la funcion de carga + saneo de
datos, de modo que el notebook de discovery (01) y el de prediccion (06) apliquen
EXACTAMENTE el mismo tratamiento estructural a los datos. Esto es clave para que
el pipeline serializado se aplique sin sorpresas al set sin etiquetar.

Convencion del proyecto: castellano sin acentos ni egnes.
"""
from pathlib import Path

import pandas as pd

# Semilla unica para todo el proyecto: split, validacion cruzada, modelos y busqueda
# de hiperparametros. Garantiza reproducibilidad.
SEED = 42


def get_root() -> Path:
    """Devuelve la raiz del proyecto tp2/ sin importar desde donde se ejecute.

    Los notebooks de la entrega corren desde notebooks/, pero el material de defensa
    corre desde defensa/ y alguien podria abrir el proyecto desde la raiz de tp2/.
    Para cubrir todos los casos, subimos carpetas hasta encontrar la que contiene
    `data/raw` (la raiz del proyecto). Si no la encontramos, caemos al heuristico
    simple por nombre de carpeta.
    """
    cwd = Path.cwd()
    for base in (cwd, *cwd.parents):
        if (base / "data" / "raw").is_dir():
            return base
    return cwd.parent if cwd.name in ("notebooks", "defensa") else cwd


ROOT = get_root()
DATA_RAW = ROOT / "data" / "raw"
DATA_PROCESSED = ROOT / "data" / "processed"
DATA_EXTERNAL = ROOT / "data" / "external"
IMGS = ROOT / "imgs"
MODELS = ROOT / "models"
MODELS_DTC = MODELS / "DTCs"
MODELS_XGB = MODELS / "XGBOOSTs"

# Rutas de los datasets originales tal como se descargaron.
TRAIN_XLSX = DATA_RAW / "smoking_prediction.xlsx"
PRED_XLSX = DATA_RAW / "smoking_prediction_entrega.xlsx"

# Mapeo de nombres originales -> snake_case sin parentesis ni espacios.
# Respeta la convencion del proyecto (sin acentos) y evita problemas al
# seleccionar columnas por nombre dentro del ColumnTransformer.
COLUMN_MAPPING = {
    "ID": "id",
    "gender": "gender",
    "age": "age",
    "height(cm)": "height_cm",
    "weight(kg)": "weight_kg",
    "waist(cm)": "waist_cm",
    "eyesight(left)": "eyesight_left",
    "eyesight(right)": "eyesight_right",
    "hearing(left)": "hearing_left",
    "hearing(right)": "hearing_right",
    "systolic": "systolic",
    "relaxation": "relaxation",
    "fasting blood sugar": "fasting_blood_sugar",
    "Cholesterol": "cholesterol",
    "triglyceride": "triglyceride",
    "HDL": "hdl",
    "LDL": "ldl",
    "hemoglobin": "hemoglobin",
    "Urine protein": "urine_protein",
    "serum creatinine": "serum_creatinine",
    "AST": "ast",
    "ALT": "alt",
    "Gtp": "gtp",
    "oral": "oral",
    "dental caries": "dental_caries",
    "tartar": "tartar",
    "smoking": "smoking",
}

# Columna identificadora (no es feature; se usa para la salida final).
ID_COL = "id"

# Variable objetivo.
TARGET = "smoking"

# Columnas que se descartan siempre antes de modelar:
#  - id: identificador, no aporta senial.
#  - oral: constante (vale "Y" en el 100% de los registros de ambos sets).
DROP_COLS = ["id", "oral"]


def cargar_y_sanear(path: Path) -> pd.DataFrame:
    """Carga un xlsx del proyecto y aplica el saneo estructural minimo.

    Pasos (deterministicos, no dependen de estadisticos -> no causan leakage):
      1. Lee el Excel (engine openpyxl).
      2. Elimina filas completamente vacias si las hubiera (saneo defensivo).
      3. Renombra columnas a snake_case segun COLUMN_MAPPING.
      4. Castea la variable objetivo a int si esta presente.

    Reutilizada por 01 (train + pred) y por 06 (pred final), garantizando que el
    set sin etiquetar reciba el mismo tratamiento que el de entrenamiento.
    """
    df = pd.read_excel(path)
    df = df.dropna(how="all").reset_index(drop=True)
    df = df.rename(columns=COLUMN_MAPPING)
    if TARGET in df.columns:
        df[TARGET] = df[TARGET].astype(int)
    df = agregar_features(df)
    return df


# Nombres de las variables derivadas (feature engineering). Se calculan fila por fila
# a partir de columnas existentes -> NO usan estadisticos globales -> no causan leakage.
FEATURES_DERIVADAS = [
    "bmi",
    "waist_to_height",
    "pulse_pressure",
    "map",
    "ast_alt_ratio",
    "non_hdl",
    "tg_hdl_ratio",
    "liver_enzymes_sum",
]


def agregar_features(df: pd.DataFrame) -> pd.DataFrame:
    """Crea variables derivadas con sentido biomedico a partir de las originales.

    Todas son combinaciones por-fila (ratios, sumas, diferencias) de columnas que ya
    existen en el dataset, asi que aplicar esta funcion a train, validacion o al set de
    prediccion es seguro: ningun valor depende de estadisticos calculados sobre el
    conjunto (no hay data leakage). Se llama dentro de `cargar_y_sanear`, de modo que
    los caminos de entrenamiento (01) y de prediccion (06) generan exactamente las
    mismas columnas.

    Las divisiones usan un epsilon para evitar division por cero.
    """
    df = df.copy()
    eps = 1e-6
    altura_m = df["height_cm"] / 100.0

    # Indice de masa corporal: resume peso y altura (proxy de obesidad).
    df["bmi"] = df["weight_kg"] / (altura_m ** 2 + eps)
    # Cintura sobre altura: marcador de grasa abdominal.
    df["waist_to_height"] = df["waist_cm"] / (df["height_cm"] + eps)
    # Presion de pulso: sistolica menos diastolica (relaxation), marcador cardiovascular.
    df["pulse_pressure"] = df["systolic"] - df["relaxation"]
    # Presion arterial media.
    df["map"] = df["relaxation"] + (df["systolic"] - df["relaxation"]) / 3.0
    # Indice de De Ritis: ratio de enzimas hepaticas AST/ALT.
    df["ast_alt_ratio"] = df["ast"] / (df["alt"] + eps)
    # Colesterol no-HDL (la fraccion "mala").
    df["non_hdl"] = df["cholesterol"] - df["hdl"]
    # Trigliceridos sobre HDL: proxy de riesgo metabolico / resistencia a la insulina.
    df["tg_hdl_ratio"] = df["triglyceride"] / (df["hdl"] + eps)
    # Carga total de enzimas hepaticas.
    df["liver_enzymes_sum"] = df["ast"] + df["alt"] + df["gtp"]
    return df


def features_target(df: pd.DataFrame):
    """Separa X (features, sin id/oral/target) e y (target) de un dataframe de train."""
    X = df.drop(columns=[c for c in DROP_COLS + [TARGET] if c in df.columns])
    y = df[TARGET] if TARGET in df.columns else None
    return X, y
