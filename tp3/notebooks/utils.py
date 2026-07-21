"""Utilidades compartidas del TP3 - Analisis de sentimiento en tweets (Sentiment140).

Centraliza la semilla, las rutas del proyecto, la carga de los CSV originales y la
funcion de limpieza de texto, de modo que todas las notebooks (01 a 06) apliquen
EXACTAMENTE el mismo tratamiento a los tweets. Esto es clave para que el modelo
serializado se aplique sin sorpresas al test manual.

Convencion del proyecto: castellano sin acentos ni egnes.
"""
from pathlib import Path

import pandas as pd

# Semilla unica para todo el proyecto: split estratificado, NMF y cualquier
# componente estocastico. Garantiza reproducibilidad.
SEED = 42


def get_root() -> Path:
    """Devuelve la raiz del proyecto tp3/ sin importar desde donde se ejecute.

    Los notebooks corren desde notebooks/, pero alguien podria abrir el proyecto
    desde la raiz de tp3/. Subimos carpetas hasta encontrar la que contiene
    `data/raw` (la raiz del proyecto); si no aparece, caemos al heuristico simple
    por nombre de carpeta.
    """
    cwd = Path.cwd()
    for base in (cwd, *cwd.parents):
        if (base / "data" / "raw").is_dir():
            return base
    return cwd.parent if cwd.name == "notebooks" else cwd


ROOT = get_root()
DATA_RAW = ROOT / "data" / "raw"
DATA_PROCESSED = ROOT / "data" / "processed"
IMGS = ROOT / "imgs"
MODELS = ROOT / "models"

# Rutas de los datasets originales tal como se descargaron del ZIP de la consigna.
TRAIN_CSV = DATA_RAW / "training.1600000.processed.noemoticon.csv"
TEST_CSV = DATA_RAW / "testdata.manual.2009.06.14.csv"

# Intermedios procesados (los genera la notebook 03).
TRAIN_CLEAN_PARQUET = DATA_PROCESSED / "train_clean.parquet"
TEST_CLEAN_PARQUET = DATA_PROCESSED / "test_clean.parquet"

# Modelo final (lo genera la notebook 04).
VECTORIZER_JOBLIB = MODELS / "tfidf_vectorizer.joblib"
MODELO_JOBLIB = MODELS / "logistic_regression.joblib"

# Los CSV no traen encabezado; estas son las columnas documentadas del dataset.
COLUMNAS = ["target", "id", "date", "query", "user", "text"]

# Variable objetivo y su interpretacion en Sentiment140.
TARGET = "target"
TARGET_LABELS = {0: "negativo", 2: "neutral", 4: "positivo"}

# Colores fijos por clase para que todos los graficos del TP sean consistentes.
# El sentimiento es una polaridad -> par divergente rojo/azul validado (CVD-safe,
# contraste >= 3:1 sobre fondo claro) con gris como punto medio neutral. Los
# graficos de barras llevan ademas etiquetas directas de valor.
COLOR_NEG = "#e34948"
COLOR_NEU = "#8a8984"
COLOR_POS = "#2a78d6"


def cargar_training(nrows: int | None = None) -> pd.DataFrame:
    """Carga el CSV de entrenamiento (1.600.000 tweets).

    encoding latin-1 porque el archivo contiene bytes fuera de UTF-8.
    `nrows` existe SOLO para depurar codigo con una muestra; la consigna exige
    que los resultados finales usen el dataset completo (nrows=None).
    """
    return pd.read_csv(
        TRAIN_CSV, encoding="latin-1", header=None, names=COLUMNAS, nrows=nrows
    )


def cargar_test() -> pd.DataFrame:
    """Carga el CSV de test manual (498 tweets etiquetados a mano)."""
    return pd.read_csv(TEST_CSV, encoding="latin-1", header=None, names=COLUMNAS)


def limpiar_tweets(textos: pd.Series) -> pd.Series:
    """Limpieza de tweets. Cada decision se tomo mirando ejemplos reales del dataset:

      1. Desescapa las entidades HTML mal formadas (&amp;, &quot;, ...): son un
         error de formato del texto, no contenido real del tweet.
      2. Pasa todo a minusculas: "Good" y "good" deben contar como la misma palabra.
      3. Reemplaza menciones @usuario por `usuariomencionado` y URLs por `linkweb`.
         Se prueba borrarlas directamente, pero en tweets donde la mencion cumple
         una funcion gramatical (ej. "@user loves @otro more" -> "loves more") se
         pierde la estructura de la oracion. Reemplazar por una palabra fija
         mantiene la estructura sin agregar cientos de miles de usuarios/dominios
         unicos al vocabulario (46% de los tweets tienen mencion, 4,8% tienen URL).
      4. Conserva la palabra de los hashtags, solo saca el simbolo # (#happy ->
         happy): son parte real del contenido del tweet, no ruido externo.
      5. Pega las contracciones en vez de expandirlas (don't -> dont, can't ->
         cant): el vectorizador de scikit-learn corta por el apostrofe y la
         negacion se pierde (don't -> "don" + "t", y la "t" se descarta por
         demasiado corta). Se prefirio pegar en vez de expandir a la forma larga
         (do not) por ser mas simple y no depender de una lista de casos
         ambiguos (it's = it is / it has).
      6. Elimina el resto de la puntuacion y colapsa espacios.

    Se usa la API .str de pandas (vectorizada) porque un apply fila a fila sobre
    1.6M de tweets es innecesariamente lento.
    """
    t = textos.str.replace("&quot;", '"', regex=False)
    t = t.str.replace("&amp;", "&", regex=False)
    t = t.str.replace("&lt;", "<", regex=False)
    t = t.str.replace("&gt;", ">", regex=False)
    t = t.str.lower()
    t = t.str.replace(r"https?://\S+|www\.\S+", " linkweb ", regex=True)
    t = t.str.replace(r"@\w+", " usuariomencionado ", regex=True)
    t = t.str.replace(r"#(\w+)", r"\1", regex=True)
    t = t.str.replace(r"(\w)'(\w)", r"\1\2", regex=True)
    t = t.str.replace(r"[^a-z0-9\s]", " ", regex=True)
    t = t.str.replace(r"\s+", " ", regex=True).str.strip()
    return t


def guardar_fig(fig, nombre: str) -> None:
    """Guarda una figura en imgs/ con parametros consistentes para la presentacion."""
    IMGS.mkdir(parents=True, exist_ok=True)
    fig.savefig(IMGS / nombre, dpi=150, bbox_inches="tight")


def etiquetas(serie_target: pd.Series) -> pd.Series:
    """Mapea los codigos 0/2/4 a sus nombres legibles."""
    return serie_target.map(TARGET_LABELS)
