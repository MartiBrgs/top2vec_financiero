# 🎯 RESUMEN: PRIMERA VEZ (Usuario No Programador)

## ⏱️ Tiempo Total: 30-45 minutos

---

## 📋 Checklist Simplificado

### ✅ ANTES DE EMPEZAR

- [ ] Computadora con Windows 10+
- [ ] 8 GB RAM mínimo (16 GB recomendado)
- [ ] 5 GB de espacio en disco
- [ ] Conexión a internet (solo para instalación)

---

## 🚀 PASOS (No programadores)

### 1️⃣ DESCARGAR EL PROYECTO (2 minutos)

**GitHub:**
1. Ve a: `https://github.com/TU_USUARIO/TU_REPOSITORIO`
2. Click en botón verde **"Code"**
3. Click en **"Download ZIP"**
4. Descomprime en: `C:\Proyectos\top2vec_para_economistas\`

⚠️ **Importante:** La ruta NO debe tener espacios ni acentos

---

### 2️⃣ INSTALAR PYTHON (10 minutos) - SOLO SI NO LO TIENES

**¿Cómo saber si ya lo tengo?**
1. Presiona `Windows + R`
2. Escribe: `cmd`
3. Escribe: `python --version`
4. Si dice `Python 3.12.x` → ✅ **Ya lo tienes**
5. Si dice "no se reconoce" → ⬇️ **Instálalo**

**Instalación:**
1. Ve a: https://www.python.org/downloads/
2. Descarga **Python 3.12**
3. **CRÍTICO**: Marca la casilla **"Add Python to PATH"** ✅
4. Click en **"Install Now"**
5. **Reinicia tu computadora**

---

### 3️⃣ INSTALAR DEPENDENCIAS (5-10 minutos) - SOLO PRIMERA VEZ

1. Abre la carpeta: `C:\Proyectos\top2vec_para_economistas\`
2. **Doble click en:** `INSTALAR.bat`
3. Espera 5-10 minutos (descarga paquetes de internet)
4. Verás:

```
╔════════════════════════════════════════════════════════╗
║    INSTALACION COMPLETADA EXITOSAMENTE                 ║
╚════════════════════════════════════════════════════════╝

Presiona cualquier tecla para continuar...
```

5. ✅ **¡Listo!** Ya puedes usar la aplicación

---

### 4️⃣ INICIAR APLICACIÓN (30 segundos)

1. **Doble click en:** `INICIAR_APP.bat`
2. Se abre una ventana negra → **NO LA CIERRES**
3. Espera 10-30 segundos
4. Tu navegador se abre automáticamente
5. Verás la aplicación en: `http://localhost:8501`

---

### 5️⃣ ENTRENAR PRIMER MODELO (15-30 minutos)

**En la aplicación web:**

1. Ve a pestaña: **"🎯 Entrenar Modelo"**
2. En "Presets", selecciona: **"Estándar (Recomendado)"**
3. Click en: **"🚀 Entrenar Modelo"**
4. **Espera 15-20 minutos** (verás barra de progreso)
5. Mensaje: **"✅ Modelo entrenado exitosamente"**

---

### 6️⃣ VER RESULTADOS (2 minutos)

1. Ve a pestaña: **"📊 Explorar Resultados"**
2. Verás:
   - Gráfico 3D de tópicos
   - WordClouds de palabras clave
   - Series temporales
3. Click en: **"📥 Descargar Resumen Excel"**
4. Abre el Excel descargado

✅ **¡Felicidades! Ya sabes usar Top2Vec** 🎉

---

## 🔄 USOS SIGUIENTES (Después de la primera vez)

**SOLO necesitas:**

```
1. Doble click en: INICIAR_APP.bat
2. Espera que se abra el navegador
3. ¡Listo!
```

❌ **NO vuelvas a ejecutar `INSTALAR.bat`** (solo fue necesario la primera vez)

---

## 📖 Documentación Útil

| Si quieres... | Lee... |
|---------------|--------|
| Instrucciones paso a paso con imágenes | `INSTRUCCIONES_PRIMERA_VEZ.md` |
| Manual completo (200 págs) | `MANUAL_USUARIO.md` |
| Resumen ultra-rápido | `EMPEZAR_AQUI.md` |

---

## ❓ Preguntas Frecuentes

### ¿Necesito saber programar?
**NO**. Solo haces doble click en archivos `.bat`

### ¿Cuánto tarda entrenar un modelo?
- Preset Rápido: 5-10 min
- Preset Estándar: 15-20 min
- Preset Detallado: 30-45 min

### ¿Necesito internet?
- Primera instalación: **SÍ**
- Usos posteriores: **NO** (funciona offline)

### ¿Puedo cerrar el navegador?
**SÍ**, pero **NO cierres la ventana negra** (terminal)

### ¿Cómo detengo la aplicación?
Cierra la ventana negra o presiona `Ctrl+C`

---

## 🆘 Problemas Comunes

### ❌ "Python no encontrado"
**Solución:** Reinstala Python marcando **"Add to PATH"** y reinicia PC

### ❌ La aplicación no se abre
**Solución:** Abre manualmente `http://localhost:8501` en tu navegador

### ❌ Error en `INSTALAR.bat`
**Solución:** Verifica que tienes internet y Python instalado

---

## 📧 Mensaje para Enviar a Usuarios

```
Hola,

Te comparto la herramienta de análisis de tópicos en noticias.

PARA EMPEZAR (primera vez):
1. Descarga desde: [LINK AL GITHUB]
2. Lee: INSTRUCCIONES_PRIMERA_VEZ.md
3. Doble click en: INSTALAR.bat (solo una vez)
4. Doble click en: INICIAR_APP.bat
5. Sigue las instrucciones en la aplicación web

TIEMPO: 30-45 minutos (primera instalación + entrenamiento)

USOS SIGUIENTES: Solo doble click en INICIAR_APP.bat

DOCUMENTACIÓN:
- INSTRUCCIONES_PRIMERA_VEZ.md (paso a paso)
- MANUAL_USUARIO.md (manual completo)
- EMPEZAR_AQUI.md (resumen rápido)

¿DUDAS? Lee las secciones de "Solución de Problemas" en los documentos

Saludos
```

---

## ✅ Validación Final

**Antes de compartir con usuarios, verifica:**

- [ ] Todos los archivos están en el repositorio
- [ ] `INSTALAR.bat` funciona correctamente
- [ ] `INICIAR_APP.bat` abre la aplicación
- [ ] Los datos están en `data/` (noticias.csv + embeddings_precalculados.npz)
- [ ] La documentación es clara y sin errores
- [ ] Has probado el flujo completo en otra computadora

---

**Versión**: 1.0  
**Creado**: Noviembre 2025  
**Audiencia**: Economistas y analistas sin conocimientos de programación
