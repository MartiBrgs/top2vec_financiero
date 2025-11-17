# 📈 Carpeta de Resultados

---

## ℹ️ Información General

Esta carpeta se usa para guardar los resultados exportados desde la aplicación web.

**NO es necesario descargar nada aquí inicialmente**. Los archivos se generarán automáticamente cuando uses la función de exportación en la aplicación.

---

## 📂 Estructura Generada Automáticamente

Después de exportar resultados, esta carpeta contendrá:

```
resultados/
├── resumen_topicos_YYYYMMDD_HHMMSS.xlsx        ← Resumen en Excel
├── documentos_por_topico_YYYYMMDD_HHMMSS.csv   ← Documentos asignados
├── evolucion_temporal_YYYYMMDD_HHMMSS.csv      ← Series temporales
├── embeddings_reducidos_YYYYMMDD_HHMMSS.npz    ← Embeddings UMAP
├── temporal_analysis/                          ← Análisis temporal detallado
│   ├── topic_evolution.csv
│   └── temporal_insights.json
└── README_RESULTADOS.md                        ← Este archivo
```

---

## 📄 Tipos de Archivos Exportados

### 1. `resumen_topicos_*.xlsx` (Excel)

**Contenido**:
- Hoja 1: Resumen de todos los tópicos
  - ID del tópico
  - Top 10 palabras clave
  - Número de documentos
  - Porcentaje del corpus
  
- Hoja 2: Documentos representativos por tópico
  - Tópico
  - Texto del documento
  - Score de similitud

**Uso**: Ideal para presentaciones y reportes

**Tamaño típico**: 2-5 MB

### 2. `documentos_por_topico_*.csv`

**Estructura**:

| Columna | Descripción |
|---------|-------------|
| `doc_id` | ID del documento (índice) |
| `topic` | Tópico asignado |
| `text` | Texto completo |
| `date` | Fecha del documento |
| `score` | Similitud con el tópico |

**Uso**: Análisis detallado, filtrado por tópico

**Tamaño típico**: 50-200 MB (dependiendo del corpus)

### 3. `evolucion_temporal_*.csv`

**Estructura**:

| Columna | Descripción |
|---------|-------------|
| `date` | Fecha (YYYY-MM-DD) |
| `topic_0` | Cantidad de docs en tópico 0 |
| `topic_1` | Cantidad de docs en tópico 1 |
| ... | ... |
| `topic_N` | Cantidad de docs en tópico N |

**Uso**: Gráficos de series de tiempo, análisis de tendencias

**Tamaño típico**: 1-5 MB

### 4. `embeddings_reducidos_*.npz`

**Contenido**:
- Embeddings UMAP 3D de todos los documentos
- Formato NumPy comprimido

**Uso**: Visualizaciones personalizadas, análisis externo

**Tamaño típico**: 10-50 MB

### 5. Carpeta `temporal_analysis/`

**Archivos**:
- `topic_evolution.csv`: Evolución de tópicos en el tiempo
- `temporal_insights.json`: Insights automáticos (tópicos emergentes, decrecientes)

**Uso**: Identificar tendencias, tópicos de moda

---

## 🚀 Cómo se Generan los Resultados

### Desde la Interfaz Web

1. Entrena un modelo (pestaña "🎯 Entrenar Modelo")
2. Ve a la pestaña "📊 Explorar Resultados"
3. Click en los botones de descarga:
   - **"📥 Descargar Resumen Excel"**
   - **"📥 Descargar Datos CSV"**
   - **"📥 Descargar Embeddings"**
4. Los archivos se guardan automáticamente en `resultados/`

### Desde Scripts

```powershell
cd src
python analisis_avanzado.py
```

---

## 📊 Trabajar con los Resultados

### Abrir en Excel

```powershell
# Abrir el Excel más reciente
$latest = Get-ChildItem resultados\resumen_topicos_*.xlsx | Sort-Object LastWriteTime -Descending | Select-Object -First 1
Start-Process $latest.FullName
```

### Importar en Python

```python
import pandas as pd

# Leer Excel
df_topics = pd.read_excel("resultados/resumen_topicos_20251116_143000.xlsx", sheet_name=0)

# Leer CSV de evolución temporal
df_temporal = pd.read_csv("resultados/evolucion_temporal_20251116_143000.csv")

# Leer embeddings
import numpy as np
embeddings = np.load("resultados/embeddings_reducidos_20251116_143000.npz")
umap_coords = embeddings['embeddings_3d']
```

### Importar en R

```r
library(readr)
library(readxl)

# Leer Excel
topics <- read_excel("resultados/resumen_topicos_20251116_143000.xlsx", sheet = 1)

# Leer CSV
temporal <- read_csv("resultados/evolucion_temporal_20251116_143000.csv")
```

---

## 📈 Análisis Comunes

### 1. Identificar Tópicos Principales

```python
import pandas as pd

df = pd.read_excel("resultados/resumen_topicos_*.xlsx")
top_10 = df.nlargest(10, 'num_documentos')
print(top_10[['topic_id', 'palabras_clave', 'num_documentos']])
```

### 2. Gráfico de Evolución Temporal

