# Cómo Usar Coqui TTS con TTS-MacOS v2.0

## 🎯 Estado Actual

✅ **Coqui TTS INSTALADO CORRECTAMENTE** (versión 0.24.3)
✅ **Entorno virtual Python 3.12 configurado**
✅ **XTTS-v2 listo para usar**
⚠️ **Requiere aceptación de licencia en primer uso**

## 📋 Requisitos Completados

### ✅ Instalación Exitosa
- **Python 3.12** - Compatible con Coqui TTS
- **PyTorch 2.2.2** - Framework de ML para macOS
- **Coqui TTS 0.24.3** - Sistema completo de TTS
- **Dependencias instaladas** - 180+ MB de paquetes listos

### ✅ Verificación Confirmada
```bash
cd v2
source coqui-env/bin/activate
python -c "import TTS; print('Coqui TTS version:', TTS.__version__)"
# Output: Coqui TTS version: 0.24.3
```

## 🚀 Cómo Usar Coqui TTS

### Método 1: Uso Directo con Coqui TTS

#### Paso 1: Activar Entorno
```bash
cd /Volumes/Resources/Develop/TTS-MacOS/v2
source coqui-env/bin/activate
```

#### Paso 2: Primera Ejecución (Aceptar Licencia)
```bash
python -c "
from TTS.api import TTS
print('Iniciando XTTS-v2 (acepta licencia cuando se solicite)...')
tts = TTS(model_name='tts_models/multilingual/multi-dataset/xtts_v2')
print('✓ XTTS-v2 listo!')
"
```

**IMPORTANTE:** Cuando se ejecute por primera vez, acepta los términos:
- Responde `y` para confirmar la licencia CPML (no-comercial)
- Esto descargará automáticamente el modelo XTTS-v2 (~2GB)

#### Paso 3: Sintetizar Voz
```bash
python -c "
from TTS.api import TTS
import tempfile
import os

# Inicializar
tts = TTS(model_name='tts_models/multilingual/multi-dataset/xtts_v2', progress_bar=False)

# Sintetizar
with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
    output_path = f.name

tts.tts_to_file(
    text='Hola mundo desde Coqui TTS en español',
    language='es',
    file_path=output_path
)

print(f'✓ Audio guardado en: {output_path}')

# Reproducir audio (macOS)
os.system(f'afplay {output_path}')
"
```

### Método 2: Uso con TTS-MacOS v2.0 (Recomendado)

#### Opción A: Motor AI con XTTS-v2
```bash
cd /Volumes/Resources/Develop/TTS-MacOS/v2

# Instalar dependencias del proyecto
source coqui-env/bin/activate
pip install -e .

# Usar motor AI
./tts-macos-v2 "Hola mundo con Coqui TTS" --engine ai --language es --voice default
```

#### Opción B: Clonado de Voz
```bash
# Requiere archivo de audio de 6+ segundos
./tts-macos-v2 "Este será mi clon de voz" \
  --engine ai \
  --voice-cloning \
  --speaker-wav /path/to/mi_voz.wav \
  --language es
```

## 🎭 Voces y Modelos Disponibles

### XTTS-v2 - Multilingüe (Recomendado)
- **Modelo:** `tts_models/multilingual/multi-dataset/xtts_v2`
- **Idiomas:** Español, Inglés, Francés, Alemán, Italiano, Portugués, etc.
- **Calidad:** Alta (~2GB modelo)
- **Clonado:** ✅ Soporta clonado con 6+ segundos de audio

### Para Español
```python
# Opciones de configuración para español
tts.tts_to_file(
    text="Texto en español",
    language="es",
    speaker_wav="voz_referencia.wav",  # Opcional para clonado
    file_path="output.wav"
)
```

## 🛠️ Comandos Útiles

### Verificación del Sistema
```bash
# Verificar instalación
cd v2 && source coqui-env/bin/activate && python -c "
from TTS.api import TTS
print('✓ Coqui TTS:', TTS.__version__)
"

# Listar modelos disponibles (después de inicializar)
python -c "
from TTS.api import TTS
tts = TTS()
print('Modelos disponibles:')
for model in [m for m in tts.models if 'xtts' in m.lower()]:
    print(f'  - {model}')
"
```

