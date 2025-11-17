# TTS-MacOS v2 - Guía de Instalación y Uso

## 🚀 Instalación Rápida (5 minutos)

### 1. Descargar y Configurar
```bash
# Clonar el repositorio
git clone https://github.com/hbuddenberg/TTS-MacOS.git
cd TTS-MacOS/v2

# Ejecutar instalación completa
./install.sh
```

### 2. Instalación Manual (Alternativa)
```bash
# Crear entorno virtual
python3 -m venv venv-v2
source venv-v2/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Crear scripts de lanzamiento
chmod +x tts-macos-v2 mcp-server-v2 install-mcp
```

### 3. Verificar Instalación
```bash
# Test básico del sistema
python -c "from v2.engines import EngineSelector; print('✅ TTS-MacOS v2 listo!')"

# Demostración interactiva
./demo.sh
```

## 🔗 Configuración Claude Desktop (2 minutos)

### Opción 1: Generador JSON (Recomendado)
```bash
# Generar JSON con rutas perfectas
./install-mcp

# Copiar el JSON generado en Claude Desktop config
# Ubicación: ~/Library/Application Support/Claude/claude_desktop_config.json (macOS)
#          ~/.config/claude/claude_desktop_config.json (Linux)
```

### Opción 2: Instalación Automática
```bash
# Instalar automáticamente en Claude Desktop
./install-mcp --install
```

### Opción 3: MCP Configuration Tool
```bash
# Usar herramienta avanzada de configuración
./mcp-config install --v2
./mcp-config detect    # Detectar instalación
./mcp-config test      # Probar configuración
./mcp-config status    # Ver estado
```

## 🎯 Uso Inmediato

### CLI Command Line
```bash
# Síntesis básica con Native Engine
./tts-macos-v2 "Hello world" --engine native

# Síntesis en español
./tts-macos-v2 "Hola mundo" --engine native --voice monica --language es

# Listar voces disponibles
./tts-macos-v2 list-voices --engine native

# Vista previa de voz
./tts-macos-v2 preview-voice monica --language es

# Guardar como archivo de audio
./tts-macos-v2 "Save this text" --output hello.wav

# Procesamiento batch
./tts-macos-v2 batch *.txt --output-dir ./audio/

# Modo compatible con v1.x
./tts-macos-v2 legacy "text" --voice monica
```

### MCP Tools en Claude Desktop
```python
# Después de configurar MCP en Claude Desktop:

# 1. Síntesis básica
tts_speak(text="Hello world", engine="auto", voice="monica", language="es")

# 2. Síntesis con parámetros avanzados
tts_speak(
    text="Texto en español", 
    engine="native", 
    voice="monica", 
    language="es",
    rate=1.2, 
    volume=1.0
)

# 3. Listar voces disponibles
tts_list_voices(engine="native", language="es", include_clones=True)

# 4. Guardar audio
tts_save(
    text="Save this audio file",
    filename="test_output",
    format="wav",
    engine="native"
)

# 5. Vista previa de voz
tts_preview(voice="monica", language="es", sample_text="Testing voice preview")

# 6. Información del sistema
tts_info()
```

## 🌍 Multi-Language Support

### Vozes en Español
```bash
# Vozes españolas disponibles
./tts-macos-v2 list-voices --engine native | grep "Español"

# Uso directo
./tts-macos-v2 "Hola desde España" --engine native --voice monica
./tts-macos-v2 "Hola desde México" --engine native --voice paulina
```

### Otros Idiomas
```bash
# Francés
./tts-macos-v2 "Bonjour le monde" --engine native --voice aurelie

# Alemán  
./tts-macos-v2 "Hallo Welt" --engine native --voice anna

# Italiano
./tts-macos-v2 "Ciao mondo" --engine native --voice paola
```

## 📊 Advanced Features

### Voice Quality and Parameters
```bash
# Control de velocidad (100-300 WPM)
./tts-macos-v2 "Fast speech" --engine native --rate 200
./tts-macos-v2 "Slow speech" --engine native --rate 100

# Control de volumen
./tts-macos-v2 "Volume test" --engine native --volume 1.5

# Calidad de audio
./tts-macos-v2 "Premium quality" --engine native --quality premium
./tts-macos-v2 "Fast processing" --engine native --quality fast
```

### Batch Processing
```bash
# Procesar múltiples archivos
./tts-macos-v2 batch speech1.txt speech2.txt --output-dir ./audio/

# Con formato específico
./tts-macos-v2 batch *.txt --output-dir ./audio/ --format wav

# Con voz específica
./tts-macos-v2 batch *.txt --voice monica --language es
```

### Configuration Management
```bash
# Ver configuración actual
./tts-macos-v2 config --show

# Establecer configuración
./tts-macos-v2 config --set default_engine=native
./tts-macos-v2 config --set default_language=es

# Resetear a defaults
./tts-macos-v2 config --reset

# Limpiar caché
./tts-macos-v2 config --clear-cache
```

