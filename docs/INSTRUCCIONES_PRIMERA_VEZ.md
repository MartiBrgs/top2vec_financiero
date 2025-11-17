# 📋 INSTRUCCIONES PARA LA PRIMERA VEZ

## 🎯 Para Usuarios No Programadores

---

## 📥 PASO 1: Descargar el Proyecto

### Opción A: Desde GitHub (Recomendado)

1. Ve a: `https://github.com/TU_USUARIO/TU_REPOSITORIO`
2. Haz click en el botón verde **"Code"**
3. Selecciona **"Download ZIP"**
4. Descomprime el archivo ZIP en tu computadora
   - Recomendado: `C:\Proyectos\top2vec_para_economistas\`
   - ⚠️ **Evita rutas con espacios o caracteres especiales**

### Opción B: Si te lo enviaron por correo/USB

1. Copia la carpeta `top2vec_para_economistas` a tu computadora
2. Ubicación recomendada: `C:\Proyectos\`

---

## 🐍 PASO 2: Instalar Python (Si no lo tienes)

### ¿Cómo saber si ya tengo Python?

1. Presiona `Windows + R`
2. Escribe: `cmd`
3. Presiona Enter
4. Escribe: `python --version`
5. Si aparece algo como `Python 3.12.4` → **Ya lo tienes instalado** ✅
6. Si dice "no se reconoce" → **Necesitas instalarlo** ⬇️

### Instalación de Python (10 minutos)

1. Ve a: https://www.python.org/downloads/
2. Descarga **Python 3.12** o superior
3. **MUY IMPORTANTE**: Durante la instalación
   - ✅ **Marca la casilla: "Add Python to PATH"**
   - ✅ **Selecciona: "Install for all users"**
4. Haz click en **"Install Now"**
5. Espera a que termine la instalación
6. Reinicia tu computadora

---

## ⚙️ PASO 3: Instalar Dependencias (Primera vez solamente)

1. Abre la carpeta donde descomprimiste el proyecto
2. **Doble click en:** `INSTALAR.bat`
3. Espera **5-10 minutos** (depende de tu conexión a internet)
4. Verás algo como:

```
╔════════════════════════════════════════════════════════════╗
║         TOP2VEC - INSTALACION DE DEPENDENCIAS              ║
╚════════════════════════════════════════════════════════════╝

[1/3] Verificando Python...                              ✓
[2/3] Creando entorno virtual...                         ✓
[3/3] Instalando paquetes (esto puede tardar)...         ✓

════════════════════════════════════════════════════════════
   INSTALACION COMPLETADA EXITOSAMENTE
════════════════════════════════════════════════════════════
```

5. Si ves el mensaje de éxito → **¡Listo!** ✅

**Nota**: Esto crea un entorno virtual aislado (`.venv/`) solo para esta aplicación, sin afectar tu instalación global de Python.

### ⚠️ Posibles Problemas en la Instalación

| Error | Solución |
|-------|----------|
| "Python no encontrado" | Instala Python (Paso 2) y marca "Add to PATH" |
| "pip no funciona" | Reinstala Python marcando "Add to PATH" |
| "Sin conexión a internet" | Conéctate a internet y vuelve a ejecutar `INSTALAR.bat` |
| Tarda más de 20 minutos | Normal si tienes internet lento, espera |

---

## 🚀 PASO 4: Iniciar la Aplicación

1. **Doble click en:** `INICIAR_APP.bat`
2. Se abrirá una ventana negra (terminal) - **NO LA CIERRES**
3. Espera 10-30 segundos
4. Tu navegador se abrirá automáticamente en: `http://localhost:8501`
5. Verás la aplicación web de Top2Vec 🎉

---

## 📊 PASO 5: Usar la Aplicación (Primera Ejecución)

### Entrenar tu Primer Modelo (15-30 minutos)

1. En la aplicación web, ve a la pestaña: **"🎯 Entrenar Modelo"**
2. **Opción Fácil**: Selecciona un preset
   - "Rápido (Prueba)" → 5-10 minutos
   - "Estándar (Recomendado)" → 15-20 minutos
   - "Detallado" → 30-45 minutos
3. Haz click en: **"🚀 Entrenar Modelo"**
4. Espera mientras se entrena (verás una barra de progreso)
5. Cuando termine, verás: **"✅ Modelo entrenado exitosamente"**

### Explorar Resultados

