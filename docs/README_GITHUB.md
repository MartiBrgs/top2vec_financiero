# 🎯 Top2Vec para Economistas

> **Herramienta de análisis de tópicos en noticias económicas usando Top2Vec con interfaz web intuitiva**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 📖 ¿Qué es esto?

Una aplicación web **sin necesidad de programar** que permite a economistas y analistas:

- 🔍 **Descubrir tópicos** automáticamente en noticias económicas
- ☁️ **Visualizar WordClouds** de cada tópico encontrado
- 📊 **Analizar evolución temporal** de los tópicos
- 📥 **Exportar resultados** a Excel/CSV
- 🎯 **Buscar documentos** relacionados con temas específicos

---

## ✨ Características

✅ **Interfaz Visual** - No necesitas saber programar  
✅ **Doble Click** - Archivos `.bat` para instalar y ejecutar  
✅ **Presets Predefinidos** - Configuraciones optimizadas (Rápido/Estándar/Detallado)  
✅ **Gráficos Interactivos** - UMAP 3D, series temporales, wordclouds  
✅ **Embeddings Precalculados** - Ahorra 2-3 horas de procesamiento  
✅ **Exportación Fácil** - Descarga resultados en Excel con un click  

---

## 🚀 Inicio Rápido (3 Pasos)

### 1️⃣ Descargar

```bash
# Opción 1: Con Git
git clone https://github.com/TU_USUARIO/TU_REPOSITORIO.git
cd top2vec_para_economistas

# Opción 2: Descargar ZIP
# Click en "Code" → "Download ZIP" → Descomprimir
```

### 2️⃣ Instalar (Primera vez solamente)

**Doble click en:** `INSTALAR.bat`

Espera 5-10 minutos mientras se instalan las dependencias.

### 3️⃣ Ejecutar

**Doble click en:** `INICIAR_APP.bat`

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

---

## 📋 Requisitos del Sistema

| Componente | Mínimo | Recomendado |
|------------|--------|-------------|
| **SO** | Windows 10 | Windows 10/11 |
| **RAM** | 8 GB | 16 GB |
| **Disco** | 5 GB libres | 10 GB libres |
| **Python** | 3.8+ | 3.12+ |
| **Internet** | Solo instalación | Solo instalación |

---

## 📂 Estructura del Proyecto

```
📂 top2vec_para_economistas/
│
├── 🔧 INSTALAR.bat                    ← Ejecuta primero (solo una vez)
├── ▶️ INICIAR_APP.bat                  ← Ejecuta cada vez que quieras usar
├── 📖 INSTRUCCIONES_PRIMERA_VEZ.md    ← Lee esto primero
├── 📖 MANUAL_USUARIO.md               ← Guía completa (200+ págs)
├── 🎯 EMPEZAR_AQUI.md                 ← Inicio rápido
│
├── 📊 data/                           ← Datos
│   ├── noticias.csv                   ← 816 MB de noticias
│   └── embeddings_precalculados.npz   ← 1 GB de embeddings
│
├── 🤖 modelos/                        ← Modelos entrenados (auto-generado)
├── 📈 resultados/                     ← Exportaciones Excel/CSV
│
└── 💻 src/                            ← Código fuente
    ├── app.py                         ← Aplicación Streamlit principal
    ├── ejecutar_modelo.py             ← Script de entrenamiento
    ├── configuracion.py               ← Parámetros configurables
    └── analisis_avanzado.py           ← Análisis adicionales
```

---

## 🎓 Documentación

| Documento | Audiencia | Contenido |
|-----------|-----------|-----------|
| **[INSTRUCCIONES_PRIMERA_VEZ.md](INSTRUCCIONES_PRIMERA_VEZ.md)** | 👔 No programadores | Guía paso a paso completa |
| **[EMPEZAR_AQUI.md](EMPEZAR_AQUI.md)** | 👔 No programadores | Resumen de 2 minutos |
| **[MANUAL_USUARIO.md](MANUAL_USUARIO.md)** | 👔 Todos | Guía completa con capturas |
| **[README.md](README.md)** | 👔 Todos | Bienvenida y resumen |
| **[src/README_TECNICO.md](src/README_TECNICO.md)** | 💻 Desarrolladores | Documentación técnica |
| **[src/FAQ.md](src/FAQ.md)** | 💻 Desarrolladores | Preguntas técnicas |

---

## 🖥️ Capturas de Pantalla

### Pestaña 1: Entrenar Modelo

![Entrenar Modelo](docs/screenshots/train_tab.png)

- Presets predefinidos (Rápido/Estándar/Detallado)
- Configuración avanzada opcional
- Monitoreo en tiempo real

### Pestaña 2: Explorar Resultados

![Explorar Resultados](docs/screenshots/explore_tab.png)

- Gráfico 3D interactivo UMAP
- WordClouds automáticos
- Series temporales
- Exportación a Excel

---

## 💡 Casos de Uso

