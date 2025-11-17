# 📤 GUÍA: Qué Subir a GitHub

---

## ✅ ARCHIVOS QUE DEBES SUBIR

### 📂 Raíz del Proyecto

```
top2vec_para_economistas/
├── ✅ INSTALAR.bat
├── ✅ INICIAR_APP.bat
├── ✅ README.md (o renombra README_GITHUB.md → README.md)
├── ✅ README_GITHUB.md (opcional, como backup)
├── ✅ INSTRUCCIONES_PRIMERA_VEZ.md
├── ✅ MANUAL_USUARIO.md
├── ✅ EMPEZAR_AQUI.md
├── ✅ RESUMEN_PRIMERA_VEZ.md
├── ✅ PLANTILLA_MENSAJE.md
├── ✅ requirements.txt
├── ✅ pyproject.toml
├── ✅ LICENSE (si tienes uno)
└── ✅ .gitignore (crear uno nuevo)
```

### 📂 src/

```
src/
├── ✅ app.py
├── ✅ ejecutar_modelo.py
├── ✅ configuracion.py
├── ✅ analisis_avanzado.py
├── ✅ README_TECNICO.md
├── ✅ README_APP.md
├── ✅ FAQ.md
├── ✅ INICIO_RAPIDO.md
├── ✅ .streamlit/
│   └── ✅ config.toml
└── ✅ utils/ (si tienes archivos Python adicionales)
```

### 📂 data/

⚠️ **PROBLEMA**: Los archivos de datos son muy grandes para GitHub

**Opciones:**

#### Opción 1: Git LFS (Recomendado para archivos grandes)
```bash
# Instalar Git LFS
git lfs install

# Rastrear archivos grandes
git lfs track "data/noticias.csv"
git lfs track "data/embeddings_precalculados.npz"

# Agregar .gitattributes
git add .gitattributes

# Subir normalmente
git add data/
git commit -m "Add large data files"
git push
```

#### Opción 2: Enlace Externo (Más simple)
```
❌ NO subir los archivos grandes a GitHub

✅ Subir un README en data/ con instrucciones:

data/
└── ✅ README_DATOS.md (instrucciones de descarga)

Contenido de README_DATOS.md:
---
# Datos del Proyecto

Los datos son demasiado grandes para GitHub.

Descarga desde:
- Google Drive: [LINK]
- OneDrive: [LINK]
- Dropbox: [LINK]

Archivos necesarios:
1. noticias.csv (816 MB)
2. embeddings_precalculados.npz (1 GB)

Colócalos en esta carpeta (data/)
---
```

#### Opción 3: Datos de Muestra
```
✅ Subir solo una muestra pequeña para pruebas

data/
├── ✅ noticias_sample.csv (primeras 1000 filas, ~10 MB)
├── ✅ README_DATOS.md (instrucciones para datos completos)
└── ❌ NO subir archivos completos
```

### 📂 modelos/

```
❌ NO subir modelos entrenados (archivos .model son grandes)

✅ Subir solo un README:

modelos/
└── ✅ README_MODELOS.md

Contenido:
---
# Carpeta de Modelos

Esta carpeta se generará automáticamente cuando entrenes 
tu primer modelo usando la aplicación.

No es necesario descargar nada aquí.
---
```

### 📂 resultados/

```
❌ NO subir resultados (son archivos generados)

✅ Subir solo estructura:

resultados/
├── ✅ README_RESULTADOS.md
└── ✅ .gitkeep (archivo vacío para mantener la carpeta)

Contenido de README_RESULTADOS.md:
---
# Carpeta de Resultados

Aquí se guardarán automáticamente:
- Archivos Excel con resumen de tópicos
- CSV con evolución temporal
- Embeddings exportados

Esta carpeta se populará cuando uses la aplicación.
---
```

---

## ❌ ARCHIVOS QUE NO DEBES SUBIR

### Archivos Temporales y de Usuario

```
❌ .venv/ (entorno virtual)
❌ __pycache__/ (archivos compilados de Python)
❌ *.pyc (bytecode de Python)
❌ .DS_Store (macOS)
❌ Thumbs.db (Windows)
❌ *.log (archivos de log)
❌ temp_plot*.html (archivos temporales de gráficos)
```

### Archivos de Configuración Local

```
❌ .vscode/ (configuración de VS Code)
❌ .idea/ (configuración de PyCharm)
❌ *.sublime-* (configuración de Sublime Text)
```

### Archivos Grandes

```
❌ data/noticias.csv (816 MB) → usar Git LFS o enlace externo
❌ data/embeddings_precalculados.npz (1 GB) → usar Git LFS o enlace externo
❌ modelos/*.model (modelos entrenados)
❌ resultados/*.xlsx (resultados generados)
```

---

## 📝 CREAR .gitignore

Crea un archivo `.gitignore` en la raíz con este contenido:

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# Entornos virtuales
.venv/
venv/
ENV/
env/

# IDEs
.vscode/
.idea/
*.sublime-*
.DS_Store
Thumbs.db