1. Ve a la pestaña: **"📊 Explorar Resultados"**
2. Verás:
   - 📊 **Gráfico 3D interactivo** de los tópicos
   - ☁️ **WordClouds** con las palabras clave de cada tópico
   - 📈 **Gráficos temporales** mostrando evolución en el tiempo
3. Descarga los resultados:
   - Haz click en **"📥 Descargar Resumen Excel"**
   - Se descargará un archivo `.xlsx` que puedes abrir en Excel

---

## 🔄 Usos Posteriores (Después de la Primera Vez)

### Cada vez que quieras usar la aplicación:

```
1. Doble click en: INICIAR_APP.bat
2. Espera que se abra el navegador
3. ¡Listo para trabajar!
```

**NO necesitas volver a ejecutar `INSTALAR.bat`** (solo fue necesario la primera vez)

---

## 📖 Documentación Adicional

| Documento | ¿Cuándo leerlo? |
|-----------|-----------------|
| **`EMPEZAR_AQUI.md`** | Resumen rápido de 2 minutos |
| **`MANUAL_USUARIO.md`** | Guía completa con capturas de pantalla |
| **`README.md`** | Información general del proyecto |

---

## ❓ Preguntas Frecuentes

### ¿Qué es Top2Vec?
Es una herramienta que encuentra tópicos (temas) automáticamente en documentos de texto usando inteligencia artificial.

### ¿Necesito saber programar?
**NO**. Solo necesitas hacer doble click en archivos `.bat` y usar la interfaz web.

### ¿Cuánto tarda entrenar un modelo?
- **Preset Rápido**: 5-10 minutos
- **Preset Estándar**: 15-20 minutos  
- **Preset Detallado**: 30-45 minutos

### ¿Puedo cerrar el navegador?
Sí, pero **NO cierres la ventana negra (terminal)**. Si la cierras, la aplicación se detendrá.

### ¿Cómo detengo la aplicación?
Cierra la ventana negra (terminal) o presiona `Ctrl+C` en ella.

### ¿Necesito internet?
- **Primera instalación**: Sí (para descargar paquetes de Python)
- **Uso normal**: No (funciona offline)

### ¿Cuánto espacio en disco necesito?
Aproximadamente **3 GB**:
- Datos: 1.8 GB (noticias + embeddings)
- Python + paquetes: 1 GB
- Modelos generados: 200-500 MB

### ¿Cuánta RAM necesito?
- **Mínimo**: 8 GB
- **Recomendado**: 16 GB

---

## 🆘 Solución de Problemas

### La aplicación no se abre en el navegador

**Solución**: Abre manualmente tu navegador y ve a: `http://localhost:8501`

### Error: "Puerto 8501 ya en uso"

**Solución**: 
1. Ya tienes una instancia corriendo
2. Ve a `http://localhost:8501` en tu navegador
3. O cierra todas las ventanas negras y vuelve a ejecutar `INICIAR_APP.bat`

### El modelo tarda mucho en entrenar

**Solución**: Esto es normal. Usa el preset "Rápido" para pruebas iniciales.

### No puedo ver los resultados

**Solución**: 
1. Verifica que el modelo terminó de entrenar (viste el mensaje de éxito)
2. Ve a la pestaña "📊 Explorar Resultados"
3. Si no hay datos, entrena primero un modelo

---

## 📞 Contacto y Soporte

Para dudas adicionales, consulta:
1. **`MANUAL_USUARIO.md`** (sección "Solución de Problemas")
2. **`src/FAQ.md`** (preguntas técnicas)

---

## ✅ Checklist de Primera Vez

Marca cada paso conforme lo completes:

- [ ] 1. Descargué y descomprimí el proyecto
- [ ] 2. Instalé Python 3.12+ (marcando "Add to PATH")
- [ ] 3. Ejecuté `INSTALAR.bat` exitosamente
- [ ] 4. Ejecuté `INICIAR_APP.bat`
- [ ] 5. La aplicación se abrió en mi navegador
- [ ] 6. Entrené mi primer modelo
- [ ] 7. Exploré los resultados
- [ ] 8. Descargué el Excel con resultados

**Si completaste todos los pasos:** ¡Felicidades! 🎉 Ya puedes usar Top2Vec

---

**Versión**: 1.0  
**Última actualización**: Noviembre 2025  
**Tiempo estimado total**: 30-45 minutos (primera vez)
