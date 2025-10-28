# 🎙️ TTS-macOS - Text-to-Speech para macOS

Herramienta versátil de Text-to-Speech que funciona de **tres formas**:

1. **🚀 uvx** - Ejecución directa sin instalación (como `npx`)
2. **🎤 CLI Tool** - Comando instalado globalmente
3. **🤖 Servidor MCP** - Para integrar con Claude Desktop

Todos usan el TTS nativo de macOS. **100% gratuito y offline.**

## ✨ Características

- 🗣️ **6 voces en español** (México, España, Argentina)
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

# Usar directamente (sin instalar)
uvx --from . tts-macos "Hola mundo"
uvx --from . tts-macos "Buenos días" --voice jorge --rate 200
uvx --from . tts-macos "Guardar" --save audio.aiff

# Crear alias para uso frecuente
alias tts='uvx --from ~/mcp-tts-macos tts-macos'
tts "Ahora es más fácil"
```

📖 **[Ver guía completa uvx](UVX-GUIDE.md)**

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

```
"Lista las voces disponibles"
```

Voces disponibles:
- **monica**: Español Mexicano (Mujer) - Por defecto
- **paulina**: Español Mexicano (Mujer)
- **jorge**: Español España (Hombre)
- **juan**: Español España (Hombre)
- **diego**: Español Argentino (Hombre)
- **angelica**: Español México (Mujer)

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
