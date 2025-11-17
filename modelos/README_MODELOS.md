# 🤖 Carpeta de Modelos

---

## ℹ️ Información General

Esta carpeta se usa para guardar los modelos Top2Vec entrenados.

**NO es necesario descargar nada aquí inicialmente**. Los modelos se generarán automáticamente cuando entrenes tu primer modelo usando la aplicación web.

---

## 📂 Estructura Generada Automáticamente

Después de entrenar modelos, esta carpeta contendrá:

```
modelos/
├── top2vec_model_YYYYMMDD_HHMMSS.model     ← Modelo entrenado
├── experiment_info_YYYYMMDD_HHMMSS.json    ← Configuración usada
└── README_MODELOS.md                       ← Este archivo
```

---

## 📄 Archivos Generados

### 1. Archivos `.model`

**Contienen**:
- Vectores de documentos
- Vectores de palabras
- Clusters de tópicos
- Metadata del modelo

**Tamaño típico**: 200-500 MB (dependiendo del dataset)

**Formato**: Archivo binario de Top2Vec (pickle serializado)

### 2. Archivos `experiment_info_*.json`

**Contienen**:
```json
{
  "timestamp": "2025-11-16T14:30:00",
  "preset": "Estándar",
  "n_topics_found": 63,
  "parameters": {
    "min_count": 30,
    "umap_n_neighbors": 15,
    "umap_n_components": 5,
    "hdbscan_min_cluster_size": 50
  },
  "training_time_seconds": 1243.5,
  "dataset_size": 50000
}
```

**Propósito**: Reproducibilidad y tracking de experimentos

---

## 🚀 Cómo se Generan los Modelos

### Opción 1: Interfaz Web (Recomendado)

1. Ejecuta: `INICIAR_APP.bat`
2. Ve a la pestaña: **"🎯 Entrenar Modelo"**
3. Selecciona un preset o configura parámetros
4. Click en: **"🚀 Entrenar Modelo"**
5. Espera 15-30 minutos
6. El modelo se guarda automáticamente aquí

### Opción 2: Script de Línea de Comandos

```powershell
cd src
python ejecutar_modelo.py
```

El modelo se guardará en `modelos/` con timestamp.

---

## 📊 Gestión de Modelos

### Listar Modelos Disponibles

```powershell
# Ver todos los modelos
Get-ChildItem modelos\*.model | Select-Object Name, Length, LastWriteTime
```

### Eliminar Modelos Antiguos

```powershell
# Eliminar modelos más antiguos de 30 días
Get-ChildItem modelos\*.model | Where-Object {$_.LastWriteTime -lt (Get-Date).AddDays(-30)} | Remove-Item
```

### Renombrar Modelo

```powershell
# Dar nombre descriptivo
Rename-Item modelos\top2vec_model_20251116_143000.model modelos\top2vec_noticias_BCE_completo.model
```

---

## 🔄 Versionado de Modelos

Recomendaciones para nombrar modelos:

| Patrón | Ejemplo | Uso |
|--------|---------|-----|
| **Por fecha** | `top2vec_20251116.model` | Experimentos cronológicos |
| **Por dataset** | `top2vec_noticias_BCE.model` | Diferentes corpus |
| **Por preset** | `top2vec_detallado_v1.model` | Comparar configuraciones |
| **Por versión** | `top2vec_production_v2.model` | Modelos en producción |

---

## 💾 Backup de Modelos

### Exportar a ZIP

```powershell
# Comprimir modelo específico
Compress-Archive -Path modelos\top2vec_model_20251116_143000.model -DestinationPath backup_modelo_20251116.zip
```

### Copiar a Otro Directorio

```powershell
# Backup manual
Copy-Item modelos\*.model -Destination D:\Backups\TopicModels\
```

---

## 🔍 Inspeccionar Modelo

### Opción 1: Interfaz Web

1. Ejecuta: `INICIAR_APP.bat`
2. Ve a: **"📊 Explorar Resultados"**
3. Selecciona el modelo a explorar
4. Visualiza tópicos, wordclouds, etc.

### Opción 2: Script Python

```python
from top2vec import Top2Vec

# Cargar modelo
model = Top2Vec.load("modelos/top2vec_model_20251116_143000.model")

# Información básica
print(f"Número de tópicos: {model.get_num_topics()}")
print(f"Documentos totales: {len(model.document_vectors)}")

# Ver tópicos
topic_words, word_scores, topic_nums = model.get_topics()
for num, words in zip(topic_nums, topic_words):
    print(f"Tópico {num}: {', '.join(words[:5])}")
```

---

## 📈 Comparación de Modelos

Para comparar diferentes modelos entrenados con distintas configuraciones:

1. Entrena varios modelos con diferentes presets
2. Usa `src/analisis_avanzado.py` para comparar
3. Exporta métricas a Excel
4. Selecciona el mejor modelo

**Métricas de comparación**:
- Número de tópicos encontrados
- Coherencia de tópicos
- Cobertura de documentos
- Tiempo de entrenamiento

---

## 🗑️ Limpieza de Espacio

Si te quedas sin espacio en disco:

```powershell
# Ver tamaño total de modelos
$size = (Get-ChildItem modelos\*.model | Measure-Object -Property Length -Sum).Sum / 1MB
Write-Host "Modelos ocupan: $size MB"

# Eliminar todos excepto el más reciente
Get-ChildItem modelos\*.model | Sort-Object LastWriteTime -Descending | Select-Object -Skip 1 | Remove-Item
```

---

## 🔐 Seguridad y Privacidad

⚠️ **Importante**: Los archivos `.model` contienen:
- Embeddings de todos los documentos
- Puede ser posible reconstruir información sensible

**Recomendaciones**:
- NO subir modelos a repositorios públicos
- Encriptar modelos si contienen datos sensibles
- Revisar políticas de privacidad antes de compartir

---

## 🆘 Problemas Comunes

### ❌ "Error al cargar modelo"

**Causas**:
1. Archivo corrupto
2. Versión incompatible de Top2Vec
3. Archivo incompleto (descarga interrumpida)

**Soluciones**:
1. Re-entrenar el modelo
2. Actualizar Top2Vec: `pip install --upgrade top2vec`
3. Verificar integridad del archivo

### ❌ "No hay espacio en disco"

**Solución**:
```powershell
# Eliminar modelos antiguos
Get-ChildItem modelos\*.model | Sort-Object LastWriteTime | Select-Object -First 5 | Remove-Item
```

### ❌ "Modelo tarda mucho en cargar"

**Normal**: Modelos grandes (>500 MB) pueden tardar 30-60 segundos en cargarse.

**Optimización**: Usar SSD en lugar de HDD.

---

## 📚 Recursos Adicionales

- [Documentación Top2Vec](https://github.com/ddangelov/Top2Vec)
- [Tutorial de uso](../src/README_TECNICO.md)
- [FAQ](../src/FAQ.md)

---

**Versión**: 1.0  
**Última actualización**: Noviembre 2025
