"""
CONFIGURACIÓN DEL MODELO TOP2VEC
=================================

Este archivo contiene todos los parámetros que puedes ajustar para el modelo.
Modifica los valores según tus necesidades de análisis.

📖 Para entender qué hace cada parámetro, consulta el README.md
"""

# =============================================================================
# 📂 ARCHIVOS DE ENTRADA/SALIDA
# =============================================================================

# Archivos de datos (ya están en la carpeta data/)
ARCHIVO_NOTICIAS = "data/noticias.csv"
ARCHIVO_EMBEDDINGS = "data/embeddings_precalculados.npz"

# Columnas en el CSV de noticias
COLUMNA_TEXTO = "body"          # Columna que contiene el texto de la noticia
COLUMNA_FECHA = "pub_date"      # Columna que contiene la fecha de publicación
COLUMNA_ID = "doc_id"           # Columna con el ID único de cada noticia

# Archivos de salida
CARPETA_MODELOS = "modelos"
CARPETA_RESULTADOS = "resultados"
NOMBRE_MODELO = "modelo_top2vec.model"


# =============================================================================
# 🔍 PARÁMETROS DE AGRUPACIÓN (HDBSCAN)
# =============================================================================
# Estos controlan cómo se forman los tópicos

HDBSCAN_CONFIG = {
    # Mínimo de documentos para formar un tópico
    # ↑ Mayor = tópicos más grandes y generales
    # ↓ Menor = captura tópicos más pequeños y específicos
    'min_cluster_size': 50,
    
    # Densidad mínima para identificar un tópico
    # ↑ Mayor = tópicos más robustos (pero menos tópicos)
    # ↓ Menor = captura tópicos más raros
    'min_samples': 25,
    
    # Métrica de distancia (no cambiar a menos que sepas lo que haces)
    'metric': 'euclidean',
    
    # Método de selección de clusters (recomendado: 'eom')
    'cluster_selection_method': 'eom'
}


# =============================================================================
# 🗺️ PARÁMETROS DE REDUCCIÓN DIMENSIONAL (UMAP)
# =============================================================================
# Estos controlan cómo se reduce la dimensionalidad de los embeddings

UMAP_CONFIG = {
    # Número de vecinos cercanos a considerar
    # ↑ Mayor (ej: 100) = estructura global, temas amplios
    # ↓ Menor (ej: 30) = estructura local, temas específicos
    'n_neighbors': 50,
    
    # Número de dimensiones en el espacio reducido
    # Rango típico: 2-10 (5 es un buen balance)
    'n_components': 5,
    
    # Métrica de similitud (coseno es mejor para textos)
    'metric': 'cosine',
    
    # Semilla aleatoria (para reproducibilidad)
    'random_state': 42
}


# =============================================================================
# 🔗 PARÁMETROS DE FUSIÓN DE TÓPICOS
# =============================================================================

# Similitud mínima para fusionar tópicos muy parecidos
# ↑ Mayor (ej: 0.15) = fusiona más tópicos similares (menos tópicos totales)
# ↓ Menor (ej: 0.05) = mantiene tópicos separados (más granularidad)
TOPIC_MERGE_DELTA = 0.1


# =============================================================================
# 📊 PARÁMETROS DE ANÁLISIS Y SALIDA
# =============================================================================

# Número de palabras clave a mostrar por tópico
NUM_PALABRAS_POR_TOPICO = 10

# Mínima frecuencia de una palabra para considerarla (filtro)
MIN_COUNT_PALABRAS = 25


# =============================================================================
# 💾 OPCIONES DE GUARDADO
# =============================================================================

# ¿Guardar el modelo entrenado? (Recomendado: True)
# Si es True, podrás reutilizar el modelo sin re-entrenar
GUARDAR_MODELO = True

# ¿Exportar resultados a Excel? (Recomendado: True)
EXPORTAR_EXCEL = True

# ¿Generar gráficos de distribución? (Requiere más tiempo)
GENERAR_GRAFICOS = False


# =============================================================================
# 🎛️ PRESETS RÁPIDOS
# =============================================================================
# Descomenta el preset que quieras usar (comenta los otros)

# --- PRESET 1: ANÁLISIS GENERAL (Por defecto) ---
# Balance entre granularidad y robustez
# Usa los valores definidos arriba


# --- PRESET 2: TEMAS EMERGENTES ---
# Para capturar tópicos pequeños pero relevantes
# HDBSCAN_CONFIG['min_cluster_size'] = 30
# HDBSCAN_CONFIG['min_samples'] = 15
# UMAP_CONFIG['n_neighbors'] = 30
# TOPIC_MERGE_DELTA = 0.08


# --- PRESET 3: MACRO-TEMAS ---
# Solo los tópicos más grandes y generales
# HDBSCAN_CONFIG['min_cluster_size'] = 100
# HDBSCAN_CONFIG['min_samples'] = 50
# UMAP_CONFIG['n_neighbors'] = 100
# TOPIC_MERGE_DELTA = 0.15


# =============================================================================
# ⚠️ CONFIGURACIÓN AVANZADA (No modificar a menos que sepas lo que haces)
# =============================================================================

# Tokenizer personalizado para español (preserva tildes y ñ)
USE_SPANISH_TOKENIZER = True

# Usar tokenizer del modelo de embeddings (False recomendado)
USE_EMBEDDING_MODEL_TOKENIZER = False

# Verbose (mostrar progreso detallado)
VERBOSE = True
