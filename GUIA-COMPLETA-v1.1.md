# 🎙️ TTS-macOS - Guía Completa

## 📦 Proyecto Actualizado - Versión 1.1.0

¡Ahora con **DOS formas de usar**!

---

## 🎯 Dos Modos de Uso

### 1️⃣ Modo CLI (Comando de Terminal)
**Úsalo como `npx` o cualquier comando de terminal**

```bash
# Ejemplos rápidos
tts-macos "Hola mundo"
tts-macos "Buenos días" --voice jorge
tts-macos "Rápido" --rate 250
tts-macos "Mensaje" --save audio.aiff
```

✅ **Ideal para:**
- Scripts de automatización
- Notificaciones de sistema
- Integración con otros comandos
- Uso programático

### 2️⃣ Modo Servidor MCP (Claude Desktop)
**Integración con tu asistente Claude**

En Claude Desktop:
```
"Lee en voz alta: Hola mundo"
"Usa la voz de Jorge y lee: Buenos días"
"Guarda como audio: Mi mensaje"
```

✅ **Ideal para:**
- Escuchar respuestas de Claude
- Interacción conversacional
- Uso con interfaz gráfica

---

## 🚀 Instalación

### Opción A: Solo CLI (más rápido)

```bash
# 1. Descomprimir
cd ~/Downloads
tar -xzf mcp-tts-macos.tar.gz
cd mcp-tts-macos

# 2. Instalar CLI
./install-cli.sh

# 3. ¡Listo!
tts-macos "Hola mundo"
```

### Opción B: Solo Servidor MCP

```bash
# 1. Descomprimir
cd ~/Downloads
tar -xzf mcp-tts-macos.tar.gz
cd mcp-tts-macos

# 2. Instalar servidor
./install.sh

# 3. Reiniciar Claude Desktop
# 4. ¡Usar en Claude!
```

### Opción C: Ambos (recomendado)

```bash
# 1. Descomprimir
cd ~/Downloads
tar -xzf mcp-tts-macos.tar.gz
cd mcp-tts-macos

# 2. Instalar CLI
./install-cli.sh

# 3. Instalar servidor MCP
./install.sh

# 4. ¡Listo! Ahora tienes ambos
```

---

## 📚 Uso del CLI

### Sintaxis Básica

```bash
tts-macos "texto" [opciones]
```

### Opciones Disponibles

| Opción | Descripción | Ejemplo |
|--------|-------------|---------|
| `-v, --voice` | Selecciona voz | `--voice jorge` |
| `-r, --rate` | Velocidad (100-300) | `--rate 200` |
| `-s, --save` | Guardar audio | `--save audio.aiff` |
| `-l, --list` | Listar voces | `--list` |
| `--help` | Ayuda | `--help` |

### Ejemplos CLI

```bash
# Básico
tts-macos "Hola mundo"

# Con voz
tts-macos "Desde España" --voice jorge

# Con velocidad
tts-macos "Rápido" --rate 250
tts-macos "Lento" --rate 125

# Guardar audio
tts-macos "Guardar esto" --save mensaje.aiff

# Combinar opciones
tts-macos "Todo junto" --voice paulina --rate 200 --save completo.aiff

# Ver voces
tts-macos --list

# Ayuda
tts-macos --help
```

### Integración con Scripts

```bash
#!/bin/bash
# notificacion.sh

function notificar() {
    tts-macos "$1" --voice monica
}

# Uso
notificar "Proceso completado"
```

### Leer archivos

```bash
# Leer archivo completo
tts-macos "$(cat documento.txt)"

# Con pipe
cat archivo.txt | xargs tts-macos --voice jorge
```

---

## 🤖 Uso con Claude Desktop

### Comandos Naturales

En Claude puedes decir:

```
"Lee esto en voz alta: [tu texto]"
"Reproduce este mensaje: [tu texto]"
"Di esto con voz de Jorge: [tu texto]"
"Lee rápido: [tu texto]"
"Lee despacio: [tu texto]"
"Guarda como audio: [tu texto]"
"¿Qué voces tienes?"
"Lista las voces disponibles"
```

### Ejemplos de Conversación

```
Usuario: Explícame qué es la fotosíntesis y luego léemelo

Claude: [Genera explicación]
        [Reproduce automáticamente con voz]

---

Usuario: Escribe un poema y guárdalo como audio

Claude: [Crea poema]
        [Guarda en el escritorio como audio.aiff]
```

---

## 🎭 Voces Disponibles