# Archivos de datos grandes (si no usas Git LFS)
data/noticias.csv
data/embeddings_precalculados.npz
data/*.npz
data/*.csv

# Modelos entrenados
modelos/*.model
modelos/*.pkl
modelos/*.bin

# Resultados generados
resultados/*.xlsx
resultados/*.csv
resultados/temporal_analysis/
resultados/temporal_analysis_reduced/

# Archivos temporales
*.log
temp_*.html
*.tmp

# Jupyter Notebooks checkpoints
.ipynb_checkpoints/

# Sistema operativo
.DS_Store
Thumbs.db
desktop.ini

# Archivos de backup
*.bak
*.swp
*~
```

---

## 📋 COMANDOS PARA SUBIR A GITHUB

### Paso 1: Crear Repositorio en GitHub

1. Ve a: https://github.com/new
2. Nombre: `top2vec-para-economistas` (o similar)
3. Descripción: "Herramienta de análisis de tópicos con interfaz web para economistas"
4. Público o Privado (según prefieras)
5. **NO** marques "Initialize with README" (ya tienes uno)
6. Click en **"Create repository"**

### Paso 2: Preparar Archivos Localmente

```powershell
# Ir a la carpeta del proyecto
cd D:\Top2Vec\top2vec_para_economistas

# Crear .gitignore (si no existe)
# Copia el contenido de arriba

# Renombrar README_GITHUB.md a README.md (opcional)
Move-Item README_GITHUB.md README.md -Force

# Verificar qué archivos se van a subir
git status
```

### Paso 3: Inicializar Git y Subir

```powershell
# Inicializar repositorio
git init

# Agregar remote
git remote add origin https://github.com/TU_USUARIO/top2vec-para-economistas.git

# Agregar archivos (respetando .gitignore)
git add .

# Commit inicial
git commit -m "Initial commit: Top2Vec para economistas con interfaz web"

# Subir a GitHub
git push -u origin master
# O si usas 'main' como rama principal:
# git push -u origin main
```

### Paso 4: Si Usas Git LFS (Para Archivos Grandes)

```powershell
# Instalar Git LFS
git lfs install

# Rastrear archivos grandes
git lfs track "data/noticias.csv"
git lfs track "data/embeddings_precalculados.npz"

# Agregar .gitattributes
git add .gitattributes

# Agregar datos
git add data/

# Commit
git commit -m "Add data files with Git LFS"

# Push
git push
```

---

## 📊 ESTRUCTURA FINAL EN GITHUB

Tu repositorio debería verse así:

```
📦 top2vec-para-economistas/
│
├── 📄 README.md
├── 🔧 INSTALAR.bat
├── ▶️ INICIAR_APP.bat
├── 📖 INSTRUCCIONES_PRIMERA_VEZ.md
├── 📖 MANUAL_USUARIO.md
├── 📖 EMPEZAR_AQUI.md
├── 📖 RESUMEN_PRIMERA_VEZ.md
├── 📧 PLANTILLA_MENSAJE.md
├── 📦 requirements.txt
├── 📦 pyproject.toml
├── 🚫 .gitignore
│
├── 📂 src/
│   ├── app.py
│   ├── ejecutar_modelo.py
│   ├── configuracion.py
│   ├── analisis_avanzado.py
│   ├── README_TECNICO.md
│   ├── README_APP.md
│   ├── FAQ.md
│   ├── INICIO_RAPIDO.md
│   └── .streamlit/
│       └── config.toml
│
├── 📂 data/
│   ├── README_DATOS.md
│   ├── noticias.csv (si usas Git LFS)
│   └── embeddings_precalculados.npz (si usas Git LFS)
│
├── 📂 modelos/
│   └── README_MODELOS.md
│
└── 📂 resultados/
    └── README_RESULTADOS.md
```

---

## ✅ CHECKLIST ANTES DE SUBIR

- [ ] ✅ Creaste `.gitignore`
- [ ] ✅ Decidiste cómo manejar archivos grandes (Git LFS o enlace externo)
- [ ] ✅ README.md está en la raíz (renombrar README_GITHUB.md)
- [ ] ✅ Todos los `.bat` funcionan correctamente
- [ ] ✅ `requirements.txt` está actualizado
- [ ] ✅ Documentación está completa y sin errores
- [ ] ✅ Has probado el flujo completo
- [ ] ✅ No hay información sensible (passwords, tokens, etc.)
- [ ] ✅ Archivos de configuración local no están incluidos

---

## 🎯 RECOMENDACIONES

### Para Archivos Grandes

**Mejor opción**: Git LFS si tu cuenta de GitHub lo soporta (gratis hasta 1 GB)

**Alternativa**: Google Drive/OneDrive con README_DATOS.md indicando enlace de descarga

### Para el README.md

Usa `README_GITHUB.md` como tu README.md principal:
```powershell
Move-Item README_GITHUB.md README.md -Force
```

### Para la Licencia

Agrega un archivo LICENSE. Para código abierto, considera:
- MIT License (muy permisiva)
- Apache 2.0 (más formal)
- GPL v3 (copyleft)

### Para Imágenes/Capturas

Si quieres agregar capturas de pantalla:
```
docs/
└── screenshots/
    ├── train_tab.png
    ├── explore_tab.png
    └── results_example.png
```

---

## 📞 COMPARTIR CON USUARIOS

Una vez subido a GitHub, comparte:

```
URL del repositorio:
https://github.com/TU_USUARIO/top2vec-para-economistas

Instrucciones:
1. Click en "Code" → "Download ZIP"
2. Descomprimir
3. Leer: INSTRUCCIONES_PRIMERA_VEZ.md
4. Doble click en: INSTALAR.bat
5. Doble click en: INICIAR_APP.bat
```

---

**Versión**: 1.0  
**Última actualización**: Noviembre 2025
