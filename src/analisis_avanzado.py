"""
ANÁLISIS AVANZADO - EJEMPLOS DE USO
====================================

Este archivo contiene ejemplos de cómo usar el modelo Top2Vec ya entrenado
para hacer análisis adicionales (después de ejecutar ejecutar_modelo.py)

Para economistas que quieran explorar más allá del resumen básico.
"""

import pandas as pd
from top2vec import Top2Vec

# =============================================================================
# CARGAR MODELO ENTRENADO
# =============================================================================

print("Cargando modelo entrenado...")
model = Top2Vec.load("modelos/modelo_top2vec.model")
print(f"✅ Modelo cargado: {model.get_num_topics()} tópicos encontrados\n")

# =============================================================================
# EJEMPLO 1: BUSCAR TÓPICOS POR PALABRAS CLAVE
# =============================================================================
# Útil cuando quieres encontrar tópicos relacionados a un tema específico

print("=" * 70)
print("EJEMPLO 1: Buscar tópicos sobre 'inflación'")
print("=" * 70)

# Buscar tópicos similares a estas palabras
keywords = ["inflación", "ipc", "precios"]
topic_words, word_scores, topic_scores, topic_nums = model.search_topics(
    keywords=keywords, 
    num_topics=5  # Top 5 tópicos más relacionados
)

print(f"\nTop 5 tópicos más relacionados con: {keywords}\n")
for i, (topic_num, score) in enumerate(zip(topic_nums, topic_scores), 1):
    print(f"{i}. Tópico #{topic_num} (similitud: {score:.3f})")
    print(f"   Palabras clave: {', '.join(topic_words[i-1][:5])}")
    print()

# =============================================================================
# EJEMPLO 2: BUSCAR DOCUMENTOS POR TÓPICO
# =============================================================================
# Útil para leer las noticias reales de un tópico específico

print("\n" + "=" * 70)
print("EJEMPLO 2: Ver documentos del tópico de inflación")
print("=" * 70)

# Tomar el primer tópico encontrado arriba
topic_interes = topic_nums[0]

# Obtener los documentos más representativos de ese tópico
documents, document_scores, document_ids = model.search_documents_by_topic(
    topic_num=topic_interes,
    num_docs=3  # Top 3 documentos más representativos
)

print(f"\nTop 3 documentos más representativos del Tópico #{topic_interes}:\n")
for i, (doc, score, doc_id) in enumerate(zip(documents, document_scores, document_ids), 1):
    print(f"{i}. Documento ID: {doc_id} (relevancia: {score:.3f})")
    print(f"   Texto (primeros 200 caracteres):")
    print(f"   {doc[:200]}...")
    print()

# =============================================================================
# EJEMPLO 3: BUSCAR DOCUMENTOS POR PALABRAS CLAVE
# =============================================================================
# Búsqueda semántica: encuentra documentos relacionados aunque no contengan
# las palabras exactas

print("\n" + "=" * 70)
print("EJEMPLO 3: Búsqueda semántica de documentos")
print("=" * 70)

# Buscar documentos sobre política monetaria
keywords_busqueda = ["banco central", "tasa interés", "política monetaria"]
documents, document_scores, document_ids = model.search_documents_by_keywords(
    keywords=keywords_busqueda,
    num_docs=3
)

print(f"\nDocumentos más relacionados con: {keywords_busqueda}\n")
for i, (doc, score, doc_id) in enumerate(zip(documents, document_scores, document_ids), 1):
    print(f"{i}. Documento ID: {doc_id} (similitud: {score:.3f})")
    print(f"   Texto (primeros 200 caracteres):")
    print(f"   {doc[:200]}...")
    print()

# =============================================================================
# EJEMPLO 4: ENCONTRAR PALABRAS SIMILARES
# =============================================================================
# Explora el vocabulario del modelo: encuentra sinónimos o términos relacionados

print("\n" + "=" * 70)
print("EJEMPLO 4: Palabras similares a 'inflación'")
print("=" * 70)