| Voz | País | Género | Descripción |
|-----|------|--------|-------------|
| **monica** | 🇲🇽 México | Mujer | Por defecto, natural |
| **paulina** | 🇲🇽 México | Mujer | Clara y profesional |
| **jorge** | 🇪🇸 España | Hombre | Castellano claro |
| **juan** | 🇪🇸 España | Hombre | Formal |
| **diego** | 🇦🇷 Argentina | Hombre | Acento rioplatense |
| **angelica** | 🇲🇽 México | Mujer | Juvenil |

---

## 📁 Estructura del Proyecto

```
mcp-tts-macos/
├── 🎤 CLI
│   ├── tts-macos              # Script CLI ejecutable
│   ├── install-cli.sh         # Instalador CLI
│   ├── setup.py               # Setup para pip
│   └── CLI-GUIDE.md           # Guía completa CLI
│
├── 🤖 Servidor MCP
│   ├── server.py              # Servidor MCP
│   ├── install.sh             # Instalador MCP
│   └── requirements.txt       # Dependencias
│
├── 🧪 Testing
│   └── test_tts.py           # Script de pruebas
│
└── 📚 Documentación
    ├── README.md              # Documentación principal
    ├── QUICKSTART.md          # Inicio rápido
    ├── TROUBLESHOOTING.md     # Solución de problemas
    ├── CHANGELOG.md           # Historial de versiones
    └── LICENSE                # Licencia MIT
```

---

## 💡 Casos de Uso

### CLI: Automatización

```bash
# Notificación de backup
./backup.sh && tts-macos "Backup completado"

# Timer Pomodoro
sleep 1500 && tts-macos "Descanso" --voice paulina

# Recordatorio
echo 'tts-macos "Reunión en 5 minutos"' | at now + 5 minutes
```

### MCP: Interacción con Claude

```
# Escuchar resúmenes largos
"Resume este documento y léemelo"

# Crear audio para presentaciones
"Crea un script de introducción y guárdalo como audio"

# Practicar idiomas
"Dame 5 frases en español y reprodúcelas"
```

---

## 🔧 Solución de Problemas

### CLI: Comando no encontrado

```bash
# Verificar instalación
which tts-macos

# Verificar PATH
echo $PATH | grep ".local/bin"

# Reinstalar
cd mcp-tts-macos
./install-cli.sh
```

### MCP: Servidor no aparece en Claude

1. Verificar configuración:
```bash
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

2. Reiniciar Claude (Cmd+Q, no solo cerrar ventana)

3. Verificar logs:
```bash
tail -f ~/Library/Logs/Claude/mcp*.log
```

### Audio no se escucha

```bash
# Verificar volumen
osascript -e 'set volume output volume 50'

# Probar comando say
say -v Monica "Test"

# Probar CLI
tts-macos "Test"
```

---

## 📊 Comparación de Modos

| Característica | CLI | Servidor MCP |
|----------------|-----|--------------|
| Uso en terminal | ✅ | ❌ |
| Integración Claude | ❌ | ✅ |
| Scripts automatización | ✅ | ❌ |
| Interfaz conversacional | ❌ | ✅ |
| Guardar archivos | ✅ | ✅ |
| Control de voz/velocidad | ✅ | ✅ |
| Instalación | Simple | Requiere config |

---

## 🆕 Novedades en v1.1.0

✨ **Modo CLI añadido**
- Comando `tts-macos` para terminal
- Instalador separado (`install-cli.sh`)
- Soporte para argumentos y flags
- Integración con pipes y scripts
- Guía completa en `CLI-GUIDE.md`

🔧 **Mejoras**
- Setup.py para instalación con pip
- Mejor manejo de errores
- Documentación expandida
- Más ejemplos de uso

---

## 📖 Documentación Completa

- **README.md** - Documentación general
- **CLI-GUIDE.md** - Guía detallada CLI (¡NUEVO!)
- **QUICKSTART.md** - Inicio rápido
- **TROUBLESHOOTING.md** - Problemas y soluciones

---

## 🎉 ¡Empieza Ahora!

### Para usar CLI:
```bash
cd mcp-tts-macos
./install-cli.sh
tts-macos "Hola mundo"
```

### Para usar con Claude:
```bash
cd mcp-tts-macos
./install.sh
# Reiniciar Claude Desktop
```

### Para usar ambos:
```bash
cd mcp-tts-macos
./install-cli.sh
./install.sh
# ¡Listo!
```

---

**¿Tienes preguntas?** Consulta la documentación incluida.

**¿Encontraste un bug?** Lee TROUBLESHOOTING.md

**¡Disfruta de TTS-macOS! 🎤**