### 📰 Análisis de Noticias Económicas

```
Objetivo: Identificar temas principales en noticias del BCE

1. Cargar noticias.csv (incluido)
2. Entrenar modelo con preset "Estándar"
3. Explorar tópicos encontrados
4. Descargar Excel con palabras clave
5. Buscar noticias sobre "inflación"
```

### 📊 Evolución Temporal de Tópicos

```
Objetivo: Ver cómo cambian los temas a lo largo del tiempo

1. Entrenar modelo
2. Ir a "Análisis Temporal"
3. Ver gráficos de series de tiempo
4. Identificar tópicos emergentes
```

### 🔍 Búsqueda Semántica

```
Objetivo: Encontrar documentos similares

1. Entrenar modelo
2. Ir a "Búsqueda de Documentos"
3. Escribir: "política monetaria expansiva"
4. Ver los 10 documentos más relevantes
```

---

## ⚙️ Configuración

### Presets Disponibles

| Preset | Tiempo | Tópicos | Uso Recomendado |
|--------|--------|---------|------------------|
| **Rápido** | 5-10 min | 20-40 | Pruebas iniciales |
| **Estándar** | 15-20 min | 40-80 | Uso general |
| **Detallado** | 30-45 min | 80-150 | Análisis profundo |

### Personalización Avanzada

Edita `src/configuracion.py` para ajustar:

- Número mínimo/máximo de tópicos
- Parámetros de UMAP y HDBSCAN
- Número de palabras por tópico
- Métricas de distancia

---

## 🛠️ Solución de Problemas

### ❌ Error: "Python no encontrado"

**Solución:**
1. Instala Python desde https://www.python.org/
2. **IMPORTANTE**: Marca "Add Python to PATH"
3. Reinicia tu computadora
4. Vuelve a ejecutar `INSTALAR.bat`

### ❌ La aplicación no se abre

**Solución:**
1. Abre manualmente: `http://localhost:8501`
2. Si no funciona, revisa que no esté bloqueado el puerto
3. Lee `MANUAL_USUARIO.md` sección "Solución de Problemas"

### ❌ El modelo tarda mucho

**Solución:**
1. Usa el preset "Rápido" para pruebas
2. Cierra otros programas para liberar RAM
3. Es normal que tarde 15-30 minutos en equipos lentos

---

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas!

1. Fork el proyecto
2. Crea una rama: `git checkout -b feature/nueva-funcionalidad`
3. Commit tus cambios: `git commit -m 'Agrega nueva funcionalidad'`
4. Push a la rama: `git push origin feature/nueva-funcionalidad`
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

---

## 🙏 Créditos

- **Top2Vec**: [ddangelov/Top2Vec](https://github.com/ddangelov/Top2Vec)
- **Streamlit**: Framework para la interfaz web
- **UMAP**: Reducción de dimensionalidad
- **HDBSCAN**: Clustering jerárquico
- **Plotly**: Visualizaciones interactivas

---

## 📞 Soporte

### Para Usuarios No Técnicos

1. Lee: `INSTRUCCIONES_PRIMERA_VEZ.md`
2. Lee: `MANUAL_USUARIO.md` → Sección "Solución de Problemas"
3. Abre un Issue en GitHub con:
   - Descripción del problema
   - Capturas de pantalla
   - Mensaje de error completo

### Para Desarrolladores

1. Lee: `src/README_TECNICO.md`
2. Lee: `src/FAQ.md`
3. Revisa Issues existentes en GitHub
4. Abre un nuevo Issue con detalles técnicos

---

## 📊 Estadísticas del Proyecto

- **Líneas de código**: ~1,500
- **Tamaño del dataset**: 816 MB (noticias) + 1 GB (embeddings)
- **Tiempo de entrenamiento**: 15-30 minutos (preset Estándar)
- **Tópicos encontrados**: 40-80 (configuración por defecto)

---

## 🗺️ Roadmap

- [ ] Soporte para otros idiomas (inglés, francés)
- [ ] Interfaz para cargar datasets propios
- [ ] Comparación de múltiples modelos
- [ ] Exportación a PDF de reportes
- [ ] Integración con APIs externas
- [ ] Modo batch para procesar múltiples archivos

---

## ⭐ Si te fue útil

Si este proyecto te ayudó, considera:

- ⭐ Darle una estrella en GitHub
- 🐛 Reportar bugs o sugerir mejoras
- 📢 Compartirlo con colegas economistas
- 🤝 Contribuir con código o documentación

---

**Versión**: 1.0  
**Última actualización**: Noviembre 2025  
**Mantenedor**: [Tu Nombre/Email]

---

<div align="center">

**¡Gracias por usar Top2Vec para Economistas!** 🎉

[Documentación](MANUAL_USUARIO.md) • [Issues](https://github.com/TU_USUARIO/TU_REPO/issues) • [Contribuir](CONTRIBUTING.md)

</div>
