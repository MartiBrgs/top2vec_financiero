# 📊 Datos del Proyecto

---

## ⚠️ Archivos Grandes No Incluidos en el Repositorio

Los archivos de datos son demasiado grandes para incluirse directamente en GitHub.

---

## 📥 Descarga de Datos

### Opción 1: Desde Google Drive (Recomendado)

**Enlace de descarga**: [PENDIENTE - AGREGAR ENLACE]

### Opción 2: Desde OneDrive

**Enlace de descarga**: [PENDIENTE - AGREGAR ENLACE]

### Opción 3: Desde Dropbox

**Enlace de descarga**: [PENDIENTE - AGREGAR ENLACE]

---

## 📂 Archivos Necesarios

Descarga los siguientes archivos y colócalos en esta carpeta (`data/`):

| Archivo | Tamaño | Descripción |
|---------|--------|-------------|
| **`noticias.csv`** | 816 MB | Corpus de noticias económicas |
| **`embeddings_precalculados.npz`** | 1 GB | Embeddings precalculados (Doc2Vec) |

---

## 📍 Ubicación Correcta

Después de descargar, tu carpeta `data/` debe verse así:

```
data/
├── noticias.csv                    ← 816 MB
├── embeddings_precalculados.npz    ← 1 GB
└── README_DATOS.md                 ← Este archivo
```

---

## ✅ Verificación

Para verificar que descargaste correctamente los archivos, ejecuta:

```powershell
# En PowerShell
cd data
Get-ChildItem | Select-Object Name, @{Name="MB";Expression={[math]::Round($_.Length/1MB,2)}}
```

Deberías ver:

```
Name                            MB
----                            --
noticias.csv                    816.23
embeddings_precalculados.npz    1024.45
README_DATOS.md                 0.01
```

---

## 📋 Formato de los Datos

### `noticias.csv`

Estructura:

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `text` | string | Texto completo de la noticia |
| `date` | datetime | Fecha de publicación (YYYY-MM-DD) |
| `source` | string | Fuente de la noticia (opcional) |

Ejemplo:

```csv
text,date,source
"El Banco Central Europeo mantiene los tipos de interés...",2023-01-15,BCE
"La inflación en la zona euro alcanza el 8.5%...",2023-01-20,Eurostat
```

### `embeddings_precalculados.npz`

Formato NumPy comprimido con:

- **`embeddings`**: Matriz de embeddings (N × 300)
  - N = número de documentos
  - 300 = dimensiones del vector Doc2Vec

- **`metadata`**: Información adicional (opcional)

---

## 🔧 Generación de Embeddings (Opcional)

Si no tienes los embeddings precalculados, puedes generarlos tú mismo:

**⚠️ Advertencia**: Este proceso tarda 2-3 horas

```powershell
cd utils
python save_embeddings.py
```

Ver: `../src/README_TECNICO.md` para más detalles.

---

## 🆘 Problemas Comunes

### ❌ "Archivo no encontrado: noticias.csv"

**Solución**: Verifica que descargaste `noticias.csv` y lo colocaste en la carpeta `data/`

### ❌ "Error al cargar embeddings_precalculados.npz"

**Solución**: 
1. Re-descarga el archivo (puede estar corrupto)
2. Verifica que el tamaño sea ~1 GB
3. Colócalo en `data/`

### ❌ "Los datos están corruptos"

**Solución**: 
1. Elimina los archivos descargados
2. Descarga nuevamente desde el enlace
3. Verifica el hash MD5 (si está disponible)

---

## 📧 Solicitar Acceso a los Datos

Si los enlaces de descarga no funcionan, contacta a:

**Email**: [AGREGAR EMAIL DEL MANTENEDOR]

Incluye en tu mensaje:
- Tu nombre y afiliación
- Propósito del uso de los datos
- Confirmación de que aceptas la licencia de uso

---

## 📜 Licencia de los Datos

Los datos incluidos en este proyecto están sujetos a:

- **Noticias**: [ESPECIFICAR LICENCIA O FUENTE]
- **Embeddings**: Derivados de las noticias, misma licencia

**Restricciones**:
- Solo para uso académico/investigación
- No redistribuir sin permiso
- Citar adecuadamente la fuente

---

## 📊 Estadísticas de los Datos

| Métrica | Valor |
|---------|-------|
| **Total de documentos** | ~50,000 |
| **Período temporal** | 2018-2023 |
| **Idioma** | Español |
| **Dominio** | Noticias económicas |
| **Fuentes principales** | BCE, Eurostat, prensa económica |
| **Tamaño promedio doc** | ~500 palabras |

---

## ⏱️ Tiempo de Descarga Estimado

| Conexión | Tiempo |
|----------|--------|
| Fibra (100 Mbps) | 2-5 minutos |
| ADSL (10 Mbps) | 20-30 minutos |
| Móvil 4G | 10-20 minutos |

---

**Versión**: 1.0  
**Última actualización**: Noviembre 2025
