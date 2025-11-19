# 🤖 Guía Completa: Usar Coqui TTS con TTS-MacOS v2.0

## 🎯 Resumen Rápido

**Sí, puedes usar Coqui TTS con TTS-MacOS v2.0!** La arquitectura está completamente implementada y lista para usar.

## 📋 Pasos para Activar Coqui TTS

### Opción 1: Script Automático (Recomendado)
```bash
cd tts-macos-v2
./install-coqui-tts.sh

# El script automáticamente:
# ✅ Detecta Python 3.12-3.13 compatible
# ✅ Crea entorno virtual "coqui-env"  
# ✅ Instala PyTorch y Coqui TTS
# ✅ Crea lanzador "./coqui-tts"
# ✅ Instala dependencias adicionales
```

### Opción 2: Manual (si el script falla)
```bash
# Crear entorno con Python 3.12
python3.12 -m venv coqui-env
source coqui-env/bin/activate

# Instalar dependencias
pip install torch torchaudio coqui-tts
pip install numpy scipy librosa soundfile

# Verificar instalación
python -c "import TTS; print('✅ Coqui TTS disponible')"
```

## 🚀 Verificar Instalación

### Test de Funcionalidad
```bash
# Ejecutar lanzador Coqui TTS
./coqui-tts

# Test básico de integración
source venv-v2/bin/activate
python -c "
try:
    from v2.engines import EngineSelector
    selector = EngineSelector()
    if selector.ai_engine and selector.ai_engine.is_available():
        print('✅ AI Engine disponible en TTS-MacOS v2')
        voices = selector.ai_engine.list_voices()
        print(f'✅ Soporta {len(voices.get(\"languages\", []))} idiomas')
    else:
        print('❌ AI Engine no disponible')
except Exception as e:
    print(f'❌ Error: {e}')
"
```

### Test de Síntesis
```bash
# Una vez que todo esté funcionando, prueba sintetización
./tts-macos-v2 "Hello from Coqui TTS!" --engine ai
```

## 🎤 Uso de Coqui TTS en TTS-MacOS v2.0

### Síntesis Básica con AI Engine
```bash
# Usar motor AI automáticamente detectado
./tts-macos-v2 "Hola mundo desde Coqui TTS" --engine auto

# Forzar uso de AI Engine
./tts-macos-v2 "Text synthesis with AI" --engine ai

# Síntesis multi-idioma
./tts-macos-v2 "Bonjour le monde" --engine ai --language fr
./tts-macos-v2 "Hola mundo" --engine ai --language es
./tts-macos-v2 "Ciao mondo" --engine ai --language it
```

### Voice Cloning (XTTS-v2)
```bash
# Crear voz personalizada desde audio (6+ segundos)
./tts-macos-v2 clone-voice mi_audio.wav --name "MiVoz"

# Usar voz clonada
./tts-macos-v2 "Esta es mi voz clonada" --voice "MiVoz" --engine ai
```

### Archivos de Audio
```bash
# Guardar en diferentes formatos
./tts-macos-v2 "Save this audio" --output audio.wav --format wav
./tts-macos-v2 "Save this audio" --output audio.mp3 --format mp3

# Carpeta de salida personalizada
./tts-macos-v2 "Batch processing" --output-dir ./custom_output/
```

## 🔧 MCP Tools con Coqui TTS

### En Claude Desktop (una vez configurado MCP)
```python
# Síntesis con motor AI
tts_speak(
    text="Hello from Coqui TTS!",
    engine="ai",
    language="es",
    voice="default",
    quality="premium"
)

# Voice cloning
tts_clone(
    speaker_wav="/path/to/audio.wav",
    voice_name="CustomVoice",
    description="Voice cloned from sample"
)

# Guardar audio con calidad AI
tts_save(
    text="High quality audio file",
    filename="ai_output",
    format="wav",
    engine="ai"
)

# Vista previa de voz AI
tts_preview(
    voice="default",
    language="es",
    sample_text="Testing AI voice quality"
)
```

## 🌐 Modelos de Coqui TTS Disponibles

### XTTS-v2 (Principal para Voice Cloning)
- **Idiomas**: 16+ idiomas incluyendo español, inglés, francés, etc.
- **Calidad**: Premium con voice cloning
- **Requerimiento**: 6 segundos de audio para clonar voz