palabras_similares, scores = model.similar_words(
    keywords=["inflación"],
    keywords_neg=[],  # Puedes poner palabras que quieras excluir
    num_words=10
)

print("\nPalabras más similares a 'inflación' según el modelo:\n")
for palabra, score in zip(palabras_similares, scores):
    print(f"  • {palabra:<20} (similitud: {score:.3f})")

# =============================================================================
# EJEMPLO 5: ANÁLISIS TEMPORAL DE TÓPICOS
# =============================================================================
# Requiere que el CSV tenga columna de fechas

print("\n" + "=" * 70)
print("EJEMPLO 5: Distribución temporal de un tópico")
print("=" * 70)

# Cargar datos originales con fechas
try:
    df = pd.read_csv("data/noticias.csv")
    
    # Obtener tópico de cada documento
    topic_nums_all = model.get_documents_topics(doc_ids=None)
    
    # Crear DataFrame con fecha y tópico
    df_temporal = pd.DataFrame({
        'fecha': pd.to_datetime(df['pub_date']),
        'topico': topic_nums_all
    })
    
    # Analizar evolución del tópico de inflación
    topic_inflacion = topic_nums[0]  # Del ejemplo 1
    
    # Filtrar solo ese tópico
    df_topic = df_temporal[df_temporal['topico'] == topic_inflacion].copy()
    
    # Agrupar por mes
    df_topic['mes'] = df_topic['fecha'].dt.to_period('M')
    conteo_mensual = df_topic.groupby('mes').size()
    
    print(f"\nFrecuencia mensual del Tópico #{topic_inflacion} (inflación):")
    print(f"Últimos 12 meses:\n")
    print(conteo_mensual.tail(12))
    
    # Guardar análisis temporal
    conteo_mensual.to_csv("resultados/evolucion_temporal_topico_inflacion.csv")
    print(f"\n✅ Guardado en: resultados/evolucion_temporal_topico_inflacion.csv")
    
except Exception as e:
    print(f"⚠️  No se pudo hacer análisis temporal: {e}")

# =============================================================================
# EJEMPLO 6: EXPORTAR TODOS LOS DOCUMENTOS CON SUS TÓPICOS
# =============================================================================

print("\n" + "=" * 70)
print("EJEMPLO 6: Crear tabla completa documento-tópico")
print("=" * 70)

try:
    # Cargar noticias
    df = pd.read_csv("data/noticias.csv")
    
    # Obtener tópico de cada documento
    all_doc_ids = [str(i) for i in range(len(df))]
    topic_assignments = model.get_documents_topics(doc_ids=all_doc_ids)
    
    # Agregar columna de tópico al DataFrame
    df['topico_asignado'] = topic_assignments
    
    # Obtener palabras clave de cada tópico
    topic_keywords = {}
    for topic_num in range(model.get_num_topics()):
        words, _, _ = model.get_topics(topic_nums=[topic_num])
        topic_keywords[topic_num] = ', '.join(words[0][:5])
    
    # Agregar palabras clave del tópico
    df['topico_keywords'] = df['topico_asignado'].map(topic_keywords)
    
    # Guardar
    output_file = "resultados/noticias_con_topicos.csv"
    df[['doc_id', 'pub_date', 'topico_asignado', 'topico_keywords', 'body']].to_csv(
        output_file, 
        index=False
    )
    
    print(f"✅ Tabla completa guardada en: {output_file}")
    print(f"   Contiene {len(df):,} documentos con sus tópicos asignados")
    
except Exception as e:
    print(f"⚠️  Error: {e}")

# =============================================================================
# RESUMEN FINAL
# =============================================================================

print("\n" + "=" * 70)
print("✅ ANÁLISIS COMPLETADO")
print("=" * 70)
print("\n💡 Puedes modificar este script para hacer tus propios análisis")
print("   Consulta la documentación de Top2Vec para más opciones:")
print("   https://top2vec.readthedocs.io/\n")
