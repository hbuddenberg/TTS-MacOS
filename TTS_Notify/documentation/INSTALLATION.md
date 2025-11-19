# Guía de Instalación - TTS Notify

Esta guía cubre todos los métodos de instalación para TTS Notify v1.5.0.

## Requisitos Previos

### Sistema Operativo
- **macOS 10.14 (Mojave) o superior** - Requerido para comando `say`

### Python
- **Python 3.10 o superior** - Para servidor MCP y CLI
- **pip** - Gestor de paquetes de Python
- **UV (opcional)** - Para modo UVX

### Herramientas Opcionales
- **Claude Desktop** - Para integración MCP
- **Git** - Para clonar repositorio

## Método 1: UVX (Recomendado para Desarrollo)

UVX permite ejecutar TTS Notify sin instalación permanente.

### Instalar UV

```bash
# Usar Homebrew (recomendado)
brew install uv

# O instalar manualmente
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Usar TTS Notify con UVX

```bash
# Ejecución directa
uvx --from TTS_Notify tts-notify "Hola mundo"

# Listar voces
uvx --from TTS_Notify tts-notify --list

# Con parámetros
uvx --from TTS_Notify tts-notify --voice Jorge --rate 200 "Texto personalizado"

# Guardar audio
uvx --from TTS_Notify tts-notify --save mi_audio "Mensaje guardado"
```

**Ventajas:**
- Sin instalación permanente
- Siempre usa la última versión
- Aislado del sistema Python
- Ideal para pruebas y desarrollo

## Método 2: Instalación Global via pip

### Desde PyPI (cuando esté disponible)

```bash
pip install tts-notify
```

### Desde Código Fuente

```bash
# Clonar repositorio
git clone <repository-url>
cd TTS_Notify

# Instalar en modo desarrollo
pip install -e .

# O instalar permanentemente
pip install .
```

### Verificar Instalación

```bash
# Verificar comando disponible
tts-notify --version

# Probar funcionamiento básico
tts-notify "Instalación exitosa"

# Listar voces del sistema
tts-notify --list
```

## Método 3: Servidor MCP

El servidor MCP permite integración con Claude Desktop.

### Instalación Automática

```bash
# Clonar repositorio
git clone <repository-url>
cd TTS_Notify

# Ejecutar instalador
./installers/install-mcp.sh
```

### Instalación Manual

```bash
# 1. Crear entorno virtual
python3 -m venv tts-notify-env
source tts-notify-env/bin/activate

# 2. Instalar dependencias MCP
pip install mcp>=1.0.0

# 3. Configurar Claude Desktop
mkdir -p ~/Library/Application\ Support/Claude/
```

Editar `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "tts-notify": {
      "command": "/path/to/TTS_Notify/tts-notify-env/bin/python",
      "args": ["/path/to/TTS_Notify/src/mcp_server.py"]
    }
  }
}
```

### Verificar Instalación MCP

1. **Reiniciar Claude Desktop** completamente (Cmd+Q)
2. **Probar en Claude**: "Lee en voz alta: Hola mundo"
3. **Verificar logs** si hay problemas

## Método 4: Desarrollo Local

### Configurar Entorno

```bash
# Clonar repositorio
git clone <repository-url>
cd TTS_Notify

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
pip install -e .
```

### Ejecutar en Modo Desarrollo

```bash
# Como módulo
python -m src "Mensaje de prueba"

# Directamente
python src/cli.py "Mensaje de prueba"

# Servidor MCP
python src/mcp_server.py
```

## Configuración Post-Instalación

### Variables de Entorno

Agregar a `~/.zshrc` o `~/.bash_profile`:

```bash
# Configuración TTS Notify
export TTS_DEFAULT_VOICE="Monica"
export TTS_DEFAULT_RATE="175"
export TTS_OUTPUT_DIR="$HOME/Desktop"

# Para Claude Code hooks (opcional)
export TTS_ENABLED=true
export TTS_VOICE="monica"
export TTS_RATE=175
```

### Instalar Voces Adicionales

Si faltan voces en español:

```bash
# Abrir preferencias del sistema
open "x-apple.systempreferences:com.apple.preference.speech?Synthesizing"

# O vía terminal
sudo softwareupdate --install-list --all
```

## Verificación de Sistema

### Comprobar Comando say

```bash
# Verificar comando say funciona
say -v ? | head -5

# Probar voz específica
say -v Monica "Prueba de voz"

# Listar voces en español
say -v ? | grep -i spanish
```

### Comprobar Python

```bash
# Verificar versión
python3 --version

# Verificar pip
pip3 --version

# Probar detección de voces
python3 -c "
from src.cli import obtener_voces_sistema
voces = obtener_voces_sistema(solo_espanol=True)
print(f'Voces españolas detectadas: {len(voces)}')
"
```

## Solución de Problemas

### Problema: Comando no encontrado

```bash
# Verificar instalación
which tts-notify

# Si no existe, agregar al PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### Problema: Voces no detectadas

```bash
# Verificar voces del sistema
say -v ? | wc -l

# Listar voces españolas
say -v ? | grep -i -E "(spanish|español)"

# Reiniciar sistema si faltan voces
sudo reboot
```

### Problema: MCP Server no conecta

1. **Verificar rutas absolutas** en configuración
2. **Activar entorno virtual** correctamente
3. **Reiniciar Claude Desktop** completamente
4. **Verificar logs** en `~/Library/Logs/Claude/`

### Problema: Permisos

```bash
# Dar permisos ejecutables
chmod +x installers/install-*.sh

# Verificar permisos de Python
which python3
python3 -c "import sys; print(sys.executable)"
```

## Actualización

### Desde UVX
UVX siempre usa la última versión automáticamente.

### Desde pip
```bash
pip install --upgrade tts-notify
```

### Desde código fuente
```bash
git pull origin main
pip install -e .
```

## Desinstalación

### Quitar instalación global
```bash
pip uninstall tts-notify
```

### Quitar configuración MCP
1. Eliminar entrada de `claude_desktop_config.json`
2. Eliminar entorno virtual: `rm -rf tts-notify-env`
3. Reiniciar Claude Desktop

### Quitar variables de entorno
Editar `~/.zshrc` o `~/.bash_profile` y eliminar líneas agregadas.

## Siguiente Paso

Una vez instalado, consulta [USAGE.md](USAGE.md) para ejemplos avanzados de uso.