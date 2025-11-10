# 🎙️ TTS-macOS - Text-to-Speech para macOS

Herramienta versátil de Text-to-Speech que funciona de **tres formas**:

1. **🚀 uvx** - Ejecución directa sin instalación (como `npx`)
2. **🎤 CLI Tool** - Comando instalado globalmente
3. **🤖 Servidor MCP** - Para integrar con Claude Desktop

Todos usan el TTS nativo de macOS. **100% gratuito y offline.**

## ✨ Características

- 🗣️ **84+ voces** detectadas automáticamente en tu sistema
  - 16 voces básicas en español (España, México)
  - 12 voces Enhanced/Premium en español (España, México, Argentina, Chile, Colombia)
  - Soporte para voces Siri (cuando estén instaladas)
  - Todas las voces del sistema (inglés, francés, italiano, etc.)
- 🔍 **Búsqueda flexible**: usa nombres parciales o sin acentos
  - `monica` → Mónica
  - `angelica` → Angélica (Enhanced)
  - `siri` → Siri Female
- ⚡ **Velocidad ajustable** (100-300 palabras por minuto)
- 💾 **Guardar audio** en archivos AIFF
- 🆓 **Completamente gratuito** (usa TTS nativo de macOS)
- 🚀 **Tres modos de uso**: uvx, CLI y servidor MCP
- 📦 **Sin dependencias** (TTS nativo)

## 📋 Requisitos