```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("resultados/evolucion_temporal_*.csv", parse_dates=['date'])
df.set_index('date', inplace=True)

# Plot tópicos principales
top_topics = df.sum().nlargest(5).index
df[top_topics].plot(figsize=(12, 6))
plt.title("Evolución de Tópicos Principales")
plt.xlabel("Fecha")
plt.ylabel("Número de Documentos")
plt.legend(title="Tópico")
plt.show()
```

### 3. Filtrar Documentos por Tópico

```python
import pandas as pd

df = pd.read_csv("resultados/documentos_por_topico_*.csv")

# Documentos del tópico 5
topic_5_docs = df[df['topic'] == 5]
print(f"Documentos en tópico 5: {len(topic_5_docs)}")
print(topic_5_docs[['text', 'date', 'score']].head())
```

---

## 🔄 Versionado de Resultados

Recomendaciones para organizar resultados:

```
resultados/
├── experimento_1/
│   ├── resumen_topicos.xlsx
│   └── evolucion_temporal.csv
├── experimento_2/
│   ├── resumen_topicos.xlsx
│   └── evolucion_temporal.csv
└── produccion/
    └── resumen_topicos_final.xlsx
```

---

## 💾 Backup de Resultados

### Comprimir Resultados

```powershell
# Crear ZIP de todos los resultados
$date = Get-Date -Format "yyyyMMdd"
Compress-Archive -Path resultados\*.xlsx, resultados\*.csv -DestinationPath "backup_resultados_$date.zip"
```

### Copiar a Otro Directorio

```powershell
# Backup a red compartida
Copy-Item resultados\*.xlsx -Destination \\servidor\compartido\TopicModels\
```

---

## 📧 Compartir Resultados

### Enviar por Email

Los archivos Excel son ideales para compartir:
- Tamaño manejable (2-5 MB)
- Fácil de abrir para no-programadores
- Contiene visualizaciones y datos

### Subir a SharePoint/OneDrive

```powershell
# Mover a carpeta sincronizada con OneDrive
Copy-Item resultados\resumen_topicos_*.xlsx -Destination "C:\Users\Usuario\OneDrive\Proyectos\TopicModels\"
```

---

## 🗑️ Limpieza de Espacio

Si acumulas muchos resultados:

```powershell
# Ver tamaño total
$size = (Get-ChildItem resultados\* -Recurse | Measure-Object -Property Length -Sum).Sum / 1MB
Write-Host "Resultados ocupan: $size MB"

# Eliminar archivos más antiguos de 60 días
Get-ChildItem resultados\*.xlsx, resultados\*.csv | 
    Where-Object {$_.LastWriteTime -lt (Get-Date).AddDays(-60)} | 
    Remove-Item

# Conservar solo los 10 más recientes de cada tipo
Get-ChildItem resultados\resumen_topicos_*.xlsx | 
    Sort-Object LastWriteTime -Descending | 
    Select-Object -Skip 10 | 
    Remove-Item
```

---

## 📊 Plantillas de Análisis

### Reporte Ejecutivo en Excel

Crea un archivo `plantilla_reporte.xlsx` con:

1. **Hoja "Resumen"**: KPIs principales
   - Número de tópicos encontrados
   - Tópicos principales (top 10)
   - Cobertura temporal

2. **Hoja "Tópicos"**: Tabla completa de tópicos

3. **Hoja "Evolución"**: Gráficos de líneas temporales

4. **Hoja "Insights"**: Hallazgos clave
   - Tópicos emergentes
   - Tópicos decrecientes
   - Correlaciones

---

## 🔍 Validación de Resultados

### Verificar Integridad

```python
import pandas as pd

# Verificar que todos los documentos están asignados
df = pd.read_csv("resultados/documentos_por_topico_*.csv")
print(f"Total documentos: {len(df)}")
print(f"Documentos con tópico: {df['topic'].notna().sum()}")
print(f"Tópicos únicos: {df['topic'].nunique()}")

# Verificar consistencia temporal
df_temp = pd.read_csv("resultados/evolucion_temporal_*.csv")
total_por_fecha = df_temp.iloc[:, 1:].sum(axis=1)
print(f"Promedio docs por fecha: {total_por_fecha.mean():.0f}")
```

---

## 🆘 Problemas Comunes

### ❌ "Archivo muy grande para abrir en Excel"

**Solución**: Excel tiene límite de ~1 millón de filas
```python
# Dividir CSV en partes más pequeñas
import pandas as pd

df = pd.read_csv("resultados/documentos_por_topico_*.csv")
chunk_size = 500000
for i, chunk in enumerate(np.array_split(df, len(df) // chunk_size + 1)):
    chunk.to_csv(f"resultados/documentos_parte_{i+1}.csv", index=False)
```

### ❌ "Codificación incorrecta de caracteres"

**Solución**: Especificar encoding UTF-8
```python
df = pd.read_csv("archivo.csv", encoding='utf-8')
```

### ❌ "Gráficos no se ven en Excel"

**Solución**: Los gráficos se crean en la aplicación web. Exporta las imágenes:
1. En la app web, click derecho en el gráfico
2. "Save as image"
3. Inserta en Excel manualmente

---

## 📚 Recursos Adicionales

- [Tutorial de análisis con Pandas](https://pandas.pydata.org/docs/getting_started/tutorials.html)
- [Visualización con Plotly](https://plotly.com/python/)
- [FAQ Técnicas](../src/FAQ.md)

---

**Versión**: 1.0  
**Última actualización**: Noviembre 2025