## 🎛️ MCP Configuration

### Configuración JSON para Claude Desktop
```json
{
  "mcpServers": {
    "tts-macos-v2": {
      "command": "/path/to/venv/bin/python",
      "args": ["/path/to/mcp_server_v2.py"],
      "env": {
        "PYTHONPATH": "/path/to/TTS-MacOS/v2"
      }
    }
  }
}
```

### Rutas Absolutas (generadas por ./install-mcp)
```bash
# Ejecutar el generador
./install-mcp

# Salida JSON con rutas resueltas:
{
  "mcpServers": {
    "tts-macos-v2": {
      "command": "/Users/user/TTS-MacOS/v2/venv-v2/bin/python",
      "args": ["/Users/user/TTS-MacOS/v2/mcp_server_v2.py"],
      "env": {
        "PYTHONPATH": "/Users/user/TTS-MacOS/v2"
      }
    }
  }
}
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Python Compatibility
```bash
# Verificar versión de Python
python --version
# Expected: Python 3.9-3.13 for AI features
# Current: Python 3.14 (Native Engine works perfectly)

# Si necesitas AI features, crea venv con Python compatible
python3.12 -m venv venv-ai
source venv-ai/bin/activate
pip install coqui-tts
```

#### 2. MCP Configuration
```bash
# Detectar instalación Claude Desktop
./mcp-config detect

# Probar configuración MCP
./mcp-config test

# Ver estado completo
./mcp-config status
```

#### 3. Voice Issues
```bash
# Listar voces nativas
./tts-macos-v2 list-voices --engine native

# Probar voz específica
./tts-macos-v2 preview-voice monica

# Usar voz por defecto
./tts-macos-v2 "test" --engine native
```

#### 4. Installation Issues
```bash
# Reinstalar completamente
./install.sh --non-interactive

# Verificar dependencias
python -c "import sys; print('Python:', sys.version)"
```

### Testing and Validation

#### Test CLI Functionality
```bash
# Test básico del CLI
./tts-macos-v2 "Testing TTS-MacOS v2" --engine native

# Test all major features
./demo.sh

# Test voice system
./tts-macos-v2 list-voices --engine native
./tts-macos-v2 preview-voice monica
```

#### Test MCP Integration
```bash
# Test MCP configuration
./mcp-config detect
./mcp-config test

# Test MCP tools (después de configurar Claude Desktop)
# En Claude Desktop:
# "List available tools"
# "tts_speak(text='Test message')"
```

#### Test Cross-Platform
```bash
# En macOS
say -v ? | head -5

# En Linux  
espeak-ng --voices | head -5

# Verificar detector de voces
./tts-macos-v2 list-voices --compact
```

## 🚀 Performance Tips

### Optimize for Speed
```bash
# Usar Native Engine para máxima velocidad
./tts-macos-v2 "Fast text" --engine native --quality fast

# Procesamiento batch eficiente
./tts-macos-v2 batch *.txt --engine native --quality fast
```

### Optimize for Quality
```bash
# Usar voces Enhanced/Premium si disponibles
./tts-macos-v2 list-voices | grep -i premium

# Ajustar parámetros para calidad
./tts-macos-v2 "High quality speech" --engine native --rate 160 --volume 1.2
```

### Memory Management
```bash
# Limpiar caché si hay problemas
./tts-macos-v2 config --clear-cache

# Usar formato WAV para mejor calidad (mayor tamaño)
./tts-macos-v2 "test" --output high_quality.wav

# Usar formatos comprimidos para menor tamaño
./tts-macos-v2 "test" --output small_file.wav
```

## 📚 Documentation

### Archivos de Referencia
- `README.md` - Documentación completa
- `MIGRATION.md` - Guía de migración desde v1.x
- `MCP-CONFIGURATION.md` - Guía de configuración MCP
- `USAGE-GUIDE.md` - Esta guía de uso
- `STATUS-AND-MODELS.md` - Estado de los modelos

### Comandos de Ayuda
```bash
# Ayuda principal del CLI
./tts-macos-v2 --help

# Ayuda de configuración MCP
./mcp-config --help

# Demostración interactiva
./demo.sh
```

## 🎯 Success Indicators

### ✅ Installation Successful
- Todos los tests del demo.sh pasan
- MCP tools disponibles en Claude Desktop
- Síntesis de voz funcional
- Lista de voces funcionando

### ✅ Advanced Features Working
- Procesamiento batch funcional
- Gestión de configuración operativa
- Multi-language sintetizando correctamente
- Archivos de audio generándose correctamente

### ✅ Integration Complete
- Claude Desktop respondiendo a commands MCP
- Configuración JSON funcionando
- Sincronización entre CLI y MCP perfecta

🎤✨ **¡TTS-MacOS v2 está listo para uso productivo inmediato!** ✨🎤