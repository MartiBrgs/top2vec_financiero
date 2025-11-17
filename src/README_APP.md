# 🌐 Aplicación Web Top2Vec

## 🚀 Ejecutar la Aplicación

### Opción 1: Doble click (Windows)
```
Doble click en: iniciar_app.bat
```

### Opción 2: Línea de comandos
```bash
# Desde la carpeta raíz del proyecto (D:\Top2Vec)
.\.venv\Scripts\python.exe -m streamlit run top2vec_para_economistas/app.py

# O desde la carpeta top2vec_para_economistas
cd top2vec_para_economistas
..\.venv\Scripts\python.exe -m streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

---

## ✨ Características

### 🔧 Pestaña: Entrenar Nuevo Modelo

- **Presets predefinidos**: Análisis General, Temas Emergentes, Macro-Temas
- **Configuración avanzada**: Control total sobre parámetros HDBSCAN y UMAP
- **Monitoreo en tiempo real**:
  - Barra de progreso
  - Uso de CPU y memoria
  - Log detallado del proceso
  - Estimación de tiempo
- **Guardado automático**: Modelo + metadata en carpeta `modelos/`

### 📊 Pestaña: Explorar Resultados

- **Carga de modelos**: Usa el recién entrenado o carga modelos anteriores
- **Explorador de tópicos**:
  - WordCloud interactivo para cada tópico
  - Serie temporal de frecuencia de documentos
  - Top 20 palabras clave con scores
  - Documentos representativos
  - Distribución global de tópicos
- **Descargas**:
  - WordCloud como PNG
  - Palabras clave en CSV
  - Serie temporal en CSV
  - Resumen completo en Excel (múltiples hojas)
  - Resumen en CSV

---

## 📁 Estructura de Archivos Generados

```
modelos/
  modelo_20251116_143022/
    ├── modelo.model           # Modelo Top2Vec entrenado
    └── metadata.json          # Configuración y estadísticas
```

---

## 🎯 Flujo de Trabajo Recomendado

1. **Entrenar Modelo**:
   - Ve a la pestaña "Entrenar Nuevo Modelo"
   - Selecciona un preset o personaliza parámetros
   - Click en "Entrenar Modelo"
   - Espera 15-30 minutos (verás progreso en tiempo real)

2. **Explorar Resultados**:
   - Automáticamente se carga el modelo entrenado
   - O selecciona un modelo anterior
   - Navega por los tópicos con el menú desplegable
   - Descarga los resultados que necesites

3. **Análisis**:
   - Revisa wordclouds para entender cada tópico
   - Analiza evolución temporal
   - Exporta todo a Excel para análisis adicional

---

## 💡 Consejos

- ✅ **Primer uso**: Empieza con el preset "Análisis General"
- ✅ **Rendimiento**: Cierra otros programas durante el entrenamiento
- ✅ **Comparación**: Entrena múltiples modelos con diferentes configuraciones
- ✅ **Backup**: Los modelos se guardan automáticamente en `modelos/`

---

## 🔧 Solución de Problemas

### La aplicación no inicia
```bash
# Instalar dependencias
pip install streamlit plotly wordcloud openpyxl psutil
```

### Error de memoria durante entrenamiento
- Aumenta `min_cluster_size` a 100
- Reduce `n_neighbors` a 30
- Cierra otras aplicaciones

### No se ven los modelos guardados
- Verifica que existe la carpeta `modelos/`
- Verifica que los archivos `metadata.json` existen

---

## 📊 Formatos de Exportación

### Excel (Recomendado)
- **Hoja 1**: Resumen de tópicos con palabras y scores
- **Hoja 2**: Series temporales (fecha × tópico)
- **Hoja 3**: Metadata del modelo

### CSV
- Resumen de tópicos
- Serie temporal de cada tópico
- Palabras clave por tópico

### PNG
- WordCloud de cada tópico individual

---

## 🎨 Personalización

Edita `.streamlit/config.toml` para cambiar colores y configuración.

---

**¡Disfruta explorando tus datos!** 🎉