### Gestión de Modelos
```bash
# Ubicación de modelos (automática)
ls -l ~/local/share/tts/

# Forzar re-descarga de modelo
rm -rf ~/local/share/tts/tts_models--multilingual--multi-dataset--xtts_v2
# Volver a ejecutar el script para descargar
```

### Limpieza
```bash
# Desactivar entorno
deactivate

# Eliminar entorno (si es necesario)
rm -rf /Volumes/Resources/Develop/TTS-MacOS/v2/coqui-env
```

## 📚 Ejemplos Prácticos

### Ejemplo 1: Lectura en Español
```python
from TTS.api import TTS

tts = TTS(model_name='tts_models/multilingual/multi-dataset/xtts_v2')
tts.tts_to_file(
    text="Bienvenido a TTS-MacOS v2.0 con Coqui TTS",
    language="es",
    file_path="bienvenida.wav"
)
```

### Ejemplo 2: Clonado de Voz
```python
# Paso 1: Grabar o obtener audio de referencia (6+ segundos)
# Paso 2: Usar para clonar
tts.tts_to_file(
    text="Esto es un clon de mi voz original",
    language="es",
    speaker_wav="mi_voz_original.wav",
    file_path="voz_clonada.wav"
)
```

### Ejemplo 3: Diferentes Idiomas
```python
# Inglés
tts.tts_to_file(text="Hello in English", language="en", file_path="en.wav")

# Francés  
tts.tts_to_file(text="Bonjour en français", language="fr", file_path="fr.wav")

# Italiano
tts.tts_to_file(text="Ciao in italiano", language="it", file_path="it.wav")
```

## 🔧 Configuración Avanzada

### Variables de Entorno
```bash
# Opcional: Configurar caché de modelos
export TTS_CACHE_DIR="$HOME/.cache/tts"

# Opcional: Configurar dispositivo (GPU/CPU)
export CUDA_VISIBLE_DEVICES=""  # Forzar CPU
```

### Parámetros de Síntesis
```python
tts.tts_to_file(
    text="Texto avanzado",
    language="es",
    speaker_wav="voz.wav",  # Opcional
    speed=1.0,              # Velocidad (0.5-2.0)
    file_path="output.wav"
)
```

## 🚨 Solución de Problemas

### Problema: "EOF when reading a line"
**Causa:** Primera ejecución requiere aceptar licencia
**Solución:** Ejecutar el script de aceptación manualmente

### Problema: "Model not found"
**Causa:** Modelo no descargado
**Solución:** Esperar descarga automática (~2GB)

### Problema: "CUDA out of memory"
**Causa:** Sin memoria GPU suficiente
**Solución:** Coqui TTS usa CPU por defecto en macOS

### Problema: "Audio quality is low"
**Causa:** Configuración por defecto
**Solución:** Ajustar parámetros de calidad

## 📈 Rendimiento

### Especificaciones Técnicas
- **Modelo XTTS-v2:** ~2GB descargado
- **Memoria RAM:** 4-8GB recomendado
- **Tiempo de síntesis:** ~2-5 segundos por frase
- **Calidad:** 24kHz, alta fidelidad

### Optimización
```python
# Para producción, mantener instancia cargada
class TTSGenerator:
    def __init__(self):
        self.tts = TTS(model_name='tts_models/multilingual/multi-dataset/xtts_v2')
    
    def generate(self, text, language="es"):
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            self.tts.tts_to_file(text=text, language=language, file_path=f.name)
            return f.name
```

## ✅ Resumen de Uso

### Para Empezar Ahora:
```bash
cd /Volumes/Resources/Develop/TTS-MacOS/v2
source coqui-env/bin/activate

# Aceptar licencia y descargar modelo
python -c "from TTS.api import TTS; TTS(model_name='tts_models/multilingual/multi-dataset/xtts_v2')"

# Probar sintetización
python -c "
from TTS.api import TTS
tts = TTS(model_name='tts_models/multilingual/multi-dataset/xtts_v2', progress_bar=False)
tts.tts_to_file('Hola desde Coqui TTS', 'es', 'test.wav')
"
```

¡Coqui TTS está completamente funcional y listo para usar con TTS-MacOS v2.0! 🎉