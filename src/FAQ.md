# 📚 PREGUNTAS FRECUENTES (FAQ)

## 🤔 Preguntas Generales

### ¿Qué es Top2Vec?
Top2Vec es un algoritmo de inteligencia artificial que:
- Lee automáticamente documentos (en este caso, noticias)
- Identifica temas recurrentes (tópicos)
- Agrupa documentos similares
- No requiere que le digas cuántos tópicos buscar (los descubre solo)

### ¿Por qué usar embeddings precalculados?
Los embeddings son representaciones numéricas de cada noticia. Calcularlos desde cero:
- ⏱️ Tomaría **varias horas** o días
- 💾 Requiere **mucha memoria RAM** (32GB+)
- 🔥 Necesita una **GPU potente** (opcional pero muy recomendado)

Al tenerlos precalculados, el análisis completo toma solo **15-30 minutos**.

### ¿Qué tan bueno es el modelo?
La calidad depende de:
- ✅ Cantidad de datos (más datos = mejores tópicos)
- ✅ Calidad del preprocesamiento de texto
- ✅ Configuración de parámetros adecuada

Con 100,000+ noticias económicas, los resultados son muy buenos.

---

## ⚙️ Preguntas sobre Parámetros

### ¿Qué parámetro debo cambiar primero?
**Respuesta rápida**: `min_cluster_size` en `configuracion.py`

- Si tienes **muy pocos tópicos** → Reduce a 30
- Si tienes **demasiados tópicos** → Aumenta a 100

### ¿Por qué obtengo muchos tópicos pequeños?
Esto significa que:
- `min_cluster_size` está muy bajo
- Los datos son muy diversos
- Hay mucho ruido en los textos

**Solución**: Aumenta `min_cluster_size` a 75 o 100.

### ¿Por qué obtengo muy pocos tópicos?
Posibles causas:
- `min_cluster_size` está muy alto
- `topic_merge_delta` está muy alto (fusiona demasiado)
- Los datos son muy homogéneos

**Solución**: Reduce `min_cluster_size` a 30 y `topic_merge_delta` a 0.05.

### ¿Qué hace exactamente `n_neighbors`?
Controla cuántos documentos cercanos considera para entender la estructura:
- **Valor alto** (100+): Ve el "panorama general", tópicos amplios
- **Valor bajo** (30-): Se enfoca en detalles locales, tópicos específicos

**Analogía**: Es como usar diferentes niveles de zoom en un mapa.

---

## 💾 Preguntas sobre Datos

### ¿Puedo usar mis propias noticias?
**Sí**, pero necesitarías:
1. Calcular los embeddings (proceso pesado, requiere GPU)
2. Tener el CSV en el mismo formato
3. Actualizar las rutas en `configuracion.py`

**Recomendación**: Empieza con los datos incluidos para aprender.

### ¿Qué columnas necesita el CSV?
Mínimo requerido:
- `body`: El texto completo de la noticia
- `pub_date`: Fecha de publicación (para análisis temporal)
- `doc_id`: Identificador único

### ¿Cuántas noticias necesito como mínimo?
- **Mínimo absoluto**: 1,000 documentos
- **Recomendado**: 10,000+ documentos
- **Óptimo**: 50,000+ documentos

Con menos de 1,000, los resultados no serán confiables.

---

## 🔍 Preguntas sobre Resultados

### ¿Cómo interpreto los scores de las palabras?
El score indica qué tan representativa es una palabra del tópico:
- **0.8-1.0**: Palabra **muy** característica del tópico
- **0.6-0.8**: Palabra **bastante** relevante
- **0.4-0.6**: Palabra **moderadamente** relacionada
- **< 0.4**: Palabra de contexto adicional

### ¿Por qué algunos tópicos parecen similares?
Posibles razones:
- `topic_merge_delta` está muy bajo (no fusiona suficiente)
- Los temas realmente son diferentes pero relacionados
- Necesitas más datos para diferenciarlos mejor

**Solución**: Aumenta `topic_merge_delta` a 0.15 o 0.20.

### ¿Qué significa "documentos clasificados"?
Es la cantidad de documentos que fueron asignados a algún tópico.
Algunos documentos pueden quedar sin clasificar si:
- Son muy diferentes a todo lo demás (outliers)
- No cumplen con `min_cluster_size`

