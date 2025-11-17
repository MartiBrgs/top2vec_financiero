"""
EJECUTAR MODELO TOP2VEC
=======================

Script principal para ejecutar el análisis de tópicos en noticias económicas.
Diseñado para ser simple de usar - solo ejecuta este archivo.

Instrucciones:
1. Abre una terminal (PowerShell o CMD)
2. Navega a esta carpeta: cd top2vec_para_economistas
3. Ejecuta: uv run python ejecutar_modelo.py

Los resultados se guardarán en la carpeta 'resultados/'
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime

# Añadir el directorio padre al path para importar top2vec
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from top2vec import Top2Vec
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import strip_tags

# Importar configuración
from configuracion import *

# =============================================================================
# FUNCIONES AUXILIARES
# =============================================================================

def spanish_friendly_tokenizer(document):
    """
    Tokenizer que preserva tildes y ñ para español
    """
    clean_text = strip_tags(document)
    return simple_preprocess(clean_text, deacc=False)


class PrecomputedEmbeddings:
    """
    Clase para proveer embeddings precomputados a Top2Vec
    (No necesitas entender esto - es código interno)
    """
    
    def __init__(self, embeddings_file, csv_file=None):
        print(f"📂 Cargando embeddings desde: {embeddings_file}")
        data = np.load(embeddings_file, allow_pickle=True)
        self.embeddings = data['embeddings']
        self.pub_dates = data['pub_date']
        self.doc_ids = data['doc_id']
        
        print(f"✅ Embeddings cargados:")
        print(f"   • Documentos: {len(self.embeddings):,}")
        print(f"   • Dimensiones: {self.embeddings.shape[1]}")
        
        self.documents = None
        if csv_file and os.path.exists(csv_file):
            print(f"📄 Cargando textos desde: {csv_file}")
            print(f"   ⏳ Este paso puede tomar varios minutos (archivo grande)...")
            df = pd.read_csv(csv_file)
            
            # Verificar que la columna existe
            if COLUMNA_TEXTO not in df.columns:
                raise ValueError(f"❌ La columna '{COLUMNA_TEXTO}' no existe en el CSV. "
                               f"Columnas disponibles: {list(df.columns)}")
            
            self.documents = df[COLUMNA_TEXTO].astype(str).tolist()
            print(f"   ✅ Textos cargados: {len(self.documents):,}")
        
        self.current_batch_start = 0
    
    def __call__(self, documents_batch):
        """Método para que Top2Vec pueda llamar a esta clase"""
        batch_size = len(documents_batch)
        start_idx = self.current_batch_start
        end_idx = min(start_idx + batch_size, len(self.embeddings))
        
        batch_embeddings = self.embeddings[start_idx:end_idx]
        self.current_batch_start = end_idx
        
        return batch_embeddings


def imprimir_banner():
    """Imprime un banner bonito al inicio"""
    print("\n" + "="*70)
    print("  📊 TOP2VEC - ANÁLISIS DE TÓPICOS EN NOTICIAS ECONÓMICAS")
    print("="*70)
    print(f"  🕐 Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70 + "\n")


def imprimir_configuracion():
    """Muestra la configuración que se está usando"""
    print("\n📋 CONFIGURACIÓN ACTUAL:")
    print("-" * 50)
    print(f"  HDBSCAN:")
    for key, value in HDBSCAN_CONFIG.items():
        print(f"    • {key}: {value}")
    print(f"\n  UMAP:")
    for key, value in UMAP_CONFIG.items():
        print(f"    • {key}: {value}")
    print(f"\n  Otros:")
    print(f"    • topic_merge_delta: {TOPIC_MERGE_DELTA}")
    print(f"    • min_count: {MIN_COUNT_PALABRAS}")
    print("-" * 50 + "\n")


def crear_modelo_top2vec():
    """
    Función principal que crea y entrena el modelo Top2Vec
    """
    
    # Validar que los archivos existen
    if not os.path.exists(ARCHIVO_EMBEDDINGS):
        raise FileNotFoundError(f"❌ No se encuentra el archivo: {ARCHIVO_EMBEDDINGS}")
    
    if not os.path.exists(ARCHIVO_NOTICIAS):
        raise FileNotFoundError(f"❌ No se encuentra el archivo: {ARCHIVO_NOTICIAS}")
    
    # Cargar embeddings y textos
    print("\n🔄 PASO 1: Cargando datos...")
    print("-" * 50)
    embedding_provider = PrecomputedEmbeddings(ARCHIVO_EMBEDDINGS, ARCHIVO_NOTICIAS)
    
    # Preparar documentos
    if embedding_provider.documents:
        documents = embedding_provider.documents
        print(f"✅ Usando {len(documents):,} documentos con texto completo")
    else:
        documents = [f"Document {i}" for i in range(len(embedding_provider.embeddings))]
        print(f"⚠️  Usando {len(documents):,} documentos placeholder (sin texto)")
    
    # Preparar IDs
    document_ids = [str(doc_id) for doc_id in embedding_provider.doc_ids.tolist()]
    print(f"✅ {len(document_ids):,} IDs de documentos preparados")
    
    # Entrenar modelo
    print("\n🚀 PASO 2: Entrenando modelo Top2Vec...")
    print("-" * 50)
    print("⏳ Este proceso puede tomar 15-30 minutos dependiendo del tamaño...")
    print("   (Los embeddings ya están calculados, solo falta el clustering)")
    print()
    
    try:
        model = Top2Vec(
            documents=documents,
            embedding_model=embedding_provider,
            document_ids=document_ids,
            tokenizer=spanish_friendly_tokenizer if USE_SPANISH_TOKENIZER else None,
            min_count=MIN_COUNT_PALABRAS,
            umap_args=UMAP_CONFIG,
            hdbscan_args=HDBSCAN_CONFIG,
            topic_merge_delta=TOPIC_MERGE_DELTA,
            use_embedding_model_tokenizer=USE_EMBEDDING_MODEL_TOKENIZER,
            verbose=VERBOSE
        )
        
        print(f"\n✅ MODELO ENTRENADO EXITOSAMENTE!")
        print("=" * 50)
        print(f"  📊 Tópicos encontrados: {model.get_num_topics()}")
        print(f"  📄 Documentos procesados: {len(documents):,}")
        print("=" * 50)
        
        return model, embedding_provider
        
    except Exception as e:
        print(f"\n❌ ERROR durante el entrenamiento:")
        print(f"   {str(e)}")
        print("\n💡 Sugerencias:")
        print("   • Verifica que tienes suficiente memoria RAM")
        print("   • Intenta aumentar min_cluster_size en configuracion.py")
        print("   • Revisa que los archivos de datos estén completos")
        raise


def exportar_resultados(model):
    """
    Exporta los resultados del modelo a archivos fáciles de leer
    """
    print("\n💾 PASO 3: Exportando resultados...")
    print("-" * 50)
    
    # Crear carpeta de resultados si no existe
    os.makedirs(CARPETA_RESULTADOS, exist_ok=True)
    
    # Obtener información de los tópicos
    num_topics = model.get_num_topics()
    topic_sizes, topic_nums = model.get_topic_sizes()
    
    # Crear DataFrame con resumen de tópicos
    resultados = []
    
    for topic_num in topic_nums:
        # Obtener palabras y scores del tópico
        words, word_scores, _ = model.get_topics(topic_nums=[topic_num])
        
        # Tomar solo las N palabras más relevantes
        top_words = words[0][:NUM_PALABRAS_POR_TOPICO]
        top_scores = word_scores[0][:NUM_PALABRAS_POR_TOPICO]
        
        # Crear fila para este tópico
        fila = {
            'topic_id': topic_num,
            'num_documentos': topic_sizes[topic_nums.tolist().index(topic_num)],
            'palabras_clave': ', '.join(top_words),
        }
        
        # Agregar cada palabra y su score como columnas separadas
        for i, (word, score) in enumerate(zip(top_words, top_scores), 1):
            fila[f'palabra_{i}'] = word
            fila[f'score_palabra_{i}'] = round(score, 4)
        
        resultados.append(fila)
    
    # Convertir a DataFrame
    df_resultados = pd.DataFrame(resultados)
    
    # Ordenar por número de documentos (tópicos más grandes primero)
    df_resultados = df_resultados.sort_values('num_documentos', ascending=False)
    
    # Exportar a Excel
    if EXPORTAR_EXCEL:
        archivo_excel = os.path.join(CARPETA_RESULTADOS, 'resumen_topicos.xlsx')
        df_resultados.to_excel(archivo_excel, index=False)
        print(f"✅ Resumen exportado a: {archivo_excel}")
    
    # También exportar a CSV (más liviano)
    archivo_csv = os.path.join(CARPETA_RESULTADOS, 'resumen_topicos.csv')
    df_resultados.to_csv(archivo_csv, index=False)
    print(f"✅ Resumen exportado a: {archivo_csv}")
    
    # Crear un archivo de texto con resumen legible
    archivo_txt = os.path.join(CARPETA_RESULTADOS, 'resumen_topicos.txt')
    with open(archivo_txt, 'w', encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write("  RESUMEN DE TÓPICOS - TOP2VEC\n")
        f.write(f"  Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"Total de tópicos encontrados: {num_topics}\n")
        f.write(f"Total de documentos clasificados: {sum(topic_sizes):,}\n\n")
        f.write("=" * 70 + "\n\n")
        
        for _, row in df_resultados.iterrows():
            f.write(f"TÓPICO {row['topic_id']} ({row['num_documentos']:,} documentos)\n")
            f.write("-" * 70 + "\n")
            f.write("Palabras clave (con relevancia):\n")
            for i in range(1, NUM_PALABRAS_POR_TOPICO + 1):
                if f'palabra_{i}' in row:
                    palabra = row[f'palabra_{i}']
                    score = row[f'score_palabra_{i}']
                    f.write(f"  {i}. {palabra:<20} (relevancia: {score:.3f})\n")
            f.write("\n" + "=" * 70 + "\n\n")
    
    print(f"✅ Resumen legible exportado a: {archivo_txt}")
    
    # Crear un resumen estadístico
    print(f"\n📊 ESTADÍSTICAS:")
    print(f"   • Tópicos totales: {num_topics}")
    print(f"   • Documentos clasificados: {sum(topic_sizes):,}")
    print(f"   • Promedio docs/tópico: {sum(topic_sizes) / num_topics:.1f}")
    print(f"   • Tópico más grande: {max(topic_sizes):,} documentos")
    print(f"   • Tópico más pequeño: {min(topic_sizes):,} documentos")
    
    return df_resultados


def guardar_modelo(model):
    """Guarda el modelo entrenado para uso futuro"""
    if GUARDAR_MODELO:
        print(f"\n💾 PASO 4: Guardando modelo...")
        print("-" * 50)
        
        os.makedirs(CARPETA_MODELOS, exist_ok=True)
        ruta_modelo = os.path.join(CARPETA_MODELOS, NOMBRE_MODELO)
        
        model.save(ruta_modelo)
        print(f"✅ Modelo guardado en: {ruta_modelo}")
        print(f"   Podrás reutilizar este modelo sin re-entrenar")


def imprimir_resumen_final():
    """Imprime un resumen final al completar"""
    print("\n" + "=" * 70)
    print("  ✅ PROCESO COMPLETADO EXITOSAMENTE")
    print("=" * 70)
    print(f"  🕐 Finalizado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    print(f"\n📂 Revisa los resultados en la carpeta: {CARPETA_RESULTADOS}/")
    print("   • resumen_topicos.xlsx - Tabla completa en Excel")
    print("   • resumen_topicos.csv - Tabla en formato CSV")
    print("   • resumen_topicos.txt - Resumen legible en texto")
    
    if GUARDAR_MODELO:
        print(f"\n🤖 Modelo guardado en: {CARPETA_MODELOS}/{NOMBRE_MODELO}")
    
    print("\n💡 Próximos pasos:")
    print("   1. Abre el archivo Excel para ver los tópicos")
    print("   2. Si quieres ajustar parámetros, edita configuracion.py")
    print("   3. Vuelve a ejecutar este script para probar nuevas configuraciones")
    print("\n")


# =============================================================================
# FUNCIÓN PRINCIPAL
# =============================================================================

def main():
    """
    Función principal que ejecuta todo el proceso
    """
    try:
        # Banner inicial
        imprimir_banner()
        
        # Mostrar configuración
        imprimir_configuracion()
        
        # Crear y entrenar modelo
        model, embedding_provider = crear_modelo_top2vec()
        
        # Exportar resultados
        df_resultados = exportar_resultados(model)
        
        # Guardar modelo
        guardar_modelo(model)
        
        # Resumen final
        imprimir_resumen_final()
        
        return model, df_resultados
        
    except Exception as e:
        print("\n" + "=" * 70)
        print("  ❌ ERROR EN LA EJECUCIÓN")
        print("=" * 70)
        print(f"\n{str(e)}\n")
        print("💡 Revisa la sección 'Solución de Problemas' en README.md")
        print("=" * 70 + "\n")
        raise


# =============================================================================
# PUNTO DE ENTRADA
# =============================================================================

if __name__ == "__main__":
    model, resultados = main()