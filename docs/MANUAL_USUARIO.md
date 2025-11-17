# 📖 MANUAL DE USUARIO - TOP2VEC

## Análisis de Tópicos en Noticias Económicas

**Versión**: 1.0  
**Fecha**: Noviembre 2025  
**Dirigido a**: Economistas y analistas sin conocimientos técnicos

---

## 📋 Tabla de Contenidos

1. [Introducción](#introducción)
2. [Requisitos del Sistema](#requisitos-del-sistema)
3. [Instalación Paso a Paso](#instalación-paso-a-paso)
4. [Uso de la Aplicación](#uso-de-la-aplicación)
5. [Interpretación de Resultados](#interpretación-de-resultados)
6. [Solución de Problemas](#solución-de-problemas)
7. [Preguntas Frecuentes](#preguntas-frecuentes)
8. [Glosario](#glosario)

---

## 🎯 Introducción

### ¿Qué es Top2Vec?

Top2Vec es una herramienta de **inteligencia artificial** que lee automáticamente miles de noticias y descubre los **temas principales** que aparecen en ellas. 

**Ejemplo simple**: Si tienes 10,000 noticias económicas, Top2Vec puede identificar automáticamente que hay:
- Un grupo de noticias sobre "inflación y precios"
- Otro grupo sobre "política monetaria del banco central"
- Otro sobre "crecimiento económico y PIB"
- etc.

### ¿Para qué sirve?

- ✅ Identificar los temas más relevantes en grandes volúmenes de noticias
- ✅ Ver cómo evolucionan los temas en el tiempo
- ✅ Encontrar patrones y correlaciones con indicadores económicos
- ✅ Automatizar el análisis de contenido de medios

### ¿Qué NO necesitas saber?

- ❌ Programación
- ❌ Machine Learning
- ❌ Línea de comandos
- ❌ Configuración técnica compleja

**Todo se hace con clicks en una interfaz visual.**

---

## 💻 Requisitos del Sistema

### Hardware Mínimo

| Componente | Mínimo | Recomendado |
|------------|--------|-------------|
| **Procesador** | Intel i5 (4 núcleos) | Intel i7 (8 núcleos) |
| **RAM** | 8 GB | 16 GB o más |
| **Disco Duro** | 5 GB libres | 10 GB libres |
| **Conexión** | Internet (solo instalación) | — |

### Software Necesario

1. **Sistema Operativo**: Windows 10 o superior
2. **Python**: Versión 3.8 o superior
   - ⚠️ Si no lo tienes, se explica cómo instalarlo más adelante

### ¿Cómo saber si tengo Python instalado?

1. Abre el "Símbolo del sistema" (busca "cmd" en el menú inicio)
2. Escribe: `python --version`
3. Si ves algo como "Python 3.12.4" → ✅ Ya lo tienes
4. Si ves un error → ❌ Debes instalarlo

---

## 🔧 Instalación Paso a Paso

### Paso 1: Instalar Python (si no lo tienes)

#### 1.1 Descargar Python

1. Ve a: [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Haz click en el botón amarillo: **"Download Python 3.x.x"**
3. Guarda el archivo descargado

#### 1.2 Instalar Python

1. **Doble click** en el archivo descargado
2. ⚠️ **MUY IMPORTANTE**: Marca la casilla **"Add Python to PATH"**
   
   ![Imagen: Checkbox "Add Python to PATH"]
   
3. Click en **"Install Now"**
4. Espera a que termine la instalación (2-5 minutos)
5. Click en **"Close"**

#### 1.3 Verificar la instalación

1. Abre el "Símbolo del sistema" (cmd)
2. Escribe: `python --version`
3. Deberías ver: `Python 3.x.x`
4. Si funciona → ✅ Listo para continuar

---

### Paso 2: Instalar Top2Vec

#### 2.1 Ubicar la carpeta

1. Abre el Explorador de Windows
2. Navega a la carpeta del proyecto:
   ```
   D:\Top2Vec\top2vec_para_economistas\
   ```

#### 2.2 Ejecutar el instalador

1. **Doble click** en el archivo: **`INSTALAR.bat`**
2. Se abrirá una ventana negra (no la cierres)
3. Presiona **Enter** cuando te lo pida
4. Espera a que termine (5-10 minutos)
5. Verás el mensaje: **"✓ INSTALACION COMPLETADA"**
6. Presiona **Enter** para cerrar

#### 2.3 Verificar que todo esté listo

Deberías ver estos archivos en la carpeta:
```
✓ INICIAR_APP.bat          ← Para abrir la aplicación
✓ INSTALAR.bat             ← Ya lo ejecutaste
✓ MANUAL_USUARIO.md        ← Este archivo
✓ data/                    ← Carpeta con noticias
✓ src/                     ← Carpeta con código
```

---

## 🚀 Uso de la Aplicación

### Iniciar la Aplicación

1. **Doble click** en: **`INICIAR_APP.bat`**
2. Se abrirá una ventana negra (no la cierres)
3. Espera 10-15 segundos
4. Tu navegador se abrirá automáticamente con la aplicación

![Imagen: Ventana de inicio]

**URL**: http://localhost:8501

⚠️ **Importante**: 
- NO cierres la ventana negra mientras uses la aplicación
- Para cerrar la aplicación, cierra la ventana negra

---

### Interfaz de la Aplicación

La aplicación tiene **2 pestañas principales**:

```
┌─────────────────────────────────────────┐
│  [🔧 Entrenar Nuevo Modelo]  [📊 Explorar Resultados]  │
└─────────────────────────────────────────┘
```

---

## 🔧 Pestaña 1: Entrenar Nuevo Modelo

Esta pestaña te permite entrenar un modelo Top2Vec con tus propios parámetros.

### Paso 1: Configuración Básica

#### 1.1 Seleccionar un Preset

Un **preset** es una configuración predefinida. Hay 3 opciones:

| Preset | ¿Cuándo usarlo? | Resultado |
|--------|-----------------|-----------|
| **Análisis General** | Primera vez / No estás seguro | 20-30 tópicos balanceados |
| **Temas Emergentes** | Buscas tópicos pequeños/raros | 40-50 tópicos, incluye temas minoritarios |
| **Macro-Temas** | Solo quieres temas muy grandes | 10-15 tópicos muy generales |

**Recomendación**: Empieza con **"Análisis General"**

#### 1.2 Nombre del Modelo

- El sistema sugiere automáticamente un nombre con fecha/hora
- Ejemplo: `modelo_20251116_153022`
- Puedes cambiarlo por algo más descriptivo:
  - `noticias_2024_trimestre4`
  - `analisis_inflacion_2023`

### Paso 2: Parámetros Avanzados (Opcional)

Si marcas **"Mostrar parámetros avanzados"**, verás:

#### 🔍 Parámetros de Agrupación (HDBSCAN)

**Tamaño Mínimo de Cluster** (10-200, default: 50)
- ¿Qué hace? Define cuántas noticias mínimo debe haber para formar un tópico
- ⬆️ Aumentar a 100 → Menos tópicos, más generales
- ⬇️ Reducir a 30 → Más tópicos, más específicos

**Muestras Mínimas** (5-100, default: 25)
- ¿Qué hace? Define qué tan "denso" debe ser un grupo para ser considerado tópico
- ⬆️ Aumentar → Tópicos más robustos
- ⬇️ Reducir → Captura tópicos más dispersos

#### 🗺️ Parámetros de Reducción Dimensional (UMAP)

**Número de Vecinos** (10-200, default: 50)
- ¿Qué hace? Define cuántos documentos cercanos considerar
- ⬆️ Aumentar a 100 → Captura estructura global (temas amplios)
- ⬇️ Reducir a 30 → Captura estructura local (temas específicos)

**Componentes** (2-10, default: 5)
- ¿Qué hace? Dimensiones del espacio reducido
- **No cambiar** a menos que sepas lo que haces

#### 🔗 Fusión de Tópicos

**Delta de Fusión** (0.01-0.30, default: 0.10)
- ¿Qué hace? Define qué tan similares deben ser dos tópicos para fusionarse
- ⬆️ Aumentar a 0.15 → Fusiona más (menos tópicos finales)
- ⬇️ Reducir a 0.05 → Mantiene separados (más tópicos finales)

### Paso 3: Entrenar el Modelo

1. Click en el botón azul: **"🚀 Entrenar Modelo"**
2. Verás una barra de progreso
3. Monitoreo en tiempo real:
   - **Tiempo transcurrido**
   - **Uso de CPU**
   - **Uso de memoria RAM**
   - **Log detallado** (puedes expandirlo)

**Tiempo estimado**: 15-30 minutos

⚠️ **Durante el entrenamiento**:
- ✅ Puedes minimizar el navegador
- ✅ Puedes usar otras aplicaciones
- ❌ NO cierres el navegador ni la ventana negra
- ❌ NO apagues el computador

### Paso 4: Completado

Cuando termine verás:
```
✅ Modelo entrenado exitosamente!

- Tópicos encontrados: 25
- Tiempo total: 18.5 minutos
- Guardado en: modelos/modelo_20251116_153022
```

El modelo se carga automáticamente para exploración.

---

## 📊 Pestaña 2: Explorar Resultados

Esta pestaña te permite visualizar y descargar los resultados.

### Paso 1: Seleccionar un Modelo

Tienes 2 opciones:

#### Opción A: Usar modelo recién entrenado
- Si acabas de entrenar un modelo, se carga automáticamente
- Verás: ✅ Modelo activo: **modelo_20251116_153022**

#### Opción B: Cargar modelo anterior
1. Desmarca: **"Usar modelo recién entrenado"**
2. Selecciona un modelo del desplegable
3. Click en: **"📥 Cargar Modelo"**

### Paso 2: Vista General

En la parte superior verás **4 métricas**:

```
┌──────────────────────────────────────────────────────┐
│  Total de Tópicos    Total de Documentos            │
│        25                  85,234                     │
│                                                       │
│  Promedio Docs/Tópico   Tópico Más Grande           │
│       3,409                  8,125                    │
└──────────────────────────────────────────────────────┘
```

### Paso 3: Explorar un Tópico

#### 3.1 Seleccionar tópico

Usa el desplegable: **"Selecciona un tópico para explorar"**

Verás opciones como:
- `Tópico 0 (8,125 docs)`
- `Tópico 1 (5,432 docs)`
- `Tópico 2 (4,821 docs)`
- ...

Los tópicos están ordenados de mayor a menor cantidad de documentos.

#### 3.2 Panel Izquierdo: WordCloud y Palabras

**WordCloud** (Nube de Palabras)
- Visualización gráfica de las palabras más importantes
- Tamaño de la palabra = relevancia
- Colores = solo para diferenciación visual

**Tabla de Palabras Clave**
- Las 20 palabras más relevantes del tópico
- Columna "Relevancia": Score de 0 a 1
  - 0.8-1.0 = Muy característico
  - 0.6-0.8 = Bastante relevante
  - 0.4-0.6 = Moderadamente relacionado

**Ejemplo**:
```
Tópico 5 - Inflación
┌─────────────┬────────────┐
│ Palabra     │ Relevancia │
├─────────────┼────────────┤
│ inflación   │ 0.8532     │
│ ipc         │ 0.7891     │
│ precios     │ 0.7245     │
│ banco       │ 0.6834     │
│ central     │ 0.6512     │
└─────────────┴────────────┘
```

Interpretación: Este tópico trata claramente sobre inflación y política monetaria.

#### 3.3 Panel Derecho: Evolución Temporal

**Gráfico de Serie Temporal**
- Eje X: Fechas
- Eje Y: Cantidad de documentos
- Línea azul: Frecuencia diaria del tópico

Puedes hacer **zoom** en el gráfico:
- Click y arrastra para seleccionar un período
- Doble click para volver al zoom original

**Estadísticas Temporales**
- **Total Docs**: Cantidad total de noticias en este tópico
- **Promedio Diario**: Promedio de noticias por día
- **Máximo Diario**: Día con más noticias del tópico

**Interpretación**:
- Picos altos = Períodos de mucha cobertura mediática
- Valles = Períodos de poca cobertura
- Tendencia creciente = Tema cada vez más relevante
- Tendencia decreciente = Tema perdiendo relevancia

### Paso 4: Análisis Adicionales

#### Documentos Representativos

Expande: **"📄 Ver Documentos Representativos"**

Verás las 5 noticias más representativas del tópico:
- ID del documento
- Score de relevancia
- Primeros 500 caracteres del texto

**¿Para qué sirve?**
- Validar que el tópico tiene sentido
- Leer ejemplos reales
- Entender el contexto mejor

#### Distribución de Documentos

Expande: **"📊 Distribución de Documentos"**

Gráfico de barras con todos los tópicos:
- Permite comparar tamaños relativos
- Identificar tópicos dominantes vs minoritarios

---

## 💾 Descargas

### Descargas Individuales (por tópico)

**1. WordCloud (PNG)**
```
📥 Descargar WordCloud
```
- Formato: Imagen PNG
- Uso: Presentaciones, informes
- Tamaño: ~200 KB

**2. Palabras Clave (CSV)**
```
📥 Descargar Palabras (CSV)
```
- Formato: CSV (Excel-compatible)
- Columnas: Palabra, Relevancia
- Uso: Análisis cuantitativo

**3. Serie Temporal (CSV)**
```
📥 Descargar Serie Temporal (CSV)
```
- Formato: CSV
- Columnas: fecha, frecuencia
- Uso: Análisis de series temporales en Excel/R/Python

### Descargas Globales (todos los tópicos)

**1. Excel Completo**
```
📥 Descargar Todo en Excel
```

Archivo con 3 hojas:
- **Hoja 1: Resumen_Topicos**
  - Columnas: topic_id, num_documentos, palabras_clave, palabra_1-10, score_1-10
- **Hoja 2: Series_Temporales**
  - Pivot table: fecha × tópico
- **Hoja 3: Metadata**
  - Información del modelo (total tópicos, fecha, etc.)

Tamaño: ~5-10 MB
**Recomendado para análisis completo**

**2. Resumen CSV**
```
📥 Descargar Resumen (CSV)
```

Tabla simplificada:
- Columnas: topic_id, num_documentos, palabras_clave
- Más liviano que Excel
- Fácil de importar en cualquier herramienta

---

## 📖 Interpretación de Resultados

### ¿Cómo identificar buenos tópicos?

Un tópico de **buena calidad** tiene:
1. ✅ Palabras clave coherentes entre sí
2. ✅ Un tema claro y distinguible
3. ✅ Suficientes documentos (> 100)

Un tópico **problemático** puede tener:
1. ❌ Palabras muy genéricas ("cosa", "hacer", "muy")
2. ❌ Mezcla de temas no relacionados
3. ❌ Muy pocos documentos (< 30)

**Solución**: Re-entrenar con parámetros diferentes

### Casos de Uso Prácticos

#### Caso 1: Análisis de Crisis

**Pregunta**: ¿Qué temas dominaron durante la crisis de 2020?

**Pasos**:
1. Entrenar modelo con preset "Análisis General"
2. En cada tópico, ver serie temporal
3. Identificar tópicos con picos en 2020
4. Revisar palabras clave de esos tópicos
5. Exportar series temporales a Excel para análisis detallado

#### Caso 2: Monitoreo de Inflación

**Pregunta**: ¿Cómo ha evolucionado la cobertura de inflación?

**Pasos**:
1. Entrenar modelo
2. Buscar tópico relacionado a inflación (palabras: inflación, ipc, precios)
3. Ver evolución temporal
4. Correlacionar con datos de IPC real
5. Descargar serie temporal para análisis econométrico

#### Caso 3: Identificación de Temas Emergentes

**Pregunta**: ¿Qué nuevos temas aparecieron recientemente?

**Pasos**:
1. Entrenar con preset "Temas Emergentes"
2. Revisar tópicos pequeños (< 500 docs)
3. Filtrar por serie temporal: buscar tópicos con crecimiento reciente
4. Analizar si son temas nuevos o ruido

---

## 🔧 Solución de Problemas

### Problema 1: No se abre la aplicación

**Síntomas**: Doble click en INICIAR_APP.bat → Ventana se abre y cierra rápidamente

**Soluciones**:
1. Verifica que Python esté instalado:
   - Abre cmd
   - Escribe: `python --version`
   - Si no funciona → Instala Python (ver Paso 1 de instalación)

2. Ejecuta de nuevo: `INSTALAR.bat`

3. Lee el error:
   - Edita `INICIAR_APP.bat`
   - Cambia la última línea por: `pause`
   - Guarda y ejecuta nuevamente
   - Ahora verás el error

### Problema 2: Error de memoria durante entrenamiento

**Síntomas**: 
```
MemoryError: Unable to allocate array
```

**Soluciones**:
1. Cierra otros programas (Chrome, Excel, etc.)
2. Re-entrena con parámetros más conservadores:
   - Tamaño Mínimo de Cluster: 100
   - Número de Vecinos: 30
3. Reinicia el computador antes de entrenar

### Problema 3: Muy pocos tópicos

**Síntomas**: Solo obtengo 5-10 tópicos cuando esperaba más

**Soluciones**:
1. Reduce "Tamaño Mínimo de Cluster" a 30
2. Reduce "Delta de Fusión" a 0.05
3. Usa preset "Temas Emergentes"

### Problema 4: Muchos tópicos pequeños

**Síntomas**: Obtengo 50+ tópicos, muchos con pocos documentos

**Soluciones**:
1. Aumenta "Tamaño Mínimo de Cluster" a 75
2. Aumenta "Delta de Fusión" a 0.15
3. Usa preset "Macro-Temas"

### Problema 5: La aplicación se cuelga

**Síntomas**: El navegador dice "Not Responding"

**Soluciones**:
1. Espera 5-10 minutos (puede ser procesamiento intenso)
2. Si sigue colgada después de 20 minutos:
   - Cierra el navegador
   - Cierra la ventana negra
   - Reinicia la aplicación

### Problema 6: Los tópicos no tienen sentido

**Síntomas**: Las palabras clave de un tópico no están relacionadas

**Posibles causas**:
1. Datos muy ruidosos
2. Parámetros inadecuados
3. Corpus muy pequeño (< 1,000 documentos)

**Soluciones**:
1. Revisa la calidad de los datos originales
2. Usa preset "Análisis General" con parámetros por defecto
3. Si el corpus es pequeño, reduce "Tamaño Mínimo de Cluster" a 20

---

## ❓ Preguntas Frecuentes

### Generales

**¿Necesito internet para usar Top2Vec?**
- Solo para la instalación inicial
- Una vez instalado, funciona offline

**¿Puedo usar mis propias noticias?**
- Sí, pero requiere conocimientos técnicos
- Contacta al administrador del sistema

**¿Los resultados son reproducibles?**
- Sí, si usas los mismos parámetros
- El modelo usa semillas aleatorias fijas

### Técnicas

**¿Qué algoritmos usa Top2Vec?**
- Embeddings: Doc2Vec o modelos transformer
- Reducción dimensional: UMAP
- Clustering: HDBSCAN

**¿Puedo cambiar el idioma?**
- El modelo actual está optimizado para español
- Preserva tildes y ñ

**¿Cuánta RAM necesito realmente?**
- Mínimo: 8 GB
- Recomendado: 16 GB
- Con 100,000+ documentos: 32 GB

### Sobre los Datos

**¿Cuántas noticias hay en el dataset?**
- Aproximadamente 100,000 noticias económicas
- Período: 2018-2025 (7 años)

**¿De dónde vienen las noticias?**
- Fuentes de medios económicos chilenos
- Corpus preprocesado y anonimizado

**¿Puedo ver el texto completo de una noticia?**
- Sí, en "Ver Documentos Representativos"
- Se muestra una muestra de cada noticia

---

## 📚 Glosario

### Términos Básicos

**Tópico / Tema**
- Grupo de documentos (noticias) sobre un tema similar
- Representado por palabras clave

**WordCloud / Nube de Palabras**
- Visualización donde el tamaño = relevancia
- Permite identificar rápidamente el tema

**Embedding**
- Representación numérica de un texto
- Permite comparar similitud entre documentos

**Score / Relevancia**
- Número entre 0 y 1
- Indica qué tan representativa es una palabra de un tópico

### Términos Técnicos

**Clustering**
- Proceso de agrupar documentos similares
- Automático (no supervisado)

**HDBSCAN**
- Algoritmo de clustering jerárquico
- Encuentra grupos densos automáticamente

**UMAP**
- Algoritmo de reducción dimensional
- Preserva la estructura local y global de los datos

**Preset**
- Configuración predefinida de parámetros
- Facilita el uso para no expertos

**Min Cluster Size**
- Mínimo de documentos para formar un tópico
- Parámetro clave de HDBSCAN

**Topic Merge Delta**
- Umbral de similitud para fusionar tópicos
- Reduce redundancia

---

## 📞 Soporte y Contacto

### Documentación Adicional

- **README.md**: Documentación técnica completa
- **FAQ.md**: Preguntas frecuentes detalladas
- **RESUMEN_APLICACION.txt**: Características técnicas

### Reportar Problemas

Si encuentras un error no cubierto en este manual:
1. Anota el mensaje de error exacto
2. Indica qué estabas haciendo cuando ocurrió
3. Incluye capturas de pantalla si es posible
4. Contacta al equipo de soporte técnico

### Actualizaciones

Para verificar si hay una nueva versión:
- Revisa la carpeta del proyecto
- Busca el archivo: `VERSION.txt`
- Compara con la versión actual (1.0)

---

## 📝 Notas Finales

### Buenas Prácticas

1. ✅ **Empieza simple**: Usa presets antes de parámetros avanzados
2. ✅ **Documenta**: Anota qué configuración usaste y por qué
3. ✅ **Itera**: Prueba diferentes configuraciones
4. ✅ **Valida**: Revisa documentos representativos para validar tópicos
5. ✅ **Exporta**: Guarda los resultados importantes

### Limitaciones

- ⚠️ Los tópicos son automáticos (pueden no coincidir con categorías predefinidas)
- ⚠️ Requiere suficientes datos (mínimo 1,000 documentos recomendado)
- ⚠️ El entrenamiento es intensivo (15-30 minutos)
- ⚠️ No garantiza tópicos perfectos (requiere interpretación humana)

---

**¡Gracias por usar Top2Vec!**

*Este manual se actualiza periódicamente. Versión actual: 1.0 (Noviembre 2025)*

---
