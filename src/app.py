"""
Top2Vec Web App - Aplicación para Economistas
==============================================

Aplicación web profesional para entrenar y explorar modelos Top2Vec
sin necesidad de programar.

Autor: Top2Vec Team
Fecha: Noviembre 2025
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import json
import sys
from datetime import datetime
from pathlib import Path
import time
import psutil
from io import BytesIO
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image

# Añadir el directorio padre al path para importar top2vec
sys.path.append(str(Path(__file__).parent.parent))

from top2vec import Top2Vec
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import strip_tags

# =============================================================================
# CONFIGURACIÓN DE LA PÁGINA
# =============================================================================

st.set_page_config(
    page_title="Top2Vec - Análisis de Tópicos",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =============================================================================
# ESTILOS CSS PERSONALIZADOS
# =============================================================================

st.markdown("""
<style>
    /* Reducir márgenes laterales para aprovechar más espacio */
    .block-container {
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 95%;
    }
    
    /* Tema principal */
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    
    /* Métricas destacadas */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    
    /* Tarjetas de información */
    .info-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 1rem 0;
    }
    
    /* Botones personalizados */
    .stButton > button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        border: none;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        background-color: #145a8c;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Tabs personalizados */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0 24px;
        background-color: #f0f2f6;
        border-radius: 5px 5px 0 0;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #1f77b4;
        color: white;
    }
    
    /* Barra de progreso */
    .stProgress > div > div > div > div {
        background-color: #1f77b4;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    
    /* Tooltips */
    .tooltip {
        position: relative;
        display: inline-block;
        cursor: help;
    }
    
    /* Alertas */
    .alert-success {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .alert-warning {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .alert-error {
        background-color: #f8d7da;
        border-left: 5px solid #dc3545;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# UTILIDADES Y FUNCIONES AUXILIARES
# =============================================================================

def spanish_friendly_tokenizer(document):
    """Tokenizer que preserva tildes y ñ para español"""
    clean_text = strip_tags(document)
    return simple_preprocess(clean_text, deacc=False)


class PrecomputedEmbeddings:
    """Clase para proveer embeddings precomputados a Top2Vec"""
    
    def __init__(self, embeddings_file, csv_file=None):
        """
        Cargar embeddings precomputados
        
        Args:
            embeddings_file: Archivo .npz con embeddings
            csv_file: CSV original para obtener textos y fechas
        """
        self.embeddings_file = embeddings_file
        
        # Cargar embeddings
        data = np.load(embeddings_file, allow_pickle=True)
        
        # CRÍTICO: El archivo NPZ usa 'embeddings' NO 'document_vectors'
        # pero el nuevo archivo usa 'document_vectors', soportar ambos
        if 'embeddings' in data:
            self.embeddings = data['embeddings']
        elif 'document_vectors' in data:
            self.embeddings = data['document_vectors']
        else:
            raise ValueError(f"No se encontraron embeddings. Claves: {list(data.keys())}")
        
        # Cargar word_vectors y vocab (CRÍTICO para Top2Vec)
        self.word_vectors = data.get('word_vectors', None)
        self.vocab = data.get('vocab', None)
        self.word_indexes = data.get('word_indexes', None)
        if self.word_indexes is not None:
            self.word_indexes = self.word_indexes.item()  # Convertir de numpy a dict
        
        # Cargar pub_dates y doc_ids del CSV
        self.documents = None
        self.pub_dates = None
        self.doc_ids = None
        
        if csv_file and os.path.exists(csv_file):
            df = pd.read_csv(csv_file)
            self.documents = df['body'].astype(str).tolist()
            
            # Cargar fechas y doc_ids
            if 'pub_date' in df.columns:
                self.pub_dates = pd.to_datetime(df['pub_date']).values
            if 'doc_id' in df.columns:
                self.doc_ids = df['doc_id'].values
            else:
                self.doc_ids = np.arange(len(self.documents))
        
        # Índice para mapear textos a embeddings
        self.current_batch_start = 0
    
    def __call__(self, documents_batch):
        """
        Método para que Top2Vec pueda llamar a esta clase como embedding_model
        
        Args:
            documents_batch: Lista de documentos para embeddings
            
        Returns:
            numpy.ndarray: Embeddings correspondientes
        """
        batch_size = len(documents_batch)
        
        # Retornar el siguiente lote de embeddings
        start_idx = self.current_batch_start
        end_idx = start_idx + batch_size
        
        if end_idx > len(self.embeddings):
            end_idx = len(self.embeddings)
            
        batch_embeddings = self.embeddings[start_idx:end_idx]
        self.current_batch_start = end_idx
        
        return batch_embeddings


def get_system_resources():
    """Obtiene información de uso de recursos del sistema"""
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    
    return {
        'cpu_percent': cpu_percent,
        'memory_percent': memory.percent,
        'memory_used_gb': memory.used / (1024**3),
        'memory_total_gb': memory.total / (1024**3)
    }


def save_model_metadata(config, model_path, num_topics, execution_time):
    """Guarda metadata del modelo entrenado"""
    metadata = {
        'timestamp': datetime.now().isoformat(),
        'model_path': str(model_path),
        'num_topics': num_topics,
        'execution_time_seconds': execution_time,
        'config': config
    }
    
    metadata_path = Path(model_path).parent / 'metadata.json'
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    return metadata_path


def load_model_metadata(model_dir):
    """Carga metadata de un modelo"""
    metadata_path = Path(model_dir) / 'metadata.json'
    if metadata_path.exists():
        with open(metadata_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def list_available_models():
    """Lista todos los modelos disponibles en la carpeta de modelos"""
    models_dir = Path('modelos')
    if not models_dir.exists():
        return []
    
    models = []
    for item in models_dir.iterdir():
        if item.is_dir():
            metadata = load_model_metadata(item)
            if metadata:
                models.append({
                    'name': item.name,
                    'path': str(item),
                    'metadata': metadata
                })
    
    return sorted(models, key=lambda x: x['metadata']['timestamp'], reverse=True)


def clean_topic_words(words, scores, target_count=20):
    """
    Limpia y deduplicar palabras de tópicos eliminando variantes con puntuación.
    
    Args:
        words: Lista de palabras del tópico
        scores: Lista de scores correspondientes
        target_count: Número de palabras únicas a retornar
    
    Returns:
        Tupla (palabras_limpias, scores_limpios)
    """
    import re
    stop_suffixes = ('.el', '.la', '.de', '.y', '.en', '.los', '.las', '.un', '.una', '.al', '.del', '.por', '.con', '.sin', '.para', '.sobre', '.entre', '.o', '.u')
    seen_clean = {}
    for word, score in zip(words, scores):
        # Quitar puntuación periférica
        cleaned = re.sub(r'^[^\w]+|[^\w]+$', '', word, flags=re.UNICODE)
        # Quitar palabras con punto seguido de letras (ej: ".el", ".de") o signos
        if re.search(r'\.[a-záéíóúñ]+$', cleaned, re.IGNORECASE) or cleaned.lower().endswith(stop_suffixes):
            cleaned = cleaned.split('.')[0]
        # Quitar palabras que contienen signos de puntuación internos o finales
        if re.search(r'[\?\!\-\(\)\[\]"\'\;\:\,]', cleaned):
            cleaned = re.sub(r'[\?\!\-\(\)\[\]"\'\;\:\,]', '', cleaned)
        # Filtrar palabras que contienen números
        if re.search(r'\d', cleaned):
            continue
        # Si la versión limpia está vacía, skip
        if not cleaned:
            continue
        if cleaned.lower() not in seen_clean or score > seen_clean[cleaned.lower()][1]:
            seen_clean[cleaned.lower()] = (cleaned, score)
        if len(seen_clean) >= target_count:
            break
    items = sorted(seen_clean.values(), key=lambda x: x[1], reverse=True)
    clean_words = [item[0] for item in items]
    clean_scores = [item[1] for item in items]
    return clean_words, clean_scores


def create_wordcloud_image(words, scores, width=800, height=400, max_words=10):
    """Crea una imagen de wordcloud"""
    # Limitar a top N palabras
    words = words[:max_words]
    scores = scores[:max_words]
    
    # Crear diccionario de frecuencias
    word_freq = {word: score for word, score in zip(words, scores)}
    
    # Generar wordcloud con semilla fija para reproducibilidad
    wc = WordCloud(
        width=width,
        height=height,
        background_color='white',
        colormap='viridis',
        relative_scaling=0.5,
        min_font_size=10,
        max_words=max_words,
        random_state=42  # Semilla fija para que siempre genere el mismo layout
    ).generate_from_frequencies(word_freq)
    
    # Convertir a imagen
    fig, ax = plt.subplots(figsize=(width/100, height/100), dpi=100)
    ax.imshow(wc, interpolation='bilinear')
    ax.axis('off')
    plt.tight_layout(pad=0)
    
    # Guardar en buffer
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
    buf.seek(0)
    plt.close()
    
    return buf


def export_to_excel(model, pub_dates):
    """Exporta todos los resultados a un archivo Excel"""
    output = BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Hoja 1: Resumen de tópicos
        topic_sizes, topic_nums = model.get_topic_sizes()
        
        # Obtener todas las palabras de los tópicos una sola vez
        all_topic_words, all_word_scores, _ = model.get_topics()
        
        resumen_data = []
        for i, topic_num in enumerate(topic_nums):
            words = all_topic_words[i]
            word_scores = all_word_scores[i]
            
            # Limpiar y deduplicar palabras
            clean_words, clean_scores = clean_topic_words(words, word_scores, target_count=10)
            
            resumen_data.append({
                'topic_id': topic_num,
                'num_documentos': topic_sizes[i],
                'palabras_clave': ', '.join(clean_words),
                **{f'palabra_{j+1}': clean_words[j] if j < len(clean_words) else '' for j in range(10)},
                **{f'score_{j+1}': round(clean_scores[j], 4) if j < len(clean_scores) else 0 for j in range(10)}
            })
        
        df_resumen = pd.DataFrame(resumen_data)
        df_resumen.to_excel(writer, sheet_name='Resumen_Topicos', index=False)
        
        # Hoja 2: Series temporales
        # Usar directamente doc_top que ya fue calculado por Top2Vec
        topic_assignments = model.doc_top
        
        df_temporal = pd.DataFrame({
            'fecha': pd.to_datetime(pub_dates),
            'topico': topic_assignments
        })
        
        pivot = df_temporal.groupby([df_temporal['fecha'].dt.date, 'topico']).size().unstack(fill_value=0)
        pivot.to_excel(writer, sheet_name='Series_Temporales')
        
        # Hoja 3: Metadata
        metadata = pd.DataFrame([{
            'total_topicos': len(topic_nums),
            'total_documentos': len(all_doc_ids),
            'fecha_generacion': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }])
        metadata.to_excel(writer, sheet_name='Metadata', index=False)
    
    output.seek(0)
    return output


# =============================================================================
# INTERFAZ PRINCIPAL
# =============================================================================

def main():
    # Header
    st.markdown('<h1 class="main-header">📊 Top2Vec - Análisis de Tópicos para Economistas</h1>', 
                unsafe_allow_html=True)
    
    # Inicializar session state
    if 'trained_model' not in st.session_state:
        st.session_state.trained_model = None
    if 'trained_model_data' not in st.session_state:
        st.session_state.trained_model_data = None
    if 'current_model' not in st.session_state:
        st.session_state.current_model = None
    if 'current_model_data' not in st.session_state:
        st.session_state.current_model_data = None
    
    # Tabs principales
    tab1, tab2, tab3 = st.tabs(["🎯 Entrenar Modelo", "📊 Explorar Resultados", "📖 Ayuda y Documentación"])
    
    with tab1:
        render_training_tab()
    
    with tab2:
        render_exploration_tab()
    
    with tab3:
        render_help_tab()


# =============================================================================
# TAB 1: ENTRENAR MODELO
# =============================================================================

def render_training_tab():
    st.markdown("### 🎯 Configuración y Entrenamiento del Modelo")
    
    st.markdown("""
    <div class="info-card">
        <strong>ℹ️ Información:</strong><br>
        Los embeddings ya están precalculados, por lo que el entrenamiento tomará aproximadamente 15-30 minutos.
        Durante el proceso verás actualizaciones en tiempo real del progreso.
    </div>
    """, unsafe_allow_html=True)
    
    # Configuración en columnas
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 📋 Configuración Básica")
        
        # Filtro de datos
        st.markdown("##### 📅 Filtro de Datos (opcional)")
        
        use_date_filter = st.checkbox(
            "Filtrar por rango de fechas",
            value=False,
            help="Entrenar solo con un subset de datos para pruebas rápidas"
        )
        
        start_year = None
        end_year = None
        
        if use_date_filter:
            col_start, col_end = st.columns(2)
            with col_start:
                start_year = st.number_input(
                    "Año inicial",
                    min_value=2008,
                    max_value=2024,
                    value=2020,
                    step=1,
                    help="Ejemplo: 2020 para entrenar desde 2020 en adelante"
                )
            with col_end:
                end_year = st.number_input(
                    "Año final",
                    min_value=2008,
                    max_value=2024,
                    value=2024,
                    step=1,
                    help="Ejemplo: 2024 para entrenar hasta 2024"
                )
            
            st.info(f"📊 Se entrenarán solo documentos entre {start_year} y {end_year}")
        
        # Presets
        preset = st.selectbox(
            "Preset de Configuración",
            ["Análisis General (Recomendado)", "Temas Emergentes", "Macro-Temas", "Personalizado"],
            help="Selecciona un preset predefinido o personaliza los parámetros"
        )
        
        # Nombre del modelo
        model_name = st.text_input(
            "Nombre del Modelo",
            value=f"modelo_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            help="Nombre único para identificar este modelo"
        )
        
        # Archivos de datos
        st.markdown("##### 📂 Archivos de Datos")
        data_file = st.text_input("Archivo de Noticias (CSV)", value="data/noticias.csv")
        embeddings_file = st.text_input("Archivo de Embeddings (NPZ)", value="data/embeddings_precalculados.npz")
    
    with col2:
        st.markdown("#### ⚙️ Parámetros del Modelo")
        
        show_advanced = st.checkbox("Mostrar parámetros avanzados", value=False)
        
        # Cargar preset
        if preset == "Análisis General (Recomendado)":
            default_config = {
                'min_cluster_size': 50,
                'min_samples': 25,
                'n_neighbors': 50,
                'n_components': 5,
                'topic_merge_delta': 0.1
            }
        elif preset == "Temas Emergentes":
            default_config = {
                'min_cluster_size': 30,
                'min_samples': 15,
                'n_neighbors': 30,
                'n_components': 5,
                'topic_merge_delta': 0.08
            }
        elif preset == "Macro-Temas":
            default_config = {
                'min_cluster_size': 75,
                'min_samples': 40,
                'n_neighbors': 70,
                'n_components': 5,
                'topic_merge_delta': 0.12
            }
        else:
            default_config = {
                'min_cluster_size': 50,
                'min_samples': 25,
                'n_neighbors': 50,
                'n_components': 5,
                'topic_merge_delta': 0.1
            }
        
        if show_advanced:
            st.markdown("##### 🔍 HDBSCAN (Agrupación)")
            
            min_cluster_size = st.slider(
                "Tamaño Mínimo de Cluster",
                min_value=10, max_value=200, value=default_config['min_cluster_size'], step=5,
                help="Mínimo de documentos para formar un tópico. ↑ = tópicos más grandes"
            )
            
            min_samples = st.slider(
                "Muestras Mínimas",
                min_value=5, max_value=100, value=default_config['min_samples'], step=5,
                help="Densidad mínima para identificar un tópico. ↑ = tópicos más robustos"
            )
            
            st.markdown("##### 🗺️ UMAP (Reducción Dimensional)")
            
            n_neighbors = st.slider(
                "Número de Vecinos",
                min_value=10, max_value=200, value=default_config['n_neighbors'], step=10,
                help="Vecinos cercanos a considerar. ↑ = estructura global, ↓ = estructura local"
            )
            
            n_components = st.slider(
                "Componentes",
                min_value=2, max_value=10, value=default_config['n_components'], step=1,
                help="Dimensiones en el espacio reducido (típicamente 2-10)"
            )
            
            st.markdown("##### 🔗 Fusión de Tópicos")
            
            topic_merge_delta = st.slider(
                "Delta de Fusión",
                min_value=0.01, max_value=0.30, value=default_config['topic_merge_delta'], step=0.01,
                help="Similitud mínima para fusionar tópicos. ↑ = fusiona más"
            )
        else:
            min_cluster_size = default_config['min_cluster_size']
            min_samples = default_config['min_samples']
            n_neighbors = default_config['n_neighbors']
            n_components = default_config['n_components']
            topic_merge_delta = default_config['topic_merge_delta']
            
            st.info(f"""
            **Usando preset '{preset}':**
            - Min Cluster Size: {min_cluster_size}
            - Min Samples: {min_samples}
            - N Neighbors: {n_neighbors}
            - N Components: {n_components}
            - Topic Merge Delta: {topic_merge_delta}
            """)
    
    # Botón de entrenamiento
    st.markdown("---")
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
    
    with col_btn2:
        train_button = st.button("🚀 Entrenar Modelo", type="primary", use_container_width=True)
    
    if train_button:
        train_model(
            model_name=model_name,
            data_file=data_file,
            embeddings_file=embeddings_file,
            config={
                'min_cluster_size': min_cluster_size,
                'min_samples': min_samples,
                'n_neighbors': n_neighbors,
                'n_components': n_components,
                'topic_merge_delta': topic_merge_delta
            },
            date_filter={'start_year': start_year, 'end_year': end_year} if use_date_filter else None
        )


def train_model(model_name, data_file, embeddings_file, config, date_filter=None):
    """Ejecuta el entrenamiento del modelo con visualización de progreso"""
    
    # Contenedor de progreso
    progress_container = st.container()
    
    with progress_container:
        st.markdown("### 🔄 Entrenamiento en Progreso")
        
        # Barra de progreso
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Métricas en tiempo real
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            metric_tiempo = st.empty()
        with col2:
            metric_cpu = st.empty()
        with col3:
            metric_memoria = st.empty()
        with col4:
            metric_eta = st.empty()
        
        # Log de mensajes
        log_container = st.expander("📋 Ver log detallado", expanded=True)
        log_text = log_container.empty()
        
        logs = []
        start_time = time.time()
        
        try:
            # Paso 1: Validar archivos
            progress_bar.progress(5)
            status_text.text("Validando archivos...")
            logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] Validando archivos...")
            log_text.text('\n'.join(logs[-20:]))
            
            if not os.path.exists(data_file):
                st.error(f"❌ No se encuentra el archivo: {data_file}")
                return
            
            if not os.path.exists(embeddings_file):
                st.error(f"❌ No se encuentra el archivo: {embeddings_file}")
                return
            
            # Paso 2: Cargar datos
            progress_bar.progress(10)
            status_text.text("Cargando embeddings y datos...")
            logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] Cargando embeddings...")
            log_text.text('\n'.join(logs[-20:]))
            
            embedding_provider = PrecomputedEmbeddings(embeddings_file, data_file)
            
            resources = get_system_resources()
            metric_cpu.metric("CPU", f"{resources['cpu_percent']:.1f}%")
            metric_memoria.metric("RAM", f"{resources['memory_percent']:.1f}%")
            
            logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Embeddings cargados: {len(embedding_provider.embeddings):,} docs")
            log_text.text('\n'.join(logs[-20:]))
            
            # Paso 3: Preparar documentos
            progress_bar.progress(20)
            status_text.text("Preparando documentos...")
            
            # Aplicar filtro de fechas si está configurado
            if date_filter and date_filter['start_year'] and date_filter['end_year']:
                logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] 📅 Aplicando filtro de fechas: {date_filter['start_year']}-{date_filter['end_year']}")
                log_text.text('\n'.join(logs[-20:]))
                
                # Convertir pub_dates a datetime si no lo está
                pub_dates_dt = pd.to_datetime(embedding_provider.pub_dates)
                
                # Crear máscara de fechas
                start_date = pd.Timestamp(f"{date_filter['start_year']}-01-01")
                end_date = pd.Timestamp(f"{date_filter['end_year']}-12-31")
                
                date_mask = (pub_dates_dt >= start_date) & (pub_dates_dt <= end_date)
                indices_filtrados = np.where(date_mask)[0]
                
                # Filtrar todos los datos
                original_count = len(embedding_provider.embeddings)
                embedding_provider.embeddings = embedding_provider.embeddings[indices_filtrados]
                embedding_provider.pub_dates = embedding_provider.pub_dates[indices_filtrados]
                embedding_provider.doc_ids = embedding_provider.doc_ids[indices_filtrados]
                
                if embedding_provider.documents:
                    embedding_provider.documents = [embedding_provider.documents[i] for i in indices_filtrados]
                
                filtered_count = len(embedding_provider.embeddings)
                logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Filtrado: {original_count:,} → {filtered_count:,} docs ({filtered_count/original_count*100:.1f}%)")
                log_text.text('\n'.join(logs[-20:]))
            
            # IMPORTANTE: Usar documentos del NPZ (ya tokenizados/procesados)
            if embedding_provider.documents:
                documents = embedding_provider.documents
                logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Textos cargados: {len(documents):,}")
            else:
                documents = [f"Document {i}" for i in range(len(embedding_provider.embeddings))]
                logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] ⚠️ Usando placeholders")
            
            log_text.text('\n'.join(logs[-20:]))
            
            # CRÍTICO: Siempre convertir doc_ids a strings (igual que código original)
            # Esto es necesario para que Top2Vec funcione correctamente con embeddings precomputados
            document_ids = [str(doc_id) for doc_id in embedding_provider.doc_ids.tolist()]
            logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] 📋 IDs de documentos: {len(document_ids)} (como strings)")
            log_text.text('\n'.join(logs[-20:]))
            
            # Paso 4: Entrenar modelo
            progress_bar.progress(30)
            status_text.text("Entrenando Top2Vec (esto puede tomar 15-30 minutos)...")
            logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] 🚀 Iniciando entrenamiento Top2Vec...")
            logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] Configuración:")
            logs.append(f"  • min_cluster_size: {config['min_cluster_size']}")
            logs.append(f"  • min_samples: {config['min_samples']}")
            logs.append(f"  • n_neighbors: {config['n_neighbors']}")
            logs.append(f"  • n_components: {config['n_components']}")
            logs.append(f"  • topic_merge_delta: {config['topic_merge_delta']}")
            log_text.text('\n'.join(logs[-20:]))
            
            # Actualizar métricas cada 5 segundos durante el entrenamiento
            training_start = time.time()
            
            # Configuración UMAP y HDBSCAN
            umap_args = {
                'n_neighbors': config['n_neighbors'],
                'n_components': config['n_components'],
                'metric': 'cosine',
                'random_state': 42
            }
            
            hdbscan_args = {
                'min_cluster_size': config['min_cluster_size'],
                'min_samples': config['min_samples'],
                'metric': 'euclidean',
                'cluster_selection_method': 'eom'
            }
            
            # Entrenar usando método del notebook (crear modelo vacío y asignar atributos)
            # Este es el método que se usó para crear el modelo funcional original
            logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] 🔧 Creando modelo desde embeddings precomputados...")
            log_text.text('\n'.join(logs[-20:]))
            
            # Usar word_vectors y vocab del embedding_provider
            word_vectors = embedding_provider.word_vectors
            vocab = embedding_provider.vocab.tolist() if isinstance(embedding_provider.vocab, np.ndarray) else embedding_provider.vocab
            word_indexes = embedding_provider.word_indexes
            
            logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Word vectors: {word_vectors.shape}")
            logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Vocabulario: {len(vocab)} palabras")
            log_text.text('\n'.join(logs[-20:]))
            
            # Crear instancia vacía de Top2Vec (método del notebook)
            model = Top2Vec.__new__(Top2Vec)
            
            # Asignar atributos básicos
            model.documents = np.array(documents, dtype="object")
            model.num_documents = len(documents)
            model.document_ids = np.array([str(i) for i in range(len(documents))])
            model.doc_id2index = dict(zip(model.document_ids, list(range(len(model.document_ids)))))
            model.doc_id_type = np.str_
            model.document_ids_provided = False
            
            # Asignar embeddings precomputados
            model.document_vectors = embedding_provider.embeddings
            model.word_vectors = word_vectors
            model.vocab = vocab
            model.word_indexes = word_indexes
            model.embedding_model = 'precomputed'
            
            # Inicializar variables de indexación
            model.topic_index = None
            model.serialized_topic_index = None
            model.topics_indexed = False
            model.document_index = None
            model.serialized_document_index = None
            model.documents_indexed = False
            model.index_id2doc_id = None
            model.doc_id2index_id = None
            model.word_index = None
            model.serialized_word_index = None
            model.words_indexed = False
            model.contextual_top2vec = False
            model.verbose = False
            
            logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Modelo base creado")
            log_text.text('\n'.join(logs[-20:]))
            
            # Ejecutar clustering y generación de tópicos
            progress_bar.progress(50)
            logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] 🎯 Ejecutando clustering UMAP + HDBSCAN...")
            log_text.text('\n'.join(logs[-20:]))
            
            model.compute_topics(
                umap_args=umap_args,
                hdbscan_args=hdbscan_args,
                topic_merge_delta=config['topic_merge_delta'],
                gpu_umap=False,
                gpu_hdbscan=False,
                index_topics=False
            )
            
            progress_bar.progress(90)
            
            elapsed = time.time() - training_start
            logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Entrenamiento completado en {elapsed/60:.1f} minutos")
            logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] 📊 Tópicos encontrados: {model.get_num_topics()}")
            
            # DEBUG: Verificar estado del modelo
            logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] 🔍 DEBUG: len(document_vectors) = {len(model.document_vectors)}")
            logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] 🔍 DEBUG: len(doc_top) = {len(model.doc_top)}")
            logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] 🔍 DEBUG: document_ids[:5] = {model.document_ids[:5]}")
            logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] 🔍 DEBUG: document_ids dtype = {model.document_ids.dtype}")
            logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] 🔍 DEBUG: doc_top[:5] = {model.doc_top[:5]}")
            
            log_text.text('\n'.join(logs[-20:]))
            
            # Paso 5: Guardar modelo
            progress_bar.progress(95)
            status_text.text("Guardando modelo...")
            
            model_dir = Path('modelos') / model_name
            model_dir.mkdir(parents=True, exist_ok=True)
            
            model_path = model_dir / 'modelo.model'
            model.save(str(model_path))
            
            logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] 💾 Modelo guardado: {model_path}")
            log_text.text('\n'.join(logs[-20:]))
            
            # Guardar fechas junto con el modelo
            pub_dates_path = model_dir / 'pub_dates.npy'
            np.save(pub_dates_path, embedding_provider.pub_dates)
            logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] 💾 Fechas guardadas: {pub_dates_path}")
            log_text.text('\n'.join(logs[-20:]))
            
            # Guardar metadata
            total_time = time.time() - start_time
            metadata_path = save_model_metadata(config, model_path, model.get_num_topics(), total_time)
            
            logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] 💾 Metadata guardada: {metadata_path}")
            log_text.text('\n'.join(logs[-20:]))
            
            # Calcular asignaciones de tópicos
            progress_bar.progress(97)
            status_text.text("Preparando asignaciones de tópicos...")
            logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] 📊 Obteniendo asignaciones de tópicos...")
            log_text.text('\n'.join(logs[-20:]))
            
            # Usar directamente doc_top y doc_dist que ya fueron calculados por Top2Vec
            num_docs = len(model.document_vectors)
            topic_assignments = model.doc_top  # Ya calculado internamente
            topic_scores_flat = model.doc_dist  # Ya calculado internamente
            
            logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Asignaciones calculadas")
            log_text.text('\n'.join(logs[-20:]))
            
            # Generar archivo Excel con resultados completos
            progress_bar.progress(99)
            status_text.text("Generando archivo de resultados...")
            logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] 📄 Generando Excel con resultados...")
            log_text.text('\n'.join(logs[-20:]))
            
            # Obtener palabras clave de cada tópico
            all_topic_words, all_word_scores, _ = model.get_topics()
            
            # Crear DataFrame con todos los documentos
            results_df = pd.DataFrame({
                'doc_id': range(num_docs),
                'topico': topic_assignments,
                'score_topico': topic_scores_flat,
                'fecha': pd.to_datetime(embedding_provider.pub_dates[:num_docs])
            })
            
            # Agregar palabras clave del tópico asignado (limpias)
            def get_clean_keywords(topic_id):
                words = all_topic_words[topic_id]
                scores = all_word_scores[topic_id]
                clean_w, clean_s = clean_topic_words(words, scores, target_count=10)
                return ', '.join(clean_w)
            
            results_df['palabras_clave'] = results_df['topico'].apply(get_clean_keywords)
            
            # Si hay documentos originales, agregarlos
            if embedding_provider.documents:
                results_df['texto'] = embedding_provider.documents[:num_docs]
            
            # Reordenar columnas
            cols = ['doc_id', 'topico', 'score_topico', 'fecha', 'palabras_clave']
            if 'texto' in results_df.columns:
                cols.append('texto')
            results_df = results_df[cols]
            
            # Guardar Excel
            results_path = model_dir / 'resultados_completos.xlsx'
            with pd.ExcelWriter(results_path, engine='openpyxl') as writer:
                # Hoja 1: Todos los documentos con sus tópicos
                results_df.to_excel(writer, sheet_name='Documentos_y_Topicos', index=False)
                
                # Hoja 2: Resumen de tópicos
                topic_sizes, topic_nums_sorted = model.get_topic_sizes()
                summary_data = []
                for i, topic_num in enumerate(topic_nums_sorted):
                    words = all_topic_words[i]
                    word_scores = all_word_scores[i]
                    # Limpiar y deduplicar palabras
                    clean_words, clean_scores = clean_topic_words(words, word_scores, target_count=10)
                    summary_data.append({
                        'topico_id': topic_num,
                        'num_documentos': topic_sizes[i],
                        'porcentaje': f"{(topic_sizes[i]/num_docs)*100:.2f}%",
                        'top_10_palabras': ', '.join(clean_words),
                        **{f'palabra_{j+1}': clean_words[j] if j < len(clean_words) else '' for j in range(10)}
                    })
                
                df_summary = pd.DataFrame(summary_data)
                df_summary.to_excel(writer, sheet_name='Resumen_Topicos', index=False)
                
                # Hoja 3: Evolución temporal por tópico
                temporal_data = []
                for topic_num in topic_nums_sorted[:20]:  # Top 20 tópicos
                    topic_docs = results_df[results_df['topico'] == topic_num]
                    monthly = topic_docs.set_index('fecha').resample('M').size()
                    for date, count in monthly.items():
                        if count > 0:
                            temporal_data.append({
                                'topico': topic_num,
                                'fecha': date,
                                'num_docs': count
                            })
                
                if temporal_data:
                    df_temporal = pd.DataFrame(temporal_data)
                    df_temporal.to_excel(writer, sheet_name='Evolucion_Temporal', index=False)
            
            logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] 💾 Resultados guardados: {results_path}")
            log_text.text('\n'.join(logs[-20:]))
            
            # Completar
            progress_bar.progress(100)
            status_text.text("✅ Entrenamiento completado!")
            
            # Actualizar métricas finales
            metric_tiempo.metric("Tiempo Total", f"{total_time/60:.1f} min")
            resources = get_system_resources()
            metric_cpu.metric("CPU", f"{resources['cpu_percent']:.1f}%")
            metric_memoria.metric("RAM", f"{resources['memory_percent']:.1f}%")
            metric_eta.metric("Tópicos", f"{model.get_num_topics()}")
            
            # Guardar en session state
            st.session_state.trained_model = model
            st.session_state.trained_model_data = {
                'name': model_name,
                'path': str(model_path),
                'pub_dates': embedding_provider.pub_dates,
                'metadata': load_model_metadata(model_dir),
                'topic_assignments': topic_assignments,
                'results_path': str(results_path)
            }
            st.session_state.current_model = model
            st.session_state.current_model_data = st.session_state.trained_model_data
            
            # Mensaje de éxito con ubicación de archivos
            st.success(f"""
            ✅ **Modelo entrenado exitosamente!**
            
            - Tópicos encontrados: {model.get_num_topics()}
            - Documentos procesados: {num_docs:,}
            - Tiempo total: {total_time/60:.1f} minutos
            """)
            
            # Mostrar ubicación de archivos generados
            st.info(f"""
            📁 **Archivos generados:**
            
            **Modelo:** `{model_path}`
            
            **Resultados completos:** `{results_path}`
            
            El archivo Excel contiene 3 hojas:
            - **Documentos_y_Topicos**: Todos los documentos con su tópico asignado
            - **Resumen_Topicos**: Estadísticas de cada tópico
            - **Evolucion_Temporal**: Evolución mensual de los top 20 tópicos
            
            💡 Puedes abrir el Excel directamente desde la ubicación mostrada.
            """)

            
        except Exception as e:
            progress_bar.progress(0)
            status_text.text("")
            st.error(f"❌ Error durante el entrenamiento: {str(e)}")
            logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ ERROR: {str(e)}")
            log_text.text('\n'.join(logs[-20:]))


