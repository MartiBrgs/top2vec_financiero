# 📊 Top2Vec para Economistas

> **Guía simplificada para ejecutar análisis de tópicos en noticias económicas**  
> No se requiere conocimiento de programación

---

## 🎯 ¿Qué hace este modelo?

**Top2Vec** es un modelo de inteligencia artificial que:
1. Lee automáticamente miles de noticias económicas
2. Identifica los **tópicos principales** (temas recurrentes)
3. Agrupa las noticias similares
4. Te permite buscar y analizar patrones temporales

**Ejemplo**: Si hay muchas noticias sobre "inflación", "tasas de interés" y "banco central" en un período, el modelo las agrupa automáticamente en un tópico.

---

## ⚡ Inicio Rápido (3 pasos)

### Paso 1: Instalar el software necesario

```bash
# Abrir PowerShell y ejecutar:
pip install uv
```

### Paso 2: Ejecutar el modelo

```bash
# Navegar a esta carpeta
cd top2vec_para_economistas

# Ejecutar el script principal
uv run python ejecutar_modelo.py
```

### Paso 3: Ver resultados

Los resultados se guardarán en la carpeta `resultados/`:
- `resumen_topicos.xlsx` - Tabla con todos los tópicos encontrados
- `modelo_top2vec.model` - Modelo entrenado (para análisis posteriores)

---

## 📖 Guía Detallada

### 🗂️ Estructura de Archivos

```
top2vec_para_economistas/
├── 📄 README.md                    ← Estás aquí
├── 🐍 ejecutar_modelo.py          ← Script principal (ejecutar este)
├── 🔧 configuracion.py             ← Parámetros del modelo (modificar aquí)
├── 📊 data/
│   ├── noticias.csv               ← Noticias para analizar (816 MB)
│   └── embeddings_precalculados.npz ← Representaciones vectoriales (precalculadas)
├── 🤖 modelos/
│   └── (aquí se guardarán los modelos entrenados)
└── 📈 resultados/
    └── (aquí se guardarán los resultados)
```

---

## ⚙️ Parámetros del Modelo (Configuración)

El archivo `configuracion.py` contiene los parámetros ajustables. Aquí explicamos cada uno:

### 🔍 Parámetros de Agrupación (HDBSCAN)

| Parámetro | ¿Qué hace? | Valor por defecto | Cuándo cambiarlo |
|-----------|------------|-------------------|------------------|
| **min_cluster_size** | Mínimo de documentos para formar un tópico | 50 | ↑ Aumentar si quieres tópicos más generales<br>↓ Reducir si quieres tópicos más específicos |
| **min_samples** | Densidad mínima para identificar un tópico | 25 | ↑ Aumentar para tópicos más robustos<br>↓ Reducir para capturar tópicos más raros |

**Ejemplo práctico**:
- Si quieres analizar solo **temas muy frecuentes** → `min_cluster_size=100`
- Si quieres capturar **temas emergentes** → `min_cluster_size=30`

### 🗺️ Parámetros de Reducción Dimensional (UMAP)

| Parámetro | ¿Qué hace? | Valor por defecto | Cuándo cambiarlo |
|-----------|------------|-------------------|------------------|
| **n_neighbors** | Cuántos documentos similares considerar | 50 | ↑ Aumentar para capturar estructura global<br>↓ Reducir para estructura local |
| **n_components** | Dimensiones en el espacio reducido | 5 | Rango típico: 2-10 |

**Ejemplo práctico**:
- Para análisis **macro** (temas amplios) → `n_neighbors=100`
- Para análisis **micro** (temas específicos) → `n_neighbors=30`

### 🔗 Parámetros de Fusión de Tópicos

| Parámetro | ¿Qué hace? | Valor por defecto | Cuándo cambiarlo |
|-----------|------------|-------------------|------------------|
| **topic_merge_delta** | Similitud mínima para fusionar tópicos | 0.1 | ↑ Aumentar para fusionar más tópicos<br>↓ Reducir para mantener tópicos separados |

**Ejemplo práctico**:
- Si ves muchos tópicos **muy similares** → `topic_merge_delta=0.15`
- Si quieres **máxima granularidad** → `topic_merge_delta=0.05`

---

## 🎓 Casos de Uso Recomendados

### Caso 1: Análisis General de Noticias
**Objetivo**: Identificar los principales temas en el corpus

```python
# En configuracion.py, usar:
min_cluster_size = 50
min_samples = 25
n_neighbors = 50
topic_merge_delta = 0.1
```