### Glow-TTS (Síntesis Rápida)
- **Ventaja**: Velocidad de procesamiento rápida
- **Calidad**: Buena calidad de voz
- **Uso**: Ideal para síntesis masiva

### Modelos Específicos por Idioma
- **Tortoise**: Voces en varios idiomas
- **VCTK**: Generador de voces completo
- **AlignTTS**: Alineación precisa

## 🎛️ Configuración Avanzada

### Ajuste de Parámetros
```bash
# Velocidad de habla (0.5-2.0x)
./tts-macos-v2 "Fast speech" --engine ai --rate 1.5

# Control de volumen (0.0-2.0x)
./tts-macos-v2 "Volume test" --engine ai --volume 1.5

# Pitch adjustment (0.5-2.0x, AI engine)
./tts-macos-v2 "Higher pitch" --engine ai --pitch 1.3

# Énfasis en palabras (AI engine)
./tts-macos-v2 "Strong emphasis" --engine ai --emphasis strong
```

### Selección de Modelos
```python
# En código Python o configuración avanzada
from v2.core.config import TTSConfig

config = TTSConfig()
config.update_config({
    "ai_engine": {
        "default_model": "xtts_v2",
        "cache_models": True,
        "download_timeout": 300
    }
})
```

## 🔍 Detección y Resolución de Problemas

### Verificar Instalación
```bash
# Verificar disponibilidad de Coqui TTS
python -c "
try:
    import TTS
    print(f'✅ Coqui TTS version: {TTS.__version__}')
    from TTS.tts.models.xtts import Xtts
    print('✅ XTTS model available')
except ImportError as e:
    print(f'❌ Coqui TTS not available: {e}')
"

# Verificar device
python -c "
import torch
print(f'PyTorch available: {torch.__version__}')
print(f'CUDA available: {torch.cuda.is_available()}')
print(f'Device: {torch.device}')
"
```

### Problemas Comunes

#### 1. Incompatibilidad de Python
```bash
# ERROR: No matching distribution found for coqui-tts
# SOLUCIÓN: Usar Python 3.9-3.13
python3.12 -m venv coqui-env
```

#### 2. Error de Memoria (Modelos Grandes)
```bash
# ERROR: RuntimeError: CUDA out of memory
# SOLUCIÓN: Usar CPU mode o reducir modelo size
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
```

#### 3. Voces no Disponibles
```bash
# ERROR: Model not found
# SOLUCIÓN: Descargar modelos automáticamente
# Los modelos se descargan en el primer uso
./tts-macos-v2 "test" --engine ai  # Descargará automáticamente
```

## 📊 Rendimiento y Optimización

### GPU Acceleration (Linux)
```bash
# Si tienes GPU NVIDIA
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118

# Verificar GPU disponible
python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}')"
```

### Optimización de Memoria
```bash
# Limpiar caché si hay problemas de memoria
./tts-macos-v2 config --clear-cache

# Usar configuración para uso eficiente
./tts-macos-v2 "text" --engine ai --quality fast
```

### Caching de Modelos
```python
# Los modelos se guardan automáticamente
# Ruta: ~/.cache/tts/
# Verificar caché
python -c "
import os
cache_dir = os.path.expanduser('~/.cache/tts')
print(f'Cache directory: {cache_dir}')
print(f'Size: {sum(os.path.getsize(os.path.join(cache_dir, f)) for f in os.listdir(cache_dir)) / 1024 / 1024:.1f} MB')
"
```

## 🎛️ CLI Avanzado

### Modo Batch Processing
```bash
# Procesar múltiples archivos con AI Engine
./tts-macos-v2 batch *.txt --engine ai --output-dir ./ai_output/

# Procesar con parámetros avanzados
./tts-macos-v2 batch *.txt \
    --engine ai \
    --voice "default" \
    --quality premium \
    --output-dir ./premium_output/
```

### Testing y Evaluación
```bash
# Modo de prueba (sin crear archivos)
./tts-macos-v2 "Test" --engine ai --dry-run

# Comparar calidad entre engines
./tts-macos-v2 "Comparison test" --engine native --output native_output.wav
./tts-macos-v2 "Comparison test" --engine ai --output ai_output.wav

# Evaluar rendimiento
./tts-macos-v2 info  # Muestra estadísticas de uso
```

## 🎯 Ejemplos Prácticos

