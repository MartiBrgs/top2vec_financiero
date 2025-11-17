# 🚀 GUÍA DE INICIO RÁPIDO

## ⚡ 3 Pasos para Empezar

### 1️⃣ Instalar Software

Abre **PowerShell** y ejecuta:

```powershell
pip install uv
```

### 2️⃣ Ejecutar el Modelo

```powershell
cd top2vec_para_economistas
uv run python ejecutar_modelo.py
```

### 3️⃣ Ver Resultados

Abre el archivo: `resultados/resumen_topicos.xlsx`

---

## 🎯 Atajos Rápidos

### Ver resultados en Excel
```powershell
cd resultados
start resumen_topicos.xlsx
```

### Ver resultados en texto
```powershell
cd resultados
notepad resumen_topicos.txt
```

### Re-ejecutar con configuración diferente
1. Edita `configuracion.py`
2. Ejecuta `uv run python ejecutar_modelo.py` nuevamente

---

## 📊 Presets Recomendados

### Análisis General (Por defecto)
✅ Ya está configurado - solo ejecuta el script

### Capturar Temas Emergentes
1. Abre `configuracion.py`
2. Descomenta las líneas del "PRESET 2: TEMAS EMERGENTES"
3. Ejecuta el script

### Solo Macro-Temas
1. Abre `configuracion.py`
2. Descomenta las líneas del "PRESET 3: MACRO-TEMAS"
3. Ejecuta el script

---

## ❓ Problemas Comunes

### "No se encuentra el archivo"
✅ Asegúrate de estar en la carpeta `top2vec_para_economistas`

### "Error de memoria"
✅ Edita `configuracion.py` y aumenta `min_cluster_size` a 100

### Muy pocos tópicos
✅ Edita `configuracion.py` y reduce `min_cluster_size` a 30

---

## 📖 Más Información

Lee el `README.md` completo para explicaciones detalladas de cada parámetro.