### Caso 2: Búsqueda de Temas Emergentes
**Objetivo**: Capturar tópicos pequeños pero relevantes

```python
# En configuracion.py, usar:
min_cluster_size = 30
min_samples = 15
n_neighbors = 30
topic_merge_delta = 0.08
```

### Caso 3: Análisis de Macro-Temas
**Objetivo**: Solo los tópicos más grandes y generales

```python
# En configuracion.py, usar:
min_cluster_size = 100
min_samples = 50
n_neighbors = 100
topic_merge_delta = 0.15
```

---

## 📊 Interpretación de Resultados

### Archivo: `resumen_topicos.xlsx`

| Columna | Significado |
|---------|-------------|
| **topic_id** | Identificador único del tópico (0, 1, 2...) |
| **num_documentos** | Cantidad de noticias en este tópico |
| **palabras_clave** | Las 10 palabras más representativas del tópico |
| **score_palabra_1...10** | Relevancia de cada palabra (0-1) |

**Cómo leer las palabras clave**:
- Palabras con score > 0.7 → **Muy representativas** del tópico
- Palabras con score 0.5-0.7 → **Moderadamente relevantes**
- Palabras con score < 0.5 → **Contexto adicional**

**Ejemplo**:
```
Topic 0 (1,250 documentos):
- inflación (0.85)
- ipc (0.78)
- banco_central (0.72)
- alza (0.65)
→ Este tópico trata claramente sobre inflación
```

---

## 🔧 Solución de Problemas

### ❌ Error: "No se encuentra el archivo noticias.csv"
**Solución**: Verifica que el archivo `data/noticias.csv` existe

### ❌ Error: "Memoria insuficiente"
**Solución**: 
1. Aumenta `min_cluster_size` a 100
2. Reduce `n_neighbors` a 30

### ❌ Demasiados tópicos pequeños
**Solución**: 
- Aumenta `topic_merge_delta` a 0.15
- Aumenta `min_cluster_size` a 75

### ❌ Muy pocos tópicos
**Solución**: 
- Reduce `min_cluster_size` a 30
- Reduce `topic_merge_delta` a 0.05

---

## 📚 Recursos Adicionales

### ¿Qué es Top2Vec?
Top2Vec es un algoritmo que:
1. Convierte cada noticia en un **vector numérico** (embedding)
2. Agrupa vectores similares usando **HDBSCAN**
3. Identifica el centro de cada grupo como un **tópico**

### Algoritmos utilizados:
- **UMAP**: Reduce las dimensiones preservando relaciones
- **HDBSCAN**: Agrupa documentos similares sin requerir número de clusters
- **Doc2Vec/Embeddings**: Representa textos como vectores

### Papers de referencia:
- Top2Vec: [arXiv:2008.09470](https://arxiv.org/abs/2008.09470)
- UMAP: [arXiv:1802.03426](https://arxiv.org/abs/1802.03426)
- HDBSCAN: [Journal of Statistical Software (2017)](https://joss.theoj.org/papers/10.21105/joss.00205)

---

## ⏱️ Tiempos de Ejecución Estimados

Con los **embeddings precalculados** (ya incluidos):

| Cantidad de Noticias | Tiempo Estimado |
|---------------------|-----------------|
| 10,000 documentos | 2-5 minutos |
| 50,000 documentos | 5-15 minutos |
| 100,000+ documentos | 15-30 minutos |

**Nota**: El 90% del tiempo de cómputo ya fue completado al precalcular los embeddings. Solo falta el agrupamiento (clustering).

---

## 💡 Consejos para Economistas

1. **Comienza con los parámetros por defecto** - Son valores balanceados
2. **Revisa el archivo de resultados** - Identifica patrones
3. **Ajusta parámetros iterativamente** - Según lo que observes
4. **Documenta tus hallazgos** - Anota qué parámetros usaste

### Preguntas de investigación típicas:
- ¿Cuáles son los temas principales en períodos de crisis?
- ¿Cómo evolucionan los tópicos en el tiempo?
- ¿Qué temas están correlacionados con indicadores económicos?

---

## 📞 Contacto y Soporte

Si tienes problemas o preguntas:
1. Revisa la sección "Solución de Problemas" arriba
2. Verifica que los archivos de datos existen
3. Consulta los logs de ejecución en la consola

---

## 📄 Licencia

Este proyecto utiliza Top2Vec bajo licencia BSD-3-Clause.

---

**Última actualización**: Noviembre 2025  
**Versión**: 1.0