**Esto es normal**: típicamente 80-95% se clasifican.

---

## 🐛 Preguntas sobre Errores

### Error: "No se encuentra el archivo noticias.csv"
**Causa**: No estás en la carpeta correcta.

**Solución**:
```powershell
cd d:\Top2Vec\top2vec_para_economistas
uv run python ejecutar_modelo.py
```

### Error: "Memoria insuficiente" o "MemoryError"
**Causa**: Tu computador no tiene suficiente RAM.

**Soluciones** (en orden):
1. Cierra otros programas
2. Aumenta `min_cluster_size` a 100 en `configuracion.py`
3. Reduce `n_neighbors` a 30
4. Como último recurso, reduce el tamaño del dataset

### Error: "No module named 'top2vec'"
**Causa**: Las dependencias no están instaladas.

**Solución**:
```powershell
pip install -r requirements.txt
```

### El proceso toma demasiado tiempo (>2 horas)
**Posibles causas**:
- Computador lento
- Demasiados documentos
- Parámetros muy exigentes

**Solución**:
- Aumenta `min_cluster_size` (procesa más rápido)
- Reduce `n_neighbors` a 30
- Verifica que no haya otros programas pesados corriendo

---

## 📊 Preguntas sobre Análisis

### ¿Cómo busco tópicos sobre un tema específico?
Usa el script `analisis_avanzado.py` (Ejemplo 1):
```python
keywords = ["inflación", "precios"]
topics = model.search_topics(keywords=keywords, num_topics=5)
```

### ¿Cómo veo las noticias reales de un tópico?
Usa el script `analisis_avanzado.py` (Ejemplo 2):
```python
documents = model.search_documents_by_topic(topic_num=0, num_docs=10)
```

### ¿Puedo analizar la evolución temporal de tópicos?
Sí, el script `analisis_avanzado.py` incluye un ejemplo (Ejemplo 5).
Crea gráficos de frecuencia mensual de cada tópico.

### ¿Cómo exporto todo a Excel para análisis posterior?
El script principal ya genera `resumen_topicos.xlsx`.
Para análisis más detallado, ejecuta `analisis_avanzado.py` (Ejemplo 6).

---

## 🎓 Preguntas Académicas

### ¿Puedo citar este trabajo?
Sí, cita el paper original de Top2Vec:
```
Angelov, D. (2020). Top2Vec: Distributed Representations of Topics. 
arXiv preprint arXiv:2008.09470.
```

### ¿Es reproducible el análisis?
Sí, gracias a:
- `random_state=42` en UMAP (fija la semilla aleatoria)
- Embeddings precalculados (siempre los mismos)
- Configuración documentada

Ejecutar con los mismos parámetros dará los mismos resultados.

### ¿Qué tan robusto es el modelo?
Top2Vec es considerado **muy robusto** porque:
- No requiere especificar número de tópicos
- Usa algoritmos de clustering denso (HDBSCAN)
- Es menos sensible a ruido que LDA o NMF

---

## 🔮 Preguntas Avanzadas

### ¿Puedo usar otros embeddings?
Sí, pero requiere modificar el código y recalcular todo.
Los embeddings actuales son de alta calidad (probablemente de un modelo transformer).

### ¿Puedo integrar esto con otros análisis?
Sí, el script `analisis_avanzado.py` muestra cómo:
- Exportar documentos con tópicos asignados
- Hacer análisis temporal
- Combinar con otros datasets

### ¿Funciona para otros idiomas además de español?
Sí, Top2Vec funciona con cualquier idioma, pero:
- Los embeddings deben ser entrenados en ese idioma
- El tokenizer debe adaptarse (preservar caracteres especiales)

---

## 💡 Consejos Finales

1. **Empieza simple**: Usa configuración por defecto primero
2. **Itera**: Ajusta parámetros según lo que observes
3. **Documenta**: Anota qué configuración usaste para cada experimento
4. **Explora**: Usa `analisis_avanzado.py` para profundizar
5. **Pregunta**: Si algo no funciona, revisa los logs de error

---

**¿Tu pregunta no está aquí?**
Revisa:
- 📖 `README.md` - Documentación completa
- 🚀 `INICIO_RAPIDO.md` - Guía rápida
- 🐍 `analisis_avanzado.py` - Ejemplos de código
