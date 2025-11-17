"""
Script de prueba rápida con subset pequeño de datos
Tiempo estimado: 1-2 minutos vs 15+ minutos del dataset completo
"""
import sys
sys.path.insert(0, 'd:/Top2Vec')

import numpy as np
import pandas as pd
from top2vec import Top2Vec
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import strip_tags

def spanish_friendly_tokenizer(document):
    """Tokenizer que preserva tildes y ñ"""
    clean_text = strip_tags(document)
    return simple_preprocess(clean_text, deacc=False)

class PrecomputedEmbeddings:
    """Proveedor de embeddings precomputados"""
    def __init__(self, embeddings, word_vectors, vocab, word_indexes, documents):
        self.embeddings = embeddings
        self.word_vectors = word_vectors
        self.vocab = vocab
        self.word_indexes = word_indexes
        self.documents = documents  # Guardar documentos originales
        self.current_batch_start = 0
        self.doc_map = {doc: i for i, doc in enumerate(documents)}  # Mapeo texto -> índice
    
    def __call__(self, documents_batch):
        """
        Top2Vec pasa documentos tokenizados.
        Necesitamos mapearlos a índices para devolver embeddings correctos.
        """
        batch_size = len(documents_batch)
        print(f"   [DEBUG] __call__ recibió batch_size={batch_size}, current_start={self.current_batch_start}")
        
        # Si batch_size es muy grande (>10000), probablemente es vocab, devolver word_vectors
        if batch_size > 10000:
            print(f"   [DEBUG] Asumiendo que es vocab ({batch_size} items), devolviendo word_vectors")
            return self.word_vectors[:batch_size]
        
        start_idx = self.current_batch_start
        end_idx = min(start_idx + batch_size, len(self.embeddings))
        
        batch_embeddings = self.embeddings[start_idx:end_idx]
        self.current_batch_start = end_idx
        
        print(f"   [DEBUG] Devolviendo embeddings[{start_idx}:{end_idx}], shape={batch_embeddings.shape}")
        
        return batch_embeddings

print("="*60)
print("PRUEBA RÁPIDA DE TOP2VEC")
print("="*60)

# Cargar datos
print("\n1. Cargando datos...")
data = np.load('d:/Top2Vec/data/embeddings/embeddings_todos.npz', allow_pickle=True)

# USAR SOLO 1000 DOCUMENTOS PARA PRUEBA RÁPIDA
SAMPLE_SIZE = 1000
print(f"   Usando solo {SAMPLE_SIZE} documentos (de {len(data['documents'])} totales)")

documents = data['documents'][:SAMPLE_SIZE].tolist()
document_vectors = data['document_vectors'][:SAMPLE_SIZE]
word_vectors = data['word_vectors']
vocab = data['vocab'].tolist()
word_indexes = data['word_indexes'].item()
doc_ids = [str(i) for i in range(SAMPLE_SIZE)]

print(f"   OK Documentos: {len(documents)}")
print(f"   OK Embeddings: {document_vectors.shape}")
print(f"   OK Vocabulario: {len(vocab)} palabras")
print(f"   OK Word vectors: {word_vectors.shape}")

# Crear embedding provider
print("\n2. Configurando embedding provider...")
embedding_provider = PrecomputedEmbeddings(
    document_vectors, word_vectors, vocab, word_indexes, documents
)

# Configuración (misma que la app)
print("\n3. Configurando parámetros...")
umap_args = {
    'n_neighbors': 50,
    'n_components': 5,
    'metric': 'cosine',
    'random_state': 42
}

hdbscan_args = {
    'min_cluster_size': 15,  # Más pequeño para dataset reducido
    'min_samples': 10,       # Más pequeño para dataset reducido
    'metric': 'euclidean',
    'cluster_selection_method': 'eom'
}

print(f"   UMAP: {umap_args}")
print(f"   HDBSCAN: {hdbscan_args}")

# Entrenar
print("\n4. Entrenando Top2Vec...")
print("   (Esto tomará ~1-2 minutos)")

import time
start = time.time()

model = Top2Vec(
    documents=documents,
    embedding_model=embedding_provider,
    document_ids=doc_ids,
    tokenizer=spanish_friendly_tokenizer,
    min_count=5,  # Reducido para dataset pequeño
    umap_args=umap_args,
    hdbscan_args=hdbscan_args,
    topic_merge_delta=0.1,
    use_embedding_model_tokenizer=False,
    verbose=True
)

elapsed = time.time() - start

# Inyectar word_vectors
print("\n5. Inyectando word_vectors...")
model.word_vectors = word_vectors
model.vocab = vocab
model.word_indexes = word_indexes
print(f"   ✅ {len(vocab)} palabras inyectadas")

# Resultados
print("\n" + "="*60)
print("RESULTADOS")
print("="*60)
print(f"\n⏱️  Tiempo de entrenamiento: {elapsed/60:.1f} minutos")
print(f"\n📊 Tópicos encontrados: {model.get_num_topics()}")

topic_sizes, topic_nums = model.get_topic_sizes()
print(f"\n📈 Distribución de documentos por tópico:")
for i, (topic_num, size) in enumerate(zip(topic_nums[:10], topic_sizes[:10])):
    pct = (size / SAMPLE_SIZE) * 100
    print(f"   Tópico {topic_num}: {size:,} docs ({pct:.1f}%)")

# Probar get_topics
print(f"\n☁️  Primeras 10 palabras del Tópico {topic_nums[0]}:")
all_words, all_scores, _ = model.get_topics()
words = all_words[topic_nums[0]][:10]
scores = all_scores[topic_nums[0]][:10]
for word, score in zip(words, scores):
    print(f"   {word:20s} {score:.4f}")

# Verificar coherencia
print(f"\n🔍 Verificación:")
print(f"   ¿Palabras tienen sentido? (deberían ser términos económicos/financieros)")
print(f"   ¿Distribución balanceada? (no todo en tópico 0)")

print("\n" + "="*60)
print("Si los resultados son buenos, usa la misma configuración en la app.")
print("Si no, ajusta hdbscan_args (min_cluster_size, min_samples)")
print("="*60)