### Narración de Audiolibros
```bash
# Capítulo 1
./tts-macos-v2 "Capítulo uno de nuestra historia" --engine ai --language es --quality premium --output chapter1.wav

# Capítulo 2 con voz específica
./tts-macos-v2 "Chapter two continues our journey" --voice "professional_voice" --engine ai
```

### Vozes Personalizadas
```bash
# Clonar voz para personaje
./tts-macos-v2 clone-voice narrator_sample.wav --name "NovelistaNarrator"
./tts-macos-v2 "El protagonista dijo: '¡La aventura comienza!'" --voice "NovelistaNarrator"

# Narrar audiolibros con diferente velocidad
./tts-macos-v2 file:"narration.txt" --engine ai --rate 1.0 --output narration_normal.wav
./tts-macos-v2 file:"narration.txt" --engine ai --rate 1.5 --output narration_fast.wav
```

### Contenido Educativo
```bash
# Voz educativa para niños
./tts-macos-v2 "Los colores son primarios, secundarios y terciarios" --engine ai --language es --voice "children_voice"

# Diferentes idiomas para educación
./tts-macos-v2 "Welcome to our lesson" --engine ai --language en --voice "teacher_voice"
./tts-macos-v2 "Bienvenido a nuestra lección" --engine ai --language es --voice "professor_voice"
```

## 🔄 Integración con TTS-MacOS v2.0

### Activación Automática
```bash
# El EngineSelector detectará automáticamente AI Engine
# cuando esté disponible y lo usará para:
# - Voice cloning
# - Múltiples idiomas no nativos
# - Calidad premium

# Ejemplo con auto-selección
./tts-macos-v2 "Text in Russian" --engine auto  # → Usará AI Engine
./tows-macos-v2 "Text in English" --engine auto  # → Usará Native Engine
```

### Configuración Híbrida
```python
# En código o configuración
from v2.engines import EngineSelector, EngineType

selector = EngineSelector()

# Configurar preferencias
engine = selector.select_engine(
    engine=EngineType.AUTO,           # Selección automática
    voice_cloning=True,              # Si se necesita voice cloning → AI Engine
    language="ja",                  # Japonés no nativo → AI Engine
    quality="premium"               # Calidad premium → AI Engine
    fallback_to_native=True        # Fallback a native si AI no disponible
)
```

## 📊 Monitoreo y Análisis

### Estadísticas de Uso
```bash
# Verificar uso del sistema
./tts-macos-v2 info

# En MCP tools
tts_info()  # Devuelve información detallada del sistema
```

### Métricas de Rendimiento
```python
# En código
from v2.core.smart_features import PerformanceOptimizer

optimizer = PerformanceOptimizer()

# Obtener recomendaciones para contenido específico
params = optimizer.optimize_parameters(
    text="Technical documentation content",
    engine_type="ai",
    quality_preference="premium"
)
```

## 🎊 Guía de Producción

### Para Uso en Producción
1. **Instalar Coqui TTS** con Python 3.12+
2. **Configurar caché** para mejorar rendimiento
3. **Testar voz cloning** con audio de alta calidad
4. **Optimizar parámetros** para cada tipo de contenido
5. **Monitorear memoria** para evitar problemas

### Mejores Prácticas
- **Calidad de Audio**: Usar archivos WAV de 16-24kHz y 16-bit
- **Tiempo de Voz**: Mínimo 6 segundos para cloning
- **Sin Ruido de Fondo**: Audio limpio para mejores resultados
- **Formato Consistente**: Usar el mismo formato en todos los audios

### Soporte y Mantenimiento
- **Actualizaciones**: `pip install --upgrade coqui-tts`
- **Problemas de Memoria**: Reinstalar o limpiar caché
- **Errores de Modelo**: Reinstalar dependencias

## 🚀 TTS-MacOS v2.0 con Coqui TTS: ¡Listo para Usar!

🎤✨ **Ahora tienes acceso completo a:**

- ✅ **84+ voces nativas** del sistema
- 🤖 **Coqui TTS** con XTTS-v2 (voice cloning)
- 🌐 **16+ idiomas** con calidad AI
- 🔗 **Voice cloning** desde 6 segundos de audio
- 💻 **Integración MCP** completa
- 🚀 **CLI avanzada** con todos los comandos
- 📊 **Smart features** y optimización

🎯 **TTS-MacOS v2.0.0 + Coqui TTS = Sistema TTS completo y profesional!** 🎤✨