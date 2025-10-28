# 🎙️ Servidor MCP Text-to-Speech para macOS - PROYECTO COMPLETO

## 📦 ¡Tu proyecto está listo!

He creado un servidor MCP completo que te permite convertir texto a voz usando el TTS nativo de macOS.

---

## 📂 Contenido del Proyecto

El archivo `mcp-tts-macos.tar.gz` contiene:

```
mcp-tts-macos/
├── 📄 server.py                    # Servidor MCP principal
├── 📄 requirements.txt             # Dependencias Python
├── 📄 README.md                    # Documentación completa
├── 📄 QUICKSTART.md                # Guía rápida de inicio
├── 📄 TROUBLESHOOTING.md           # Solución de problemas
├── 📄 CHANGELOG.md                 # Registro de versiones
├── 📄 LICENSE                      # Licencia MIT
├── 🔧 install.sh                   # Instalador automático
├── 🧪 test_tts.py                 # Script de pruebas
├── 📄 claude_desktop_config.example.json  # Ejemplo de configuración
└── 📄 .gitignore                  # Para control de versiones
```

---

## 🚀 Instalación Rápida (5 minutos)

### 1. Descomprimir el proyecto

```bash
# Descargar y descomprimir
cd ~/Documents
tar -xzf mcp-tts-macos.tar.gz
cd mcp-tts-macos
```

### 2. Ejecutar el instalador

```bash
./install.sh
```

El instalador hace TODO automáticamente:
- ✅ Verifica que tengas Python 3
- ✅ Crea el entorno virtual
- ✅ Instala las dependencias
- ✅ Configura Claude Desktop
- ✅ Prueba que todo funcione

### 3. Reiniciar Claude Desktop

1. Cierra Claude completamente (⌘+Q)
2. Abre Claude nuevamente
3. Deberías ver el servidor conectado

### 4. ¡Prueba!

Escribe en Claude:
```
"Lee este texto en voz alta: Hola, este es mi primer mensaje de texto a voz"
```

---

## 🎭 Voces Disponibles

El servidor incluye 6 voces en español:

| Voz | País | Género |
|-----|------|--------|
| monica | México | Mujer |
| paulina | México | Mujer |
| jorge | España | Hombre |
| juan | España | Hombre |
| diego | Argentina | Hombre |
| angelica | México | Mujer |

---

## 💡 Ejemplos de Uso

### Reproducir texto simple
```
"Lee en voz alta: Buenos días, ¿cómo estás?"
```

### Cambiar de voz
```
"Usa la voz de Jorge y lee: Hola desde España"
```

### Ajustar velocidad
```
"Lee esto rápido: [tu texto]"
"Lee esto despacio: [tu texto]"
```

### Guardar audio
```
"Guarda como audio el siguiente texto: [tu mensaje]"
```
El archivo se guardará en tu Escritorio.

### Listar voces
```
"¿Qué voces tienes disponibles?"
"Muéstrame las voces en español"
```

---

## 🔧 Características Principales

### ✨ Funcionalidades

- **3 herramientas MCP:**
  1. `speak_text` - Reproduce texto con voz
  2. `list_voices` - Lista voces disponibles
  3. `save_audio` - Guarda audio en archivo

- **Control total:**
  - Elige entre 6 voces en español
  - Ajusta velocidad (100-300 palabras/min)
  - Guarda audio en formato AIFF
  - Ejecución asíncrona para mejor rendimiento

- **Integración perfecta:**
  - Funciona con Claude Desktop
  - No requiere API keys ni servicios externos
  - 100% gratuito (usa TTS de macOS)

---

## 📖 Documentación

El proyecto incluye documentación completa:

- **README.md**: Guía completa del proyecto
- **QUICKSTART.md**: Para empezar en 2 minutos
- **TROUBLESHOOTING.md**: Solución de problemas comunes

---

## 🆘 ¿Problemas?

### Verifica la instalación
```bash
cd mcp-tts-macos
python3 test_tts.py
```

### Problemas comunes

**No se escucha audio:**
- Verifica el volumen: `osascript -e 'set volume 50'`
- Prueba: `say "Hola mundo"`

**Servidor no aparece en Claude:**
- Reinicia Claude con ⌘+Q
- Verifica el archivo de configuración:
  `~/Library/Application Support/Claude/claude_desktop_config.json`

**Voces no disponibles:**
- Ve a: Preferencias → Accesibilidad → Contenido Hablado
- Descarga las voces en español

### Más ayuda
Consulta `TROUBLESHOOTING.md` para guía detallada.

---

## 🎉 ¡Listo para Usar!

Tu servidor MCP de Text-to-Speech está completo y listo para instalar.

### Próximos pasos:
1. ✅ Descomprimir el proyecto
2. ✅ Ejecutar `./install.sh`
3. ✅ Reiniciar Claude Desktop
4. ✅ ¡Disfrutar de texto a voz!

---

## 📊 Especificaciones Técnicas

- **Lenguaje:** Python 3.10+
- **Protocolo:** MCP (Model Context Protocol)
- **Sistema:** macOS únicamente
- **Dependencias:** mcp (Python package)
- **TTS Engine:** macOS native `say` command
- **Formato audio:** AIFF
- **Licencia:** MIT

---

## 🌟 Ventajas de este Servidor

✅ **Gratuito**: Sin costos de API
✅ **Privado**: Todo local, sin enviar datos
✅ **Rápido**: Latencia mínima
✅ **Fácil**: Instalación en 1 comando
✅ **Completo**: 6 voces profesionales
✅ **Documentado**: Guías detalladas

---

## 💻 Requisitos del Sistema

- macOS 10.14 o superior
- Python 3.10 o superior
- Claude Desktop instalado
- 50 MB de espacio en disco

---

## 🎓 Aprende Más

Para información detallada sobre cómo funciona el servidor MCP,
personalización avanzada, y contribuir al proyecto, consulta
el README.md incluido.

---

**¡Disfruta de tu nuevo servidor Text-to-Speech!** 🎤

_Creado con ❤️ para la comunidad de Claude_