# =============================================================================
# TAB 2: EXPLORAR RESULTADOS
# =============================================================================

def render_exploration_tab():
    st.markdown("### 📊 Exploración de Resultados")
    
    # Selector de modelo
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Opción 1: Usar modelo recién entrenado
        if st.session_state.trained_model is not None:
            use_trained = st.checkbox(
                "📌 Usar modelo recién entrenado",
                value=True,
                help="Explorar el modelo que acabas de entrenar"
            )
            
            if use_trained:
                st.info(f"✅ Modelo activo: **{st.session_state.trained_model_data['name']}**")
                render_topic_explorer(
                    st.session_state.trained_model,
                    st.session_state.trained_model_data
                )
                return
        
        # Opción 2: Cargar modelo existente
        st.markdown("#### 📂 Cargar Modelo Existente")
        
        available_models = list_available_models()
        
        if not available_models:
            st.warning("No hay modelos guardados. Entrena un modelo primero en la pestaña 'Entrenar Nuevo Modelo'.")
            return
        
        model_options = {
            f"{m['name']} ({m['metadata']['timestamp'][:10]})": m 
            for m in available_models
        }
        
        selected_model_name = st.selectbox(
            "Selecciona un modelo",
            options=list(model_options.keys()),
            help="Modelos guardados ordenados por fecha (más recientes primero)"
        )
        
        selected_model = model_options[selected_model_name]
        
        # Mostrar info del modelo
        with st.expander("ℹ️ Información del Modelo", expanded=True):
            metadata = selected_model['metadata']
            
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                st.metric("Tópicos", metadata['num_topics'])
            with col_b:
                st.metric("Tiempo de Entrenamiento", f"{metadata['execution_time_seconds']/60:.1f} min")
            with col_c:
                st.metric("Fecha", metadata['timestamp'][:10])
            
            st.json(metadata['config'])
        
        # Botón para cargar
        if st.button("📥 Cargar Modelo", type="primary"):
            with st.spinner("Cargando modelo..."):
                try:
                    model_dir = Path(selected_model['path'])
                    model_path = model_dir / 'modelo.model'
                    model = Top2Vec.load(str(model_path))
                    
                    # Intentar cargar fechas del modelo guardado primero
                    pub_dates_path = model_dir / 'pub_dates.npy'
                    if pub_dates_path.exists():
                        pub_dates = np.load(pub_dates_path)
                    else:
                        # Fallback: cargar del archivo de embeddings original
                        embeddings_file = "data/embeddings_precalculados.npz"
                        if Path(embeddings_file).exists():
                            data = np.load(embeddings_file, allow_pickle=True)
                            # Intentar cargar pub_dates de diferentes fuentes
                            if 'metadata' in data:
                                metadata_npz = data['metadata'].item()
                                pub_dates = metadata_npz.get('pub_date', np.arange(len(model.document_vectors)))
                            elif 'pub_date' in data:
                                pub_dates = data['pub_date']
                            else:
                                pub_dates = np.arange(len(model.document_vectors))
                        else:
                            pub_dates = np.arange(len(model.document_vectors))
                    
                    # Obtener asignaciones de tópicos directamente
                    with st.spinner("Cargando asignaciones de tópicos..."):
                        # Usar doc_top que ya fue calculado por Top2Vec
                        topic_assignments = model.doc_top
                    
                    st.session_state.current_model = model
                    st.session_state.current_model_data = {
                        'name': selected_model['name'],
                        'path': str(model_path),
                        'pub_dates': pub_dates,
                        'metadata': metadata,
                        'topic_assignments': topic_assignments  # Guardar asignaciones
                    }
                    
                    st.success(f"✅ Modelo '{selected_model['name']}' cargado exitosamente!")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Error al cargar el modelo: {str(e)}")
    
    # Si hay un modelo cargado, mostrar el explorador
    if st.session_state.current_model is not None:
        st.markdown("---")
        render_topic_explorer(
            st.session_state.current_model,
            st.session_state.current_model_data
        )