- macOS (cualquier versión reciente)
- Python 3.10 o superior
- [uv](https://github.com/astral-sh/uv) (para usar con uvx - recomendado)
- Claude Desktop (solo para modo servidor MCP)

## 🚀 Inicio Rápido

### Opción A: Usar con uvx (Recomendado - como npx) 🆕

```bash
# Instalar uv (una sola vez)
brew install uv
# o: curl -LsSf https://astral.sh/uv/install.sh | sh

cd mcp-tts-macos

# Ver todas las voces disponibles
uvx --from . tts-macos --list

# Usar directamente (sin instalar)
uvx --from . tts-macos "Hola mundo"
uvx --from . tts-macos "Buenos días" --voice Jorge --rate 200
uvx --from . tts-macos "Calidad superior" --voice "Mónica (Enhanced)"
uvx --from . tts-macos "Guardar" --save audio.aiff

# Crear alias para uso frecuente
alias tts='uvx --from /ruta/completa/al/proyecto/mcp-tts-macos tts-macos'
tts "Ahora es más fácil"
tts --list

# Ver ayuda
uvx --from . tts-macos --help
```

📖 **Ventajas de uvx**: Sin instalación, sin conflictos de versiones, siempre actualizado

### ⚠️ Importante: Uso de `--refresh` con uvx

Cuando uses uvx después de instalar o modificar el proyecto:

```bash
# PRIMERA VEZ después de cambios o instalación
uvx --from . --refresh tts-macos --list --gen female

# Después del refresh, usa normal
uvx --from . tts-macos --list --gen female
uvx --from . tts-macos --list --gen male --lang es_ES
uvx --from . tts-macos "Hola mundo" --voice Monica
```

**¿Cuándo usar `--refresh`?**
- Después de instalar el proyecto por primera vez
- Después de modificar el código fuente del CLI
- Después de actualizar las opciones o argumentos
- Cuando veas errores como "unrecognized arguments"

**Para el uso diario**: Una vez que hayas hecho `--refresh` al menos una vez, puedes usar uvx normal sin problemas.

### Opción B: Instalar como CLI global

```bash
cd mcp-tts-macos

# Instalar comando global
./install-cli.sh

# Usar desde cualquier lugar
tts-macos "Hola mundo"
tts-macos "Buenos días" --voice jorge --rate 200
```

📖 **[Ver guía completa CLI](CLI-GUIDE.md)**

### Opción C: Usar como servidor MCP con Claude

```bash
cd mcp-tts-macos

# Instalar servidor MCP
./install.sh

# Reiniciar Claude Desktop
# Luego en Claude: "Lee en voz alta: Hola mundo"
```

📖 **Continúa leyendo para configuración MCP completa**

### 1. Clonar o descargar el proyecto

```bash
cd ~/Documents
# Si tienes el proyecto descargado, entra a su carpeta
cd mcp-tts-macos
```

### 2. Crear entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Probar el servidor

```bash
python server.py
```

Si todo está bien, el servidor quedará esperando conexiones MCP.

## ⚙️ Configuración en Claude Desktop

### 1. Localizar el archivo de configuración

Abre la terminal y ejecuta:

```bash
open ~/Library/Application\ Support/Claude/
```

### 2. Editar claude_desktop_config.json

Si el archivo no existe, créalo. Debe contener:

```json
{
  "mcpServers": {
    "tts-macos": {
      "command": "/Users/TU_USUARIO/Documents/mcp-tts-macos/venv/bin/python",
      "args": [
        "/Users/TU_USUARIO/Documents/mcp-tts-macos/server.py"
      ]
    }
  }
}
```

**⚠️ IMPORTANTE:** Reemplaza `TU_USUARIO` con tu nombre de usuario de macOS.

Para saber tu usuario, ejecuta en terminal:
```bash
whoami
```

### 3. Reiniciar Claude Desktop

Cierra completamente Claude Desktop y vuelve a abrirlo.

### 4. Verificar instalación

En Claude Desktop, deberías ver un ícono de herramientas (🔧) o una indicación de que el servidor MCP está conectado.

## 📖 Uso

### 🎤 Reproducir texto con voz

Simplemente pídele a Claude:

```
"Lee este texto en voz alta: Hola, este es un ejemplo de texto a voz"
```

```
"Reproduce este mensaje con la voz de Jorge"
```

### 🎭 Cambiar voces

Para ver **todas las voces** disponibles:

```bash
# Con uvx
uvx --from . tts-macos --list

# Con CLI instalado
tts-macos --list
```

**Voces destacadas en Español:**

📦 **Básicas (16 voces):**
- Eddy, Flo, Grandma, Grandpa, Reed, Rocko, Sandy, Shelley (España y México)

⭐ **Enhanced/Premium (12 voces):**
- **Mónica** (España) - Calidad mejorada
- **Angélica** (México) - Calidad mejorada
- **Jorge** (España) - Voz masculina natural
- **Paulina** (México) - Voz femenina clara
- **Juan** (México) - Voz masculina profesional
- **Diego** (Argentina) - Acento argentino
- **Carlos** (Colombia) - Acento colombiano
- **Francisca** (Chile) - Acento chileno
- **Isabela** (Argentina) - Voz femenina argentina
- **Marisol** (España) - Incluye versión Premium
- **Soledad** (Colombia) - Acento colombiano
- **Jimena** (Colombia) - Voz femenina colombiana

🤖 **Siri:**
- ⚠️ **Limitación importante**: Las voces de Siri NO son accesibles con el comando `say -v`
- Las voces de Siri solo funcionan como voz del sistema (sin especificar voz)
- **Alternativa recomendada**: Usa voces Enhanced/Premium que ofrecen calidad similar
- 📖 **[Ver guía completa sobre voces de Siri](SIRI-VOICES-GUIDE.md)**

💡 **Total: 84+ voces** detectadas automáticamente en tu sistema (excluyendo Siri por limitaciones técnicas)

### ⚡ Ajustar velocidad

```
"Lee esto más rápido: [tu texto]"
"Velocidad 200 palabras por minuto: [tu texto]"
```

Rango: 100-300 palabras por minuto (default: 175)

### 💾 Guardar audio en archivo

```
"Guarda este texto como audio en un archivo llamado 'mensaje': Hola mundo"
```

El archivo se guardará en tu **Escritorio** con formato AIFF.

## 🎯 Ejemplos de Uso

### 📦 Modo CLI / uvx

```bash
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# USO BÁSICO
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Ver todas las voces disponibles
uvx --from . tts-macos --list

# Reproducir texto con voz por defecto
uvx --from . tts-macos "Hola mundo"

# Ver ayuda completa
uvx --from . tts-macos --help

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# VOCES ESPECÍFICAS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Voces básicas
uvx --from . tts-macos "Buenos días" --voice Eddy
uvx --from . tts-macos "Buenas tardes" --voice Flo

# Voces Enhanced (mejor calidad)
uvx --from . tts-macos "Calidad superior" --voice "Mónica (Enhanced)"
uvx --from . tts-macos "Voz profesional" --voice "Jorge (Enhanced)"

# Voces con acentos regionales
uvx --from . tts-macos "Acento mexicano" --voice "Angélica (Enhanced)"
uvx --from . tts-macos "Acento argentino" --voice "Diego (Enhanced)"
uvx --from . tts-macos "Acento colombiano" --voice "Carlos (Enhanced)"
uvx --from . tts-macos "Acento chileno" --voice "Francisca (Enhanced)"

# Voces Siri (si están instaladas)
uvx --from . tts-macos "Hola desde Siri" --voice "Siri Female"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# BÚSQUEDA FLEXIBLE (sin acentos ni mayúsculas)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Puedes escribir sin acentos
uvx --from . tts-macos "Hola" --voice monica    # → Mónica (Enhanced)
uvx --from . tts-macos "Hola" --voice angelica  # → Angélica (Enhanced)

# Búsqueda parcial
uvx --from . tts-macos "Hola" --voice siri      # → Siri Female
uvx --from . tts-macos "Hola" --voice franc     # → Francisca (Enhanced)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# VELOCIDAD
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Velocidad normal (por defecto: 175 WPM)
uvx --from . tts-macos "Velocidad normal"

# Más lento (útil para aprender)
uvx --from . tts-macos "Más despacio" --rate 120

# Más rápido
uvx --from . tts-macos "Más rápido" --rate 250

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# GUARDAR AUDIO
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Guardar como archivo AIFF
uvx --from . tts-macos "Guardar este mensaje" --save mensaje.aiff

# Guardar con voz específica
uvx --from . tts-macos "Mensaje importante" --voice "Jorge (Enhanced)" --save importante.aiff

# El archivo se guarda en el Escritorio

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ALIAS (para uso frecuente)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Crear alias permanente (agregar a ~/.zshrc o ~/.bashrc)
alias tts='uvx --from /Volumes/Resources/Develop/TTS-MacOS/mcp-tts-macos tts-macos'

# Usar el alias
tts "Ahora es más fácil"
tts --list
tts "Mensaje" --voice monica
```

### 🤖 Modo Servidor MCP (con Claude Desktop)

### Ejemplo 1: Escuchar una respuesta larga

```
Usuario: "Explícame qué es la inteligencia artificial y luego léemelo"

Claude: [Genera explicación y automáticamente la reproduce con TTS]
```

### Ejemplo 2: Crear un mensaje de voz

```
Usuario: "Escribe un mensaje de cumpleaños para mi madre y guárdalo como audio"

Claude: [Crea mensaje y guarda archivo en el escritorio]
```

### Ejemplo 3: Practicar pronunciación

```
Usuario: "Dame 5 frases en español y reprodúcelas una por una con diferentes voces"

Claude: [Reproduce cada frase con una voz diferente]
```

## 🔧 Solución de Problemas

### El servidor no aparece en Claude Desktop

1. Verifica que las rutas en `claude_desktop_config.json` sean correctas
2. Asegúrate de usar rutas **absolutas** (empezando con `/Users/`)
3. Reinicia Claude Desktop completamente (Cmd+Q)

### Error: "command not found" o "No such file"

Verifica que el entorno virtual esté activado:
```bash
which python
# Debe mostrar: .../mcp-tts-macos/venv/bin/python
```

### No se escucha el audio

1. Verifica el volumen de tu Mac
2. Prueba desde terminal:
```bash
say -v Monica "Hola mundo"
```
3. Si funciona en terminal pero no en el MCP, revisa los logs

### La voz no se encuentra

Algunas voces pueden no estar instaladas. Para instalarlas:
1. Ve a **Preferencias del Sistema** → **Accesibilidad** → **Contenido Hablado**
2. Haz clic en **Voces del Sistema**
3. Descarga las voces en español que necesites

### ¿Por qué no aparecen las voces de Siri?

**Respuesta corta**: Las voces de Siri NO son accesibles con TTS-macOS por limitaciones técnicas de Apple.

**Solución**: Usa voces **Enhanced** o **Premium** que ofrecen calidad similar:

```bash
# En lugar de Siri, usa:
uvx --from . tts-macos "Hola mundo" --voice "Mónica (Enhanced)"
uvx --from . tts-macos "Hola mundo" --voice "Jorge (Enhanced)"
```

📖 **[Lee la guía completa sobre voces de Siri](SIRI-VOICES-GUIDE.md)** para entender las limitaciones técnicas y alternativas.

## 📁 Estructura del Proyecto

```
mcp-tts-macos/
├── server.py              # Servidor MCP principal
├── requirements.txt       # Dependencias Python
├── README.md             # Este archivo
└── venv/                 # Entorno virtual (se crea al instalar)
```

## 🤝 Contribuciones

¿Tienes ideas para mejorar este proyecto? ¡Las contribuciones son bienvenidas!

## 📝 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 🆘 Soporte

Si tienes problemas:
1. Revisa la sección "Solución de Problemas"
2. Verifica que tu versión de macOS sea compatible
3. Asegúrate de tener Python 3.10+

## 🎉 ¡Disfruta!

Ahora puedes escuchar todas las respuestas de Claude en voz alta. ¡Experimenta con diferentes voces y velocidades!

---

**Hecho con ❤️ para la comunidad de Claude y macOS**