def render_topic_explorer(model, model_data):
    """Renderiza el explorador interactivo de tópicos"""
    
    st.markdown("### 🔍 Explorador de Tópicos")
    
    # Obtener información del modelo
    topic_sizes, topic_nums = model.get_topic_sizes()
    num_topics = len(topic_nums)
    
    # Header con métricas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total de Tópicos", num_topics)
    with col2:
        st.metric("Total de Documentos", sum(topic_sizes))
    with col3:
        st.metric("Promedio Docs/Tópico", f"{sum(topic_sizes)/num_topics:.0f}")
    with col4:
        st.metric("Tópico Más Grande", f"{max(topic_sizes):,}")
    
    st.markdown("---")
    
    # Selector de tópico
    topic_options = [
        f"Tópico {num} ({topic_sizes[i]:,} docs)" 
        for i, num in enumerate(topic_nums)
    ]
    
    selected_topic_idx = st.selectbox(
        "Selecciona un tópico para explorar",
        range(len(topic_options)),
        format_func=lambda x: topic_options[x]
    )
    
    selected_topic_num = topic_nums[selected_topic_idx]
    
    # Obtener información del tópico
    # Cachear palabras de tópicos en session_state para evitar recalcular
    # Usar el path del modelo como identificador único
    current_model_id = model_data.get('path', id(model))
    
    if ('cached_topic_words' not in st.session_state or 
        'cached_model_id' not in st.session_state or 
        st.session_state.cached_model_id != current_model_id):
        all_topic_words, all_word_scores, _ = model.get_topics()
        st.session_state.cached_topic_words = all_topic_words
        st.session_state.cached_word_scores = all_word_scores
        st.session_state.cached_model_id = current_model_id
    
    words = st.session_state.cached_topic_words[selected_topic_num]
    word_scores = st.session_state.cached_word_scores[selected_topic_num]
    
    # Limpiar y deduplicar palabras (eliminar variantes con puntuación)
    top_words, top_scores = clean_topic_words(words, word_scores, target_count=20)
    
    # Layout en dos columnas (más ancho)
    col_left, col_right = st.columns([1.2, 1.8])
    
    with col_left:
        st.markdown(f"#### ☁️ WordCloud - Tópico {selected_topic_num}")
        
        # Generar wordcloud
        try:
            wc_image = create_wordcloud_image(top_words, top_scores, width=800, height=500)
            st.image(wc_image, use_container_width=True)
            
            # Botón de descarga del WordCloud
            st.download_button(
                label="💾 Descargar WordCloud (PNG)",
                data=wc_image,
                file_name=f"wordcloud_topico_{selected_topic_num}.png",
                mime="image/png",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Error generando wordcloud: {e}")
        
        # Tabla de palabras clave
        st.markdown("##### 📝 Palabras Clave")
        
        df_words = pd.DataFrame({
            'Palabra': top_words,
            'Relevancia': [f"{score:.4f}" for score in top_scores]
        })
        
        st.dataframe(df_words, use_container_width=True, height=400)
    
    with col_right:
        st.markdown(f"#### 📈 Evolución Temporal - Tópico {selected_topic_num}")
        
        # Selector de frecuencia de agrupación
        freq_option = st.selectbox(
            "Frecuencia de agrupación",
            ["Diaria", "Semanal", "Mensual", "Trimestral", "Anual"],
            index=2,  # Mensual por defecto
            key=f"freq_{selected_topic_num}"
        )
        
        freq_map = {
            "Diaria": "D",
            "Semanal": "W",
            "Mensual": "M",
            "Trimestral": "Q",
            "Anual": "Y"
        }
        
        # Crear serie temporal
        try:
            # Usar las asignaciones de tópicos pre-calculadas
            if 'topic_assignments' not in model_data:
                st.error("Las asignaciones de tópicos no están disponibles. Por favor, recarga el modelo.")
                return
            
            topic_assignments = model_data['topic_assignments']
            pub_dates_subset = model_data['pub_dates'][:len(topic_assignments)]
            
            # Convertir fechas a datetime
            fechas = pd.to_datetime(pub_dates_subset)
            
            df_temporal = pd.DataFrame({
                'fecha': fechas,
                'topico': topic_assignments
            })
            
            # Filtrar por tópico seleccionado
            df_topic = df_temporal[df_temporal['topico'] == selected_topic_num].copy()
            
            if len(df_topic) == 0:
                st.warning(f"No hay documentos en el tópico {selected_topic_num}")
            else:
                # Agrupar por la frecuencia seleccionada
                df_topic = df_topic.set_index('fecha')
                conteo = df_topic.resample(freq_map[freq_option]).size().reset_index(name='frecuencia')
                conteo.columns = ['fecha', 'frecuencia']
                
                # Filtrar fechas con frecuencia > 0
                conteo = conteo[conteo['frecuencia'] > 0]
                
                # Gráfico interactivo
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(
                    x=conteo['fecha'],
                    y=conteo['frecuencia'],
                    mode='lines+markers',
                    name=f'Tópico {selected_topic_num}',
                    line=dict(color='#1f77b4', width=2),
                    marker=dict(size=6),
                    hovertemplate='<b>Fecha:</b> %{x|%Y-%m-%d}<br><b>Documentos:</b> %{y}<extra></extra>'
                ))
                
                fig.update_layout(
                    title=f"Frecuencia {freq_option} de Documentos - Tópico {selected_topic_num}",
                    xaxis_title="Fecha",
                    yaxis_title="Número de Documentos",
                    hovermode='x unified',
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Botón para descargar gráfico
                fig_bytes = fig.to_image(format="png", width=1200, height=600)
                st.download_button(
                    label="💾 Descargar Gráfico (PNG)",
                    data=fig_bytes,
                    file_name=f"evolucion_temporal_topico_{selected_topic_num}_{freq_option.lower()}.png",
                    mime="image/png",
                    use_container_width=True
                )
                
                # Estadísticas temporales
                st.markdown("##### 📊 Estadísticas Temporales")
                
                col_a, col_b, col_c, col_d = st.columns(4)
                
                with col_a:
                    st.metric("Total Docs", len(df_topic))
                with col_b:
                    st.metric(f"Promedio {freq_option}", f"{conteo['frecuencia'].mean():.1f}")
                with col_c:
                    st.metric(f"Máximo {freq_option}", conteo['frecuencia'].max())
                with col_d:
                    fecha_min = df_topic.index.min().strftime('%Y-%m-%d')
                    fecha_max = df_topic.index.max().strftime('%Y-%m-%d')
                    st.metric("Rango", f"{fecha_min} a {fecha_max}")
            
        except Exception as e:
            st.error(f"Error generando serie temporal: {e}")
    
    # Sección de análisis adicionales
    st.markdown("---")
    st.markdown("### 📑 Análisis Adicionales")
    
    with st.expander("📄 Ver Documentos Representativos", expanded=False):
        try:
            documents, document_scores, document_ids = model.search_documents_by_topic(
                topic_num=selected_topic_num,
                num_docs=5
            )
            
            for i, (doc, score, doc_id) in enumerate(zip(documents, document_scores, document_ids), 1):
                st.markdown(f"**Documento {i}** (ID: {doc_id}, Relevancia: {score:.3f})")
                st.text_area(
                    label="",
                    value=doc[:500] + "..." if len(doc) > 500 else doc,
                    height=100,
                    key=f"doc_{i}",
                    label_visibility="collapsed"
                )
        except Exception as e:
            st.error(f"Error obteniendo documentos: {e}")
    
    with st.expander("📊 Distribución de Documentos", expanded=False):
        try:
            # Gráfico de barras de todos los tópicos
            df_distribution = pd.DataFrame({
                'Tópico': [f"Tópico {num}" for num in topic_nums],
                'Documentos': topic_sizes
            })
            
            fig_dist = px.bar(
                df_distribution,
                x='Tópico',
                y='Documentos',
                title="Distribución de Documentos por Tópico",
                color='Documentos',
                color_continuous_scale='viridis'
            )
            
            fig_dist.update_layout(height=400)
            st.plotly_chart(fig_dist, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error generando distribución: {e}")
    
    # Sección de archivo de resultados
    st.markdown("---")
    st.markdown("### 📊 Resultados Completos")
    
    # Determinar la ruta del archivo de resultados
    if 'results_path' in model_data:
        results_path = Path(model_data['results_path'])
    else:
        # Construir ruta esperada basada en el path del modelo
        model_dir = Path(model_data['path']).parent
        results_path = model_dir / 'resultados_completos.xlsx'
    
    # Verificar si existe el archivo
    if results_path.exists():
        st.info(f"""
        📁 **Archivo de resultados completos generado automáticamente:**
        
        `{results_path}`
        
        El archivo Excel contiene 3 hojas:
        - **Documentos_y_Topicos**: Lista completa de todos los documentos con su tópico asignado, fecha, score, y palabras clave
        - **Resumen_Topicos**: Resumen estadístico de cada tópico
        - **Evolucion_Temporal**: Evolución mensual de los top 20 tópicos
        """)
        
        # Botón para descargar el archivo de resultados
        with open(results_path, 'rb') as f:
            st.download_button(
                label="📥 Descargar Resultados Completos (Excel)",
                data=f.read(),
                file_name=f"resultados_{model_data['name']}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                type="primary"
            )
    else:
        st.info(f"""
        📁 **El archivo con los datos completos está en la ruta:**
        
        `{results_path}`
        
        *Nota: Si el archivo no existe aún, se generará automáticamente cuando vuelvas a entrenar un modelo.*
        """)


# =============================================================================
# TAB 3: AYUDA Y DOCUMENTACIÓN
# =============================================================================

def render_help_tab():
    """Renderiza la pestaña de ayuda y documentación dentro de la app"""
    
    st.markdown("## 📖 Ayuda y Documentación")
    
    # Subtabs para organizar la documentación
    help_tab1, help_tab2, help_tab3, help_tab4, help_tab5, help_tab6 = st.tabs([
        "📚 Fundamentos Top2Vec",
        "🚀 Inicio Rápido",
        "📊 Datos y Configuración",
        "🎯 Cómo Usar",
        "❓ Preguntas Frecuentes",
        "🔧 Solución de Problemas"
    ])
    
    with help_tab1:
        render_top2vec_fundamentals()
    
    with help_tab2:
        render_quick_start_help()
    
    with help_tab3:
        render_data_info_help()
    
    with help_tab4:
        render_usage_help()
    
    with help_tab5:
        render_faq_help()
    
    with help_tab6:
        render_troubleshooting_help()


def render_top2vec_fundamentals():
    """Fundamentos teóricos y metodológicos de Top2Vec"""
    st.markdown("### 📚 Fundamentos de Top2Vec")
    
    st.markdown("""
    <div class="info-card">
    <strong>📖 Fundamentación Científica</strong><br>
    Top2Vec es un algoritmo de modelado de tópicos basado en embeddings densos y clustering 
    no supervisado, publicado en 2020 por Dimo Angelov.
    </div>
    """, unsafe_allow_html=True)
    
    # Sub-tabs para organizar teoría
    theory_tab1, theory_tab2, theory_tab3, theory_tab4, theory_tab5 = st.tabs([
        "🧠 ¿Qué es Top2Vec?",
        "⚙️ Cómo Funciona",
        "📊 Comparación con Otros Métodos",
        "📖 Referencias Científicas",
        "🎓 Interpretación de Resultados"
    ])
    
    with theory_tab1:
        st.markdown("""
        #### 🧠 ¿Qué es Top2Vec?
        
        **Top2Vec** (Topic-to-Vector) es un método automático de descubrimiento de tópicos que utiliza 
        representaciones vectoriales densas (embeddings) de documentos y palabras.
        
        ---
        
        ##### 🎯 Objetivo Principal
        
        Identificar automáticamente **tópicos semánticamente coherentes** en colecciones grandes de documentos 
        sin necesidad de:
        - Especificar el número de tópicos *a priori*
        - Preprocesamiento intensivo (lematización, stemming)
        - Diccionarios o vocabularios predefinidos
        
        ---
        
        ##### 🔑 Conceptos Clave
        
        **1. Embeddings de Documentos**
        - Cada documento se representa como un vector denso en espacio de alta dimensión (típicamente 300 dims)
        - Documentos similares tienen vectores cercanos
        - Capturan significado semántico, no solo co-ocurrencia de palabras
        
        **2. Embeddings de Palabras**
        - Cada palabra tiene su propio vector
        - Palabras con significados similares están cerca en el espacio vectorial
        - Ejemplo: "banco", "entidad", "financiera" estarán cercanas
        
        **3. Clustering Automático**
        - Los documentos se agrupan automáticamente por similitud semántica
        - Cada cluster = un tópico
        - No necesitas decir cuántos tópicos quieres
        
        **4. Vectores de Tópicos**
        - Cada tópico tiene un centroide (promedio de documentos del cluster)
        - Las palabras más cercanas al centroide son las "palabras clave" del tópico
        
        ---
        
        ##### 💡 Diferencia Clave vs Métodos Clásicos
        
        | Aspecto | Top2Vec | LDA (Clásico) |
        |---------|---------|---------------|
        | **Representación** | Vectores densos (embeddings) | Bolsa de palabras (sparse) |
        | **Semántica** | ✅ Captura significado | ❌ Solo co-ocurrencia |
        | **Núm. tópicos** | ✅ Automático | ❌ Debes especificarlo |
        | **Preprocesamiento** | ⚠️ Mínimo | ⚠️ Intensivo |
        | **Textos cortos** | ✅ Funciona bien | ❌ Problemas |
        
        ---
        
        ##### 🎓 Base Teórica
        
        Top2Vec se fundamenta en tres áreas de NLP moderno:
        
        1. **Word Embeddings (Word2Vec, 2013)**
           - Mikolov et al.: Representaciones vectoriales de palabras
           - Base: "palabras en contextos similares tienen significados similares"
        
        2. **Document Embeddings (Doc2Vec, 2014)**
           - Le & Mikolov: Extensión de Word2Vec para documentos completos
           - Cada documento = vector en mismo espacio que palabras
        
        3. **Density-Based Clustering (HDBSCAN, 2015)**
           - Campello et al.: Clustering jerárquico basado en densidad
           - Detecta automáticamente número de clusters
           - Robusto a ruido y outliers
        
        ---
        
        ##### 📐 Intuición Geométrica
        
        Imagina un espacio 3D donde:
        - Cada punto = un documento
        - Documentos sobre "inflación" están en una región
        - Documentos sobre "empleo" en otra región
        - Documentos sobre "política monetaria" en otra
        
        Top2Vec:
        1. Encuentra estas regiones densas (clusters)
        2. Calcula el "centro" de cada región
        3. Encuentra las palabras más cercanas a cada centro
        4. ¡Esas palabras definen el tópico!
        """)
        
        # Diagrama conceptual (texto ASCII)
        st.markdown("""
        **Diagrama Conceptual:**
        ```
        Espacio de Embeddings (simplificado en 2D):
        
                Tópico 1: "Inflación"
                    ●●●●●
                   ●  ⊗  ●  ← Centroide
                    ●●●●●
                    
        Tópico 2: "Empleo"           Tópico 3: "BCE"
           ●●●                          ●●●●
          ●  ⊗ ●                        ● ⊗ ●
           ●●●                          ●●●●
        
        ● = Documento
        ⊗ = Centroide del tópico
        
        Palabras cercanas al centroide = Palabras clave del tópico
        ```
        """)
    
    with theory_tab2:
        st.markdown("""
        #### ⚙️ Cómo Funciona Top2Vec - Pipeline Completo
        
        Top2Vec ejecuta 5 pasos principales:
        
        ---
        
        ##### **PASO 1: Crear Embeddings de Documentos** 📝
        
        **Input**: Texto crudo de documentos
        
        **Proceso**:
        - Tokenización básica (separar palabras)
        - Entrenar modelo Doc2Vec o usar embeddings precalculados
        - Cada documento → vector de 300 dimensiones
        
        **Output**: Matriz de documentos (N × 300)
        - N = número de documentos
        - 300 = dimensiones del embedding
        
        **En esta app**: Usamos embeddings **precalculados** para ahorrar 2-3 horas
        
        ```python
        # Conceptualmente:
        doc1 = "El BCE sube los tipos de interés"
        embedding1 = [0.23, -0.45, 0.12, ..., 0.67]  # 300 valores
        
        doc2 = "El BCE mantiene política monetaria"
        embedding2 = [0.21, -0.43, 0.15, ..., 0.65]  # Similar a doc1
        
        doc3 = "El desempleo juvenil aumenta"
        embedding3 = [-0.55, 0.32, -0.78, ..., 0.12]  # Diferente
        ```
        
        ---
        
        ##### **PASO 2: Reducción de Dimensionalidad (UMAP)** 🔻
        
        **Problema**: 300 dimensiones son demasiadas para clustering eficiente
        
        **Solución**: UMAP (Uniform Manifold Approximation and Projection)
        
        **Proceso**:
        - Reduce de 300D → 5D (típicamente)
        - Preserva estructura local y global
        - Mantiene relaciones de similitud
        
        **Parámetros clave**:
        - `n_neighbors`: Cuántos vecinos considerar
          - Mayor = estructura más global
          - Menor = estructura más local
        - `n_components`: Dimensiones finales (típicamente 5)
        - `metric`: Distancia a usar (típicamente 'cosine')
        
        **Output**: Matriz reducida (N × 5)
        
        ```python
        # Antes (300D):
        doc1_high = [0.23, -0.45, 0.12, ..., 0.67]  # 300 valores
        
        # Después (5D):
        doc1_low = [1.2, -0.5, 3.4, 0.8, -2.1]  # 5 valores
        ```
        
        **¿Por qué UMAP y no PCA?**
        - ✅ UMAP preserva mejor estructura no-lineal
        - ✅ Mejor para visualización
        - ✅ Mantiene clusters locales
        - ❌ PCA solo captura varianza lineal
        
        ---
        
        ##### **PASO 3: Clustering con HDBSCAN** 🎯
        
        **Objetivo**: Agrupar documentos similares automáticamente
        
        **Algoritmo**: HDBSCAN (Hierarchical Density-Based Spatial Clustering)
        
        **¿Cómo funciona?**
        1. Estima densidad local de puntos
        2. Identifica regiones de alta densidad
        3. Agrupa puntos en esas regiones
        4. Puntos en regiones de baja densidad = ruido (outliers)
        
        **Parámetros clave**:
        - `min_cluster_size`: Tamaño mínimo de un cluster válido
          - Mayor = menos tópicos, más generales
          - Menor = más tópicos, más específicos
        - `min_samples`: Cuán conservador ser con outliers
        
        **Output**: Etiquetas de cluster para cada documento
        ```python
        doc1 → Tópico 0 (Política monetaria)
        doc2 → Tópico 0 (Política monetaria)
        doc3 → Tópico 5 (Empleo)
        doc4 → -1 (Ruido/Outlier)
        ```
        
        **Ventaja vs K-Means**:
        - ✅ Detecta automáticamente número de clusters
        - ✅ Maneja clusters de formas irregulares
        - ✅ Identifica outliers
        - ✅ No asume clusters esféricos
        
        ---
        
        ##### **PASO 4: Calcular Vectores de Tópicos** 📊
        
        **Para cada cluster/tópico**:
        
        1. Tomar todos los embeddings de documentos del cluster
        2. Calcular el centroide (promedio)
        
        ```python
        # Tópico 0 tiene 150 documentos
        docs_topic0 = [embedding1, embedding2, ..., embedding150]
        
        # Centroide = promedio
        topic_vector0 = mean(docs_topic0)
        ```
        
        **Este vector representa el "tema central" del tópico**
        
        ---
        
        ##### **PASO 5: Encontrar Palabras del Tópico** 🔤
        
        **Objetivo**: Identificar palabras que mejor describen cada tópico
        
        **Proceso**:
        1. Cargar embeddings de palabras (vocabulario)
        2. Para cada tópico, calcular similitud coseno entre:
           - Vector del tópico
           - Cada palabra del vocabulario
        3. Ordenar palabras por similitud
        4. Top N palabras = palabras clave del tópico
        
        ```python
        # Vector del tópico 0
        topic0_vector = [0.22, -0.44, 0.13, ..., 0.66]
        
        # Palabras del vocabulario
        word_vectors = {
            "inflación": [0.21, -0.43, 0.12, ..., 0.65],
            "tipos": [0.23, -0.45, 0.14, ..., 0.67],
            "interés": [0.20, -0.42, 0.11, ..., 0.64],
            ...
        }
        
        # Calcular similitudes
        similitudes = {
            "inflación": cosine_similarity(topic0_vector, word_vectors["inflación"]),
            "tipos": cosine_similarity(topic0_vector, word_vectors["tipos"]),
            ...
        }
        
        # Top 10 palabras
        top_words = ["inflación", "tipos", "interés", "precios", "IPC", ...]
        ```
        
        ---
        
        ##### **🔄 Pipeline Completo Resumido**
        
        ```
        1. DOCUMENTOS CRUDOS
           ↓
        2. DOC2VEC → EMBEDDINGS (N × 300)
           ↓
        3. UMAP → REDUCCIÓN (N × 5)
           ↓
        4. HDBSCAN → CLUSTERS (etiquetas)
           ↓
        5. CENTROIDES → VECTORES DE TÓPICOS
           ↓
        6. SIMILITUD COSENO → PALABRAS CLAVE
           ↓
        7. TÓPICOS FINALES ✅
        ```
        
        ---
        
        ##### ⏱️ Tiempo de Cada Paso (50K documentos)
        
        | Paso | Tiempo | Notas |
        |------|--------|-------|
        | 1. Doc2Vec | 2-3 horas | **Precalculado en esta app** |
        | 2. UMAP | 5-10 min | Depende de n_neighbors |
        | 3. HDBSCAN | 3-5 min | Depende de min_cluster_size |
        | 4. Centroides | <1 min | Cálculo simple |
        | 5. Palabras | 1-2 min | Búsqueda de similitud |
        | **Total** | **~15-20 min** | **Sin Doc2Vec** |
        
        """)
    
    with theory_tab3:
        st.markdown("""
        #### 📊 Comparación con Otros Métodos de Topic Modeling
        
        ---
        
        ##### 🆚 Top2Vec vs LDA (Latent Dirichlet Allocation)
        
        | Característica | Top2Vec | LDA |
        |----------------|---------|-----|
        | **Año** | 2020 | 2003 |
        | **Representación** | Embeddings densos (Doc2Vec) | Bolsa de palabras (sparse) |
        | **Semántica** | ✅ Captura significado contextual | ❌ Solo co-ocurrencia |
        | **Núm. tópicos** | ✅ Automático (HDBSCAN) | ❌ Debes especificar K |
        | **Preprocesamiento** | ⚠️ Mínimo (tokenización) | ⚠️ Intensivo (stopwords, lemma, stem) |
        | **Textos cortos** | ✅ Funciona bien | ❌ Problemas (poca co-ocurrencia) |
        | **Interpretabilidad** | ✅ Palabras por similitud vectorial | ✅ Probabilidades claras |
        | **Velocidad entrenamiento** | ⚠️ Medio (si Doc2Vec ya existe) | ✅ Rápido |
        | **Escalabilidad** | ⚠️ Medio (UMAP puede ser lento) | ✅ Buena (Online LDA) |
        | **Outliers** | ✅ Detecta y maneja | ❌ Asigna a algún tópico |
        | **Tópicos overlapping** | ❌ Un doc = un tópico | ✅ Distribución de tópicos |
        
        **¿Cuándo usar Top2Vec?**
        - Corpus con textos cortos (tweets, noticias, reviews)
        - No sabes cuántos tópicos esperar
        - Quieres capturar significado semántico
        - Tienes recursos computacionales razonables
        
        **¿Cuándo usar LDA?**
        - Corpus muy grande (millones de docs)
        - Sabes aproximadamente cuántos tópicos quieres
        - Necesitas interpretabilidad probabilística
        - Quieres actualizar modelo incrementalmente
        
        ---
        
        ##### 🆚 Top2Vec vs BERTopic
        
        | Característica | Top2Vec | BERTopic |
        |----------------|---------|----------|
        | **Año** | 2020 | 2020 |
        | **Embeddings** | Doc2Vec (300D) | BERT/Sentence-BERT (768D) |
        | **Calidad semántica** | ✅ Buena | ✅✅ Excelente |
        | **Clustering** | HDBSCAN | HDBSCAN |
        | **Representación** | Palabras cercanas | c-TF-IDF |
        | **Velocidad** | ✅ Rápido | ⚠️ Más lento (BERT pesado) |
        | **Recursos** | 💻 Moderados | 💻💻 Altos (GPU recomendada) |
        | **Idiomas** | ⚠️ Necesita modelo por idioma | ✅ Multilingüe (BERT multilingüe) |
        | **Actualización temporal** | ⚠️ Re-entrenar | ✅ Mejor soporte |
        
        **¿Cuándo usar Top2Vec?**
        - Recursos limitados (sin GPU)
        - Velocidad es importante
        - Embeddings Doc2Vec son suficientes
        
        **¿Cuándo usar BERTopic?**
        - Máxima calidad semántica
        - Tienes GPU
        - Corpus multilingüe
        - Necesitas dinámicas temporales avanzadas
        
        ---
        
        ##### 🆚 Top2Vec vs NMF (Non-Negative Matrix Factorization)
        
        | Característica | Top2Vec | NMF |
        |----------------|---------|-----|
        | **Representación** | Embeddings densos | TF-IDF sparse |
        | **Semántica** | ✅ Sí | ❌ No |
        | **Núm. tópicos** | ✅ Automático | ❌ Manual |
        | **Interpretabilidad** | ✅ Buena | ✅✅ Excelente |
        | **Velocidad** | ⚠️ Medio | ✅ Rápido |
        | **Tópicos disjuntos** | ✅ Sí | ⚠️ Parcial |
        
        ---
        
        ##### 📈 Comparación Visual de Calidad
        
        **Coherencia de Tópicos** (mayor = mejor):
        ```
        BERTopic     ████████████████████ 95%
        Top2Vec      ████████████████░░░░ 85%
        LDA          ███████████░░░░░░░░░ 70%
        NMF          ██████████░░░░░░░░░░ 65%
        ```
        
        **Velocidad** (menor = más rápido):
        ```
        NMF          ████░░░░░░░░░░░░░░░░ Muy rápido
        LDA          ███████░░░░░░░░░░░░░ Rápido
        Top2Vec      ████████████░░░░░░░░ Medio
        BERTopic     ████████████████████ Lento
        ```
        
        **Requerimientos Computacionales**:
        ```
        NMF          💻 Bajo
        LDA          💻 Bajo
        Top2Vec      💻💻 Medio
        BERTopic     💻💻💻 Alto
        ```
        
        ---
        
        ##### 🎯 Resumen: ¿Cuál Elegir?
        
        **Top2Vec es ideal cuando**:
        - ✅ Necesitas descubrir tópicos automáticamente
        - ✅ Corpus tiene textos cortos o medianos
        - ✅ Calidad semántica es importante
        - ✅ Tienes recursos computacionales moderados
        - ✅ No quieres preprocesamiento intensivo
        
        **En nuestro caso (noticias económicas)**:
        - ✅ Textos moderadamente largos
        - ✅ No sabemos cuántos tópicos hay
        - ✅ Queremos capturar significado (BCE = Banco Central Europeo)
        - ✅ Recursos disponibles: CPU estándar, 8-16 GB RAM
        
        → **Top2Vec es la elección correcta** ✅
        """)
    
    with theory_tab4:
        st.markdown("""
        #### 📖 Referencias Científicas y Bibliografía
        
        ---
        
        ##### 📄 Paper Original de Top2Vec
        
        **Título**: *Top2Vec: Distributed Representations of Topics*
        
        **Autor**: Dimo Angelov
        
        **Año**: 2020
        
        **Publicación**: arXiv preprint arXiv:2008.09470
        
        **Abstract**: 
        > "We present Top2Vec, an algorithm for topic modeling and semantic search. 
        > It automatically detects topics present in text and generates jointly 
        > embedded topic, document and word vectors."
        
        **Enlace**: https://arxiv.org/abs/2008.09470
        
        **Cita (BibTeX)**:
        ```bibtex
        @article{angelov2020top2vec,
          title={Top2Vec: Distributed Representations of Topics},
          author={Angelov, Dimo},
          journal={arXiv preprint arXiv:2008.09470},
          year={2020}
        }
        ```
        
        ---
        
        ##### 📚 Fundamentos Teóricos
        
        **1. Word2Vec (2013)**
        
        - **Paper**: *Efficient Estimation of Word Representations in Vector Space*
        - **Autores**: Mikolov, T., Chen, K., Corrado, G., & Dean, J.
        - **Publicación**: ICLR 2013
        - **Enlace**: https://arxiv.org/abs/1301.3781
        - **Contribución**: Embeddings de palabras usando CBOW y Skip-gram
        
        **2. Doc2Vec (2014)**
        
        - **Paper**: *Distributed Representations of Sentences and Documents*
        - **Autores**: Le, Q., & Mikolov, T.
        - **Publicación**: ICML 2014
        - **Enlace**: https://arxiv.org/abs/1405.4053
        - **Contribución**: Extensión de Word2Vec para documentos completos
        
        **3. UMAP (2018)**
        
        - **Paper**: *UMAP: Uniform Manifold Approximation and Projection*
        - **Autores**: McInnes, L., Healy, J., & Melville, J.
        - **Publicación**: arXiv preprint arXiv:1802.03426
        - **Enlace**: https://arxiv.org/abs/1802.03426
        - **Contribución**: Reducción de dimensionalidad preservando estructura topológica
        
        **4. HDBSCAN (2015)**
        
        - **Paper**: *Density-Based Clustering Based on Hierarchical Density Estimates*
        - **Autores**: Campello, R. J., Moulavi, D., & Sander, J.
        - **Publicación**: PAKDD 2013
        - **DOI**: 10.1007/978-3-642-37456-2_14
        - **Contribución**: Clustering jerárquico basado en densidad con detección automática
        
        ---
        
        ##### 📊 Comparaciones con Otros Métodos
        
        **LDA (2003)**
        
        - **Paper**: *Latent Dirichlet Allocation*
        - **Autores**: Blei, D. M., Ng, A. Y., & Jordan, M. I.
        - **Publicación**: JMLR 2003
        - **Enlace**: https://www.jmlr.org/papers/v3/blei03a.html
        
        **BERTopic (2022)**
        
        - **Paper**: *BERTopic: Neural topic modeling with a class-based TF-IDF procedure*
        - **Autor**: Grootendorst, M.
        - **Publicación**: arXiv preprint arXiv:2203.05794
        - **Enlace**: https://arxiv.org/abs/2203.05794
        
        ---
        
        ##### 🔬 Validación y Evaluación
        
        **Métricas de Coherencia**
        
        - **Paper**: *Exploring the Space of Topic Coherence Measures*
        - **Autores**: Röder, M., Both, A., & Hinneburg, A.
        - **Publicación**: WSDM 2015
        - **Contribución**: C_v, C_uci, C_npmi para evaluar calidad de tópicos
        
        ---
        
        ##### 📖 Libros de Referencia
        
        **1. Natural Language Processing with Python**
        - Autores: Bird, S., Klein, E., & Loper, E.
        - Editorial: O'Reilly (2009)
        - Capítulos relevantes: 6 (Clasificación), 7 (Estructura)
        
        **2. Speech and Language Processing**
        - Autores: Jurafsky, D., & Martin, J. H.
        - Editorial: Pearson (3rd ed., 2023)
        - Capítulos: 6 (Vector Semantics), 25 (Topic Models)
        
        **3. Introduction to Information Retrieval**
        - Autores: Manning, C. D., Raghavan, P., & Schütze, H.
        - Editorial: Cambridge (2008)
        - Capítulos: 18 (Matrix decompositions), 19 (Latent Semantic Indexing)
        
        ---
        
        ##### 🌐 Recursos Online
        
        **Documentación Oficial**:
        - Top2Vec GitHub: https://github.com/ddangelov/Top2Vec
        - UMAP Docs: https://umap-learn.readthedocs.io/
        - HDBSCAN Docs: https://hdbscan.readthedocs.io/
        
        **Tutoriales**:
        - Gensim Doc2Vec: https://radimrehurek.com/gensim/models/doc2vec.html
        - UMAP Beginner Tutorial: https://umap-learn.readthedocs.io/en/latest/basic_usage.html
        
        **Datasets Públicos**:
        - 20 Newsgroups: http://qwone.com/~jason/20Newsgroups/
        - Reuters Corpus: https://martin-thoma.com/nlp-reuters/
        
        ---
        
        ##### 📊 Aplicaciones en Economía
        
        **1. Topic Modeling in Economics**
        - Autores: Hansen, S., McMahon, M., & Prat, A.
        - Publicación: AEJ: Macroeconomics (2018)
        - Tema: Comunicación de bancos centrales
        
        **2. Central Bank Communication and Policy Effectiveness**
        - Autores: Ehrmann, M., & Fratzscher, M.
        - Publicación: ECB Working Paper (2007)
        - Tema: Análisis de comunicaciones del BCE
        
        **3. News and Narratives in Financial Systems**
        - Autores: Shiller, R. J.
        - Publicación: American Economic Review (2017)
        - Tema: Narrativas económicas en medios
        """)
    
    with theory_tab5:
        st.markdown("""
        #### 🎓 Interpretación de Resultados
        
        ---
        
        ##### 📊 Entender los Tópicos Encontrados
        
        **Un tópico en Top2Vec NO es**:
        - ❌ Una categoría predefinida
        - ❌ Un tema único y absoluto
        - ❌ Una asignación determinista
        
        **Un tópico en Top2Vec SÍ es**:
        - ✅ Un cluster de documentos semánticamente similares
        - ✅ Una distribución de palabras relacionadas
        - ✅ Una representación emergente del corpus
        
        ---
        
        ##### 🔤 Interpretar Palabras Clave
        
        **Ejemplo de Tópico**:
        ```
        Tópico 5: 
        Palabras: ["inflación", "precios", "IPC", "subida", "tasa", 
                   "consumo", "datos", "interanual", "energía", "subyacente"]
        ```
        
        **¿Cómo interpretar?**
        
        1. **Lee las primeras 5-10 palabras**: Dan la "esencia" del tópico
        2. **Busca coherencia temática**: ¿Hablan del mismo tema?
        3. **Identifica el concepto central**: En este caso → "Inflación y precios"
        4. **Verifica con documentos representativos**: ¿Confirman tu interpretación?
        
        **Señales de un tópico coherente**:
        - ✅ Palabras claramente relacionadas
        - ✅ Campo semántico unificado
        - ✅ Documentos representativos confirman interpretación
        
        **Señales de un tópico problemático**:
        - ⚠️ Palabras muy genéricas ("datos", "según", "puede")
        - ⚠️ Mezcla de temas no relacionados
        - ⚠️ Pocos documentos asignados
        
        ---
        
        ##### 📈 Interpretar el Número de Tópicos
        
        **¿Cuántos tópicos son "buenos"?**
        
        No hay número mágico, depende del corpus:
        
        - **Corpus muy homogéneo** (ej: solo sobre BCE)
          - Espera: 10-30 tópicos
          - Serán sub-temas específicos
        
        - **Corpus diverso** (ej: economía general)
          - Espera: 50-150 tópicos
          - Cubrirán múltiples áreas
        
        **Reglas empíricas**:
        - **10-40 tópicos**: Macro-temas, bueno para overview
        - **40-80 tópicos**: Balance, recomendado
        - **80-150 tópicos**: Temas muy específicos, análisis detallado
        - **>200 tópicos**: Posible sobre-segmentación
        
        ---
        
        ##### 🔍 Analizar Calidad de Tópicos
        
        **Métrica 1: Coherencia de Palabras**
        
        ¿Las palabras del tópico tienen sentido juntas?
        
        **Ejemplo bueno**:
        ```
        ["empleo", "paro", "desempleo", "laboral", "trabajadores"]
        → Alta coherencia ✅
        ```
        
        **Ejemplo malo**:
        ```
        ["banco", "casa", "verde", "datos", "puede"]
        → Baja coherencia ❌
        ```
        
        **Métrica 2: Tamaño del Tópico**
        
        ```
        - <1% del corpus: Posible ruido o muy específico
        - 1-5%: Tópico específico bien definido ✅
        - 5-15%: Tópico importante ✅✅
        - >20%: Posible tópico muy general (revisar)
        ```
        
        **Métrica 3: Documentos Representativos**
        
        Lee los 5-10 documentos más representativos:
        - ¿Todos tratan del mismo tema?
        - ¿La interpretación del tópico es clara?
        - ¿Los documentos confirman las palabras clave?
        
        ---
        
        ##### 📊 Interpretar el Gráfico 3D (UMAP)
        
        **Ejes X, Y, Z**: NO tienen significado interpretable
        - Son dimensiones reducidas abstractas
        - Solo importan las **distancias relativas**
        
        **¿Qué SÍ interpretar?**
        
        - **Clusters bien separados** → Tópicos distintos ✅
        - **Clusters mezclados** → Tópicos relacionados o ambiguos ⚠️
        - **Puntos aislados** → Outliers o documentos únicos
        - **Densidad del cluster** → Coherencia interna del tópico
        
        **Ejemplo**:
        ```
        Si ves:
        - Cluster A (azul) muy separado de cluster B (rojo)
          → Tópicos muy diferentes (ej: "inflación" vs "empleo")
        
        - Cluster C (verde) cerca de cluster D (amarillo)
          → Tópicos relacionados (ej: "BCE" vs "política monetaria")
        ```
        
        ---
        
        ##### 📅 Interpretar Análisis Temporal
        
        **Gráfico de series de tiempo muestra**:
        - Número de documentos por tópico en cada período
        
        **Patrones a identificar**:
        
        **1. Tópicos Emergentes** 📈
        ```
        Línea ascendente constante
        → Tema cada vez más mencionado
        → Ej: "inflación" 2021-2023
        ```
        
        **2. Tópicos Decrecientes** 📉
        ```
        Línea descendente
        → Tema perdiendo relevancia
        → Ej: "QE" después de 2020
        ```
        
        **3. Tópicos Estacionales** 🔄
        ```
        Picos periódicos
        → Eventos recurrentes
        → Ej: "presupuestos" cada otoño
        ```
        
        **4. Eventos Puntuales** 📌
        ```
        Pico abrupto único
        → Crisis o evento específico
        → Ej: "COVID-19" marzo 2020
        ```
        
        ---
        
        ##### ⚠️ Limitaciones y Consideraciones
        
        **1. Tópicos no son categorías absolutas**
        - Un documento puede estar "entre" tópicos
        - Interpretación requiere contexto
        
        **2. Outliers son normales**
        - 5-15% de documentos pueden ser outliers (-1)
        - Son documentos únicos o muy específicos
        - NO significa que el modelo falló
        
        **3. Nomenclatura es subjetiva**
        - Debes **TÚ** interpretar y nombrar tópicos
        - Las palabras clave son guía, no etiquetas absolutas
        
        **4. Reproducibilidad parcial**
        - UMAP tiene componente aleatorio
        - Pequeñas variaciones son normales
        - Tendencias principales deben ser consistentes
        
        **5. Contexto importa**
        - Conocimiento del dominio ayuda a interpretar
        - No confíes ciegamente en las palabras
        - Valida con documentos representativos
        
        ---
        
        ##### 🎯 Checklist de Validación
        
        Para cada tópico, pregúntate:
        
        - [ ] ¿Las palabras clave tienen sentido juntas?
        - [ ] ¿Puedo dar un nombre descriptivo al tópico?
        - [ ] ¿Los documentos representativos confirman mi interpretación?
        - [ ] ¿El tamaño del tópico es razonable (>1% corpus)?
        - [ ] ¿La evolución temporal tiene sentido?
        
        Si 4/5 son ✅ → Tópico válido
        Si <3/5 son ✅ → Revisar o descartar
        """)


def render_quick_start_help():
    """Guía de inicio rápido"""
    st.markdown("### 🚀 Inicio Rápido")
    
    st.markdown("""
    <div class="info-card">
    <strong>¿Primera vez usando la aplicación?</strong><br>
    Sigue estos pasos para empezar a analizar tópicos en menos de 5 minutos.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    #### Flujo de Trabajo en 3 Pasos
    
    1. **🎯 Entrenar Modelo** (15-30 minutos)
       - Ve a la pestaña "🎯 Entrenar Modelo"
       - Selecciona un preset (recomendado: "Análisis General")
       - Click en "🚀 Entrenar Modelo"
       - Espera a que termine (verás una barra de progreso)
    
    2. **📊 Explorar Resultados** (5-10 minutos)
       - Ve a la pestaña "📊 Explorar Resultados"
       - Selecciona el modelo entrenado
       - Explora:
         - Gráfico 3D interactivo de tópicos
         - WordClouds de palabras clave
         - Series temporales
         - Documentos representativos
    
    3. **📥 Descargar Resultados** (1 minuto)
       - En la sección "Exportación de Resultados"
       - Click en "📥 Descargar Resumen Excel"
       - Abre el archivo en Excel
       - ¡Listo para presentar!
    
    ---
    
    #### ⏱️ Tiempos Estimados
    
    | Tarea | Tiempo |
    |-------|--------|
    | Entrenar modelo (Rápido) | 10-15 min |
    | Entrenar modelo (Estándar) | 15-25 min |
    | Entrenar modelo (Detallado) | 30-45 min |
    | Explorar resultados | 5-10 min |
    | Exportar a Excel | 1-2 min |
    
    ---
    
    #### ✅ Checklist de Primera Vez
    
    - [ ] Aplicación iniciada correctamente
    - [ ] Archivos de datos verificados (ver pestaña "📊 Datos y Configuración")
    - [ ] Primer modelo entrenado exitosamente
    - [ ] Resultados explorados visualmente
    - [ ] Excel descargado y abierto
    
    """)
    
    st.success("💡 **Consejo**: Empieza con el preset 'Análisis General' para tu primer modelo.")


def render_data_info_help():
    """Información sobre los datos y configuración"""
    st.markdown("### 📊 Datos y Configuración del Sistema")
    
    # Verificar archivos de datos
    st.markdown("#### 📁 Verificación de Archivos")
    
    data_dir = Path(__file__).parent.parent / "data"
    noticias_file = data_dir / "noticias.csv"
    embeddings_file = data_dir / "embeddings_precalculados.npz"
    
    col1, col2 = st.columns(2)
    
    with col1:
        if noticias_file.exists():
            file_size = noticias_file.stat().st_size / (1024**2)  # MB
            st.success(f"✅ **noticias.csv** encontrado ({file_size:.0f} MB)")
            
            # Leer información del dataset
            try:
                df_sample = pd.read_csv(noticias_file, nrows=1000)
                df_info = pd.read_csv(noticias_file, usecols=['date'])
                
                st.info(f"""
                **Información del Dataset:**
                - 📄 Documentos: ~{len(df_info):,}
                - 📅 Fecha inicial: {df_info['date'].min()}
                - 📅 Fecha final: {df_info['date'].max()}
                - 📋 Columnas: {', '.join(df_sample.columns[:5].tolist())}...
                """)
            except Exception as e:
                st.warning(f"No se pudo leer información detallada: {e}")
        else:
            st.error("❌ **noticias.csv** NO encontrado")
            st.markdown("""
            **Solución:**
            1. Descarga el archivo desde: [ENLACE]
            2. Colócalo en la carpeta `data/`
            3. Reinicia la aplicación
            """)
    
    with col2:
        if embeddings_file.exists():
            file_size = embeddings_file.stat().st_size / (1024**2)  # MB
            st.success(f"✅ **embeddings_precalculados.npz** encontrado ({file_size:.0f} MB)")
            
            try:
                embeddings_data = np.load(embeddings_file)
                st.info(f"""
                **Información de Embeddings:**
                - 🧠 Vectores: {embeddings_data['embeddings'].shape[0]:,}
                - 📏 Dimensiones: {embeddings_data['embeddings'].shape[1]}
                - 💾 Tamaño en memoria: ~{embeddings_data['embeddings'].nbytes / (1024**2):.0f} MB
                """)
            except Exception as e:
                st.warning(f"No se pudo leer información detallada: {e}")
        else:
            st.error("❌ **embeddings_precalculados.npz** NO encontrado")
            st.markdown("""
            **Solución:**
            1. Descarga el archivo desde: [ENLACE]
            2. Colócalo en la carpeta `data/`
            3. Reinicia la aplicación
            """)
    
    st.markdown("---")
    
    # Información sobre el formato esperado
    st.markdown("#### 📝 Formato de Datos Esperado")
    
    st.markdown("""
    **Archivo: noticias.csv**
    
    El archivo CSV debe tener las siguientes columnas:
    
    | Columna | Tipo | Descripción | Requerida |
    |---------|------|-------------|-----------|
    | `body` o `text` | string | Texto completo de la noticia | ✅ Sí |
    | `date` | datetime | Fecha de publicación (YYYY-MM-DD) | ✅ Sí |
    | `title` | string | Título de la noticia | ⚠️ Opcional |
    | `url` | string | URL de la noticia | ⚠️ Opcional |
    | `doc_id` | int/string | Identificador único | ⚠️ Opcional |
    
    **Ejemplo de filas:**
    ```csv
    body,date,title
    "El Banco Central Europeo mantiene los tipos...",2023-01-15,"BCE mantiene tipos"
    "La inflación en la zona euro alcanza...",2023-01-20,"Inflación récord"
    ```
    
    ---
    
    **Archivo: embeddings_precalculados.npz**
    
    Formato NumPy comprimido con:
    - `embeddings`: Matriz de vectores (N × 300)
    - N = número de documentos
    - 300 = dimensiones del embedding Doc2Vec
    
    ⚠️ **Importante**: El número de embeddings debe coincidir con el número de documentos en `noticias.csv`
    """)
    
    st.markdown("---")
    
    # Información del sistema
    st.markdown("#### 💻 Información del Sistema")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        ram_total = psutil.virtual_memory().total / (1024**3)  # GB
        ram_available = psutil.virtual_memory().available / (1024**3)  # GB
        ram_percent = psutil.virtual_memory().percent
        
        st.metric("RAM Total", f"{ram_total:.1f} GB")
        st.metric("RAM Disponible", f"{ram_available:.1f} GB")
        if ram_percent > 80:
            st.warning(f"⚠️ Uso de RAM: {ram_percent:.0f}%")
        else:
            st.info(f"Uso de RAM: {ram_percent:.0f}%")
    
    with col2:
        cpu_count = psutil.cpu_count()
        cpu_percent = psutil.cpu_percent(interval=1)
        
        st.metric("CPUs", cpu_count)
        st.metric("Uso CPU", f"{cpu_percent:.1f}%")
    
    with col3:
        disk = psutil.disk_usage('.')
        disk_free = disk.free / (1024**3)  # GB
        
        st.metric("Espacio Disponible", f"{disk_free:.1f} GB")
    
    st.markdown("""
    **Requisitos Recomendados:**
    - 💾 RAM: 16 GB (mínimo 8 GB)
    - 🖥️ CPU: 4 núcleos o más
    - 📀 Disco: 10 GB libres
    """)


def render_usage_help():
    """Guía de uso detallada"""
    st.markdown("### 🎯 Cómo Usar la Aplicación")
    
    usage_subtab1, usage_subtab2, usage_subtab3 = st.tabs([
        "Entrenar Modelos",
        "Explorar Resultados",
        "Casos de Uso"
    ])
    
    with usage_subtab1:
        st.markdown("""
        #### 🎯 Entrenar un Modelo Top2Vec
        
        **1. Seleccionar Preset**
        
        Los presets están optimizados para diferentes necesidades:
        
        - **Análisis General (Recomendado)**
          - ⏱️ Tiempo: 15-25 min
          - 📊 Tópicos: 40-80
          - 🎯 Uso: Primer análisis, exploración inicial
        
        - **Temas Emergentes**
          - ⏱️ Tiempo: 10-15 min
          - 📊 Tópicos: 20-40
          - 🎯 Uso: Identificar tendencias rápidamente
        
        - **Macro-Temas**
          - ⏱️ Tiempo: 30-45 min
          - 📊 Tópicos: 80-150
          - 🎯 Uso: Análisis detallado y profundo
        
        - **Personalizado**
          - ⏱️ Tiempo: Variable
          - 📊 Tópicos: Según configuración
          - 🎯 Uso: Usuarios avanzados
        
        ---
        
        **2. Configurar Parámetros (Opcional)**
        
        Si seleccionas "Personalizado", puedes ajustar:
        
        - **min_count**: Frecuencia mínima de palabras (5-50)
          - Más alto = menos ruido, menos tópicos
          - Más bajo = más tópicos, puede incluir ruido
        
        - **umap_n_neighbors**: Vecinos en UMAP (5-50)
          - Más alto = estructura global
          - Más bajo = estructura local
        
        - **hdbscan_min_cluster_size**: Tamaño mínimo de cluster (30-200)
          - Más alto = menos tópicos, más generales
          - Más bajo = más tópicos, más específicos
        
        ---
        
        **3. Iniciar Entrenamiento**
        
        - Click en "🚀 Entrenar Modelo"
        - Verás una barra de progreso
        - **NO cierres la ventana** del navegador
        - Espera a ver el mensaje de éxito
        
        ---
        
        **4. Guardar el Modelo**
        
        - El modelo se guarda automáticamente en `modelos/`
        - Nombre con timestamp: `top2vec_model_YYYYMMDD_HHMMSS.model`
        - También se guarda la configuración usada en JSON
        """)
    
    with usage_subtab2:
        st.markdown("""
        #### 📊 Explorar Resultados
        
        **1. Seleccionar Modelo**
        
        - Usa el dropdown para elegir un modelo entrenado
        - Verás información básica: fecha, tópicos, documentos
        
        ---
        
        **2. Gráfico 3D Interactivo**
        
        - **Rotar**: Click izquierdo + arrastrar
        - **Zoom**: Scroll del mouse
        - **Pan**: Click derecho + arrastrar
        - **Hover**: Ver información de cada punto
        
        Los colores representan diferentes tópicos.
        
        ---
        
        **3. WordClouds de Tópicos**
        
        - Selecciona un tópico del dropdown
        - Verás una nube de palabras:
          - Tamaño = importancia de la palabra
          - Color = categoría (decorativo)
        - Debajo verás las palabras exactas con scores
        
        ---
        
        **4. Análisis Temporal**
        
        - Gráfico de líneas mostrando evolución en el tiempo
        - Selecciona múltiples tópicos para comparar
        - Identifica:
          - 📈 Tópicos emergentes (líneas ascendentes)
          - 📉 Tópicos decrecientes (líneas descendentes)
          - 🔄 Tópicos estacionales (picos periódicos)
        
        ---
        
        **5. Documentos Representativos**
        
        - Ver los documentos más representativos de cada tópico
        - Útil para entender el contexto
        - Incluye fecha y score de similitud
        
        ---
        
        **6. Búsqueda de Documentos**
        
        - Escribe un tema o query
        - Encuentra los documentos más similares
        - Ejemplo: "política monetaria", "inflación", "tipos de interés"
        
        ---
        
        **7. Exportar Resultados**
        
        Tres formatos disponibles:
        
        - **Excel (.xlsx)**: Ideal para presentaciones
          - Hoja 1: Resumen de tópicos
          - Hoja 2: Documentos representativos
        
        - **CSV (.csv)**: Para análisis adicional
          - Compatible con R, Python, Excel
        
        - **Embeddings (.npz)**: Para análisis avanzado
          - Vectores 3D de UMAP
        """)
    
    with usage_subtab3:
        st.markdown("""
        #### 💼 Casos de Uso Prácticos
        
        **1. Análisis de Comunicaciones del BCE**
        
        Objetivo: Identificar temas principales en las últimas 500 comunicaciones
        
        Flujo:
        1. Entrenar modelo con preset "Análisis General"
        2. Identificar top 10 tópicos
        3. Analizar evolución temporal
        4. Exportar a Excel para briefing ejecutivo
        
        Tiempo total: ~30 minutos
        
        ---
        
        **2. Seguimiento de Inflación en Prensa**
        
        Objetivo: Ver cómo ha evolucionado la cobertura de inflación
        
        Flujo:
        1. Entrenar modelo con preset "Temas Emergentes"
        2. Usar búsqueda semántica: "inflación"
        3. Ver análisis temporal del tópico identificado
        4. Comparar con tópicos relacionados ("precios", "IPC")
        
        Tiempo total: ~20 minutos
        
        ---
        
        **3. Preparación de Reporte Mensual**
        
        Objetivo: Reporte mensual de temas emergentes
        
        Flujo:
        1. Entrenar modelo cada mes
        2. Comparar con modelo del mes anterior
        3. Identificar tópicos nuevos o crecientes
        4. Exportar wordclouds para presentación
        
        Tiempo total: ~40 minutos/mes
        
        ---
        
        **4. Investigación sobre Política Monetaria**
        
        Objetivo: Analizar discursos sobre política monetaria 2020-2025
        
        Flujo:
        1. Filtrar dataset por fechas
        2. Entrenar con preset "Macro-Temas"
        3. Analizar evolución de tópicos clave
        4. Exportar documentos representativos para análisis cualitativo
        
        Tiempo total: ~1 hora
        """)


def render_faq_help():
    """Preguntas frecuentes"""
    st.markdown("### ❓ Preguntas Frecuentes")
    
    with st.expander("❓ ¿Qué es Top2Vec y cómo funciona?"):
        st.markdown("""
        **Top2Vec** es un algoritmo de descubrimiento automático de tópicos que:
        
        1. Crea embeddings (representaciones vectoriales) de documentos
        2. Reduce dimensionalidad con UMAP
        3. Agrupa documentos similares con HDBSCAN
        4. Identifica tópicos a partir de los clusters
        
        **Ventajas vs LDA tradicional:**
        - ✅ Detecta automáticamente el número de tópicos
        - ✅ Usa embeddings semánticos (captura significado)
        - ✅ No requiere preprocesamiento intensivo
        - ✅ Mejor con textos cortos y datasets pequeños
        """)
    
    with st.expander("❓ ¿Cuánto tiempo tarda entrenar un modelo?"):
        st.markdown("""
        Depende del preset y del tamaño del dataset:
        
        | Preset | Documentos | Tiempo Estimado |
        |--------|------------|-----------------|
        | Temas Emergentes | 10K-50K | 10-15 min |
        | Análisis General | 10K-50K | 15-25 min |
        | Macro-Temas | 10K-50K | 30-45 min |
        
        **Factores que afectan:**
        - CPU: Más núcleos = más rápido
        - RAM: Más RAM = menos swapping
        - Dataset: Más documentos = más tiempo
        """)
    
    with st.expander("❓ ¿Cuántos tópicos debo esperar?"):
        st.markdown("""
        El número de tópicos se detecta automáticamente, pero típicamente:
        
        - **Temas Emergentes**: 20-40 tópicos
        - **Análisis General**: 40-80 tópicos
        - **Macro-Temas**: 80-150 tópicos
        
        Depende de:
        - Diversidad del corpus
        - Parámetros (min_cluster_size, etc.)
        - Calidad de los embeddings
        
        **¿Muy pocos tópicos?** → Reduce `min_cluster_size`  
        **¿Demasiados tópicos?** → Aumenta `min_cluster_size`
        """)
    
    with st.expander("❓ ¿Puedo usar mis propios datos?"):
        st.markdown("""
        **Sí**, solo necesitas:
        
        1. **Archivo CSV** con columnas:
           - `text` o `body`: Texto de los documentos
           - `date`: Fecha (YYYY-MM-DD)
        
        2. **Embeddings precalculados** (opcional):
           - Si no los tienes, puedes generarlos
           - Ver: `utils/save_embeddings.py`
           - Tarda 2-3 horas para 50K documentos
        
        3. **Colocar archivos** en `data/`:
           - `data/tus_documentos.csv`
           - `data/tus_embeddings.npz`
        
        4. **Modificar** `src/configuracion.py`:
           - Cambiar rutas de archivos
        """)
    
    with st.expander("❓ ¿Los resultados son reproducibles?"):
        st.markdown("""
        **Parcialmente**:
        
        - ✅ **Embeddings**: Sí (si usas los precalculados)
        - ⚠️ **UMAP**: No completamente (tiene aleatoriedad)
        - ⚠️ **HDBSCAN**: Mayormente sí
        
        **Para mayor reproducibilidad:**
        1. Usa `random_state` fijo en configuración
        2. Guarda el modelo entrenado
        3. Documenta la versión de paquetes usados
        
        **Nota**: Pequeñas variaciones son normales y no afectan conclusiones principales.
        """)
    
    with st.expander("❓ ¿Puedo comparar múltiples modelos?"):
        st.markdown("""
        **Sí**, puedes:
        
        1. Entrenar varios modelos con diferentes configuraciones
        2. Cada modelo se guarda con timestamp único
        3. En "Explorar Resultados", selecciona del dropdown
        
        **Comparación manual:**
        - Número de tópicos encontrados
        - Coherencia de wordclouds
        - Distribución temporal
        
        **Próximamente**: Pestaña de comparación automática
        """)
    
    with st.expander("❓ ¿Qué idiomas soporta?"):
        st.markdown("""
        Top2Vec funciona con **cualquier idioma**, pero:
        
        - **Español**: ✅ Totalmente soportado (este dataset)
        - **Inglés**: ✅ Totalmente soportado
        - **Otros**: ⚠️ Depende de los embeddings
        
        **Para usar otro idioma:**
        1. Entrenar embeddings en ese idioma
        2. O usar modelos preentrenados multilingües
        3. Ajustar stopwords si es necesario
        """)


def render_troubleshooting_help():
    """Solución de problemas"""
    st.markdown("### 🔧 Solución de Problemas")
    
    st.markdown("""
    #### ❌ Errores Comunes y Soluciones
    """)
    
    with st.expander("❌ 'FileNotFoundError: noticias.csv'"):
        st.markdown("""
        **Causa**: No se encuentra el archivo de datos
        
        **Solución**:
        1. Verifica que `data/noticias.csv` existe
        2. Descarga el archivo si falta
        3. Verifica permisos de lectura
        4. Reinicia la aplicación
        
        **Verificación rápida**:
        ```python
        import os
        print(os.path.exists('data/noticias.csv'))  # Debe ser True
        ```
        """)
    
    with st.expander("❌ 'MemoryError' durante entrenamiento"):
        st.markdown("""
        **Causa**: RAM insuficiente
        
        **Solución inmediata**:
        1. Cierra otros programas
        2. Usa preset "Temas Emergentes" (consume menos RAM)
        3. Reduce el dataset (usa una muestra)
        
        **Solución a largo plazo**:
        - Aumenta RAM a 16 GB
        - Usa una máquina con más recursos
        - Procesa el dataset en lotes
        """)
    
    with st.expander("❌ El modelo tarda demasiado (>1 hora)"):
        st.markdown("""
        **Causas posibles**:
        - CPU lento (pocos núcleos)
        - Parámetros muy exigentes
        - Dataset muy grande
        
        **Soluciones**:
        1. Usa preset "Temas Emergentes" (más rápido)
        2. Reduce `umap_n_neighbors`
        3. Aumenta `min_cluster_size`
        4. Verifica que no hay otros procesos consumiendo CPU
        
        **Normal**: 15-30 min en CPU moderno (i5/i7)
        """)
    
    with st.expander("❌ 'No topics found' (0 tópicos)"):
        st.markdown("""
        **Causa**: Parámetros muy restrictivos
        
        **Solución**:
        1. Reduce `min_cluster_size` (prueba 30-50)
        2. Reduce `min_count` (prueba 5-10)
        3. Aumenta `umap_n_neighbors`
        4. Verifica que el dataset tiene suficiente diversidad
        
        **Prueba rápida**: Usa preset "Análisis General"
        """)
    
    with st.expander("❌ Demasiados tópicos (>200)"):
        st.markdown("""
        **Causa**: Parámetros muy permisivos
        
        **Solución**:
        1. Aumenta `min_cluster_size` (prueba 100-150)
        2. Aumenta `min_count` (prueba 30-50)
        3. Reduce `umap_n_neighbors`
        
        **Nota**: Tópicos muy específicos pueden ser útiles para análisis detallado.
        """)
    
    with st.expander("❌ La aplicación se congela"):
        st.markdown("""
        **Durante entrenamiento**: Normal, espera pacientemente
        
        **Otros casos**:
        1. Refresca el navegador (F5)
        2. Verifica RAM disponible
        3. Cierra otras pestañas del navegador
        4. Reinicia la aplicación (Ctrl+C en terminal)
        
        **Si persiste**:
        - Revisa logs en la terminal
        - Verifica errores de Python
        - Contacta soporte técnico
        """)
    
    with st.expander("❌ 'Port 8501 already in use'"):
        st.markdown("""
        **Causa**: Ya hay una instancia corriendo
        
        **Solución**:
        1. Ve a http://localhost:8501 (puede que ya esté abierta)
        2. O cierra la terminal anterior
        3. O usa otro puerto:
           ```bash
           streamlit run app.py --server.port 8502
           ```
        """)
    
    with st.expander("❌ Los wordclouds no se ven bien"):
        st.markdown("""
        **Causas posibles**:
        - Navegador no soporta imágenes
        - Error en generación de imagen
        
        **Solución**:
        1. Actualiza el navegador
        2. Prueba en Chrome o Firefox
        3. Verifica que la librería `wordcloud` esté instalada:
           ```bash
           pip install wordcloud
           ```
        """)
    
    st.markdown("---")
    
    st.markdown("""
    #### 📧 Contacto de Soporte
    
    Si ninguna solución funciona:
    
    1. **Revisa la documentación completa**: `MANUAL_USUARIO.md`
    2. **Busca en FAQ técnico**: `src/FAQ.md`
    3. **Abre un issue en GitHub**: [Enlace]
    4. **Contacta al administrador**: [Email]
    
    **Incluye siempre**:
    - Descripción del problema
    - Mensaje de error completo
    - Pasos para reproducir
    - Información del sistema (ver "📊 Datos y Configuración")
    """)


# =============================================================================
# EJECUTAR APLICACIÓN
# =============================================================================

if __name__ == "__main__":
    main()
