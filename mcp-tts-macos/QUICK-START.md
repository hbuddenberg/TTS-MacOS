# 🚀 Guía Rápida - TTS-macOS

## 📖 Tabla de Contenidos

- [Instalación](#-instalación)
- [Comandos Básicos](#-comandos-básicos)
- [Ver Voces](#-ver-voces)
- [Usar Voces](#-usar-voces)
- [Crear Alias](#-crear-alias)
- [Ejemplos Avanzados](#-ejemplos-avanzados)

## 🔧 Instalación

```bash
# Instalar uv (una sola vez)
brew install uv

# Clonar o navegar al proyecto
cd /ruta/al/proyecto/mcp-tts-macos
```

## 💻 Comandos Básicos

```bash
# Ver ayuda completa
uvx --from . tts-macos --help

# Ver todas las voces disponibles (84+ voces)
uvx --from . tts-macos --list

# Reproducir texto simple
uvx --from . tts-macos "Hola mundo"

# Ver versión
uvx --from . tts-macos --version
```

## 🎤 Ver Voces

```bash
# Listar TODAS las voces (categorizado por tipo)
uvx --from . tts-macos --list

# Salida mostrará:
# ├── Voces en Español (16)
# ├── Voces Enhanced/Premium (12)
# ├── Voces de Siri
# └── Total de voces: 84+
```

## 🎭 Usar Voces

### Voces Básicas
```bash
uvx --from . tts-macos "Buenos días" --voice Eddy
uvx --from . tts-macos "Buenas noches" --voice Flo
```

### Voces Enhanced (Mejor Calidad)
```bash
# Voz con nombre completo
uvx --from . tts-macos "Calidad superior" --voice "Mónica (Enhanced)"

# Búsqueda flexible (sin acentos)
uvx --from . tts-macos "Calidad superior" --voice monica

# Otros ejemplos
uvx --from . tts-macos "Hola mundo" --voice "Jorge (Enhanced)"
uvx --from . tts-macos "Hola mundo" --voice jorge
```

### Voces con Acentos Regionales
```bash
# México
uvx --from . tts-macos "Acento mexicano" --voice "Angélica (Enhanced)"
uvx --from . tts-macos "Otra voz mexicana" --voice "Juan (Enhanced)"

# España
uvx --from . tts-macos "Acento español" --voice "Jorge (Enhanced)"
uvx --from . tts-macos "Voz de España" --voice "Mónica (Enhanced)"

# Argentina
uvx --from . tts-macos "Acento argentino" --voice "Diego (Enhanced)"

# Colombia
uvx --from . tts-macos "Acento colombiano" --voice "Carlos (Enhanced)"

# Chile
uvx --from . tts-macos "Acento chileno" --voice "Francisca (Enhanced)"
```

### ⚠️ Voces Siri - Limitación Importante

**Las voces de Siri NO funcionan con TTS-macOS** por limitaciones técnicas de Apple.

```bash
# ❌ ESTO NO FUNCIONA
uvx --from . tts-macos "Hola desde Siri" --voice "Siri Female"  # Error
uvx --from . tts-macos "Hola desde Siri" --voice siri           # Error
```

**✅ ALTERNATIVA RECOMENDADA**: Usa voces Enhanced de alta calidad

```bash
# Estas voces tienen calidad similar o superior a Siri
uvx --from . tts-macos "Calidad profesional" --voice "Mónica (Enhanced)"
uvx --from . tts-macos "Voz natural" --voice "Jorge (Enhanced)"
uvx --from . tts-macos "Audio claro" --voice "Angélica (Enhanced)"
```

📖 **[Ver guía completa sobre voces de Siri](SIRI-VOICES-GUIDE.md)**

## 🔍 Búsqueda Flexible

La herramienta acepta nombres **sin acentos**, **parciales** y **case-insensitive**:

```bash
# Sin acentos
uvx --from . tts-macos "Hola" --voice monica    # → Mónica (Enhanced)
uvx --from . tts-macos "Hola" --voice angelica  # → Angélica (Enhanced)

# Búsqueda parcial
uvx --from . tts-macos "Hola" --voice franc     # → Francisca (Enhanced)
uvx --from . tts-macos "Hola" --voice siri      # → Siri Female

# Case insensitive
uvx --from . tts-macos "Hola" --voice MONICA    # → Mónica (Enhanced)
uvx --from . tts-macos "Hola" --voice JoRgE     # → Jorge (Enhanced)
```

## ⚡ Velocidad

```bash
# Velocidad por defecto (175 WPM)
uvx --from . tts-macos "Velocidad normal"

# Más lento (útil para aprender)
uvx --from . tts-macos "Más despacio" --rate 120

# Velocidad media
uvx --from . tts-macos "Velocidad media" --rate 175

# Más rápido
uvx --from . tts-macos "Más rápido" --rate 250

# Muy rápido
uvx --from . tts-macos "Muy rápido" --rate 300
```

## 💾 Guardar Audio

```bash
# Guardar con voz por defecto
uvx --from . tts-macos "Mensaje a guardar" --save mensaje.aiff

# Guardar con voz específica
uvx --from . tts-macos "Audio profesional" --voice "Jorge (Enhanced)" --save profesional.aiff

# Guardar con velocidad personalizada
uvx --from . tts-macos "Audio rápido" --voice monica --rate 220 --save rapido.aiff

# Los archivos se guardan en el Escritorio
```

## 🔗 Crear Alias

Para uso más frecuente, crea un alias permanente:

```bash
# Agregar a ~/.zshrc o ~/.bashrc
alias tts='uvx --from /Volumes/Resources/Develop/TTS-MacOS/mcp-tts-macos tts-macos'

# Recargar configuración
source ~/.zshrc  # o source ~/.bashrc

# Usar el alias
tts "Ahora es más fácil"
tts --list
tts "Mensaje" --voice monica
tts "Audio" --save archivo.aiff --voice jorge
```

## 🎯 Ejemplos Avanzados

```bash
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CASO 1: Mensaje de cumpleaños con voz mexicana
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
uvx --from . tts-macos "Feliz cumpleaños mamá, espero que tengas un día maravilloso" \
  --voice "Angélica (Enhanced)" \
  --save cumpleanos.aiff

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CASO 2: Mensaje profesional con voz española
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
uvx --from . tts-macos "Estimado cliente, su pedido ha sido enviado" \
  --voice "Jorge (Enhanced)" \
  --rate 160 \
  --save mensaje-profesional.aiff

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CASO 3: Anuncio rápido
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
uvx --from . tts-macos "Atención: El evento comienza en 5 minutos" \
  --voice "Mónica (Enhanced)" \
  --rate 200

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CASO 4: Audio educativo (más lento)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
uvx --from . tts-macos "La inteligencia artificial es una rama de la informática" \
  --voice "Paulina (Enhanced)" \
  --rate 130 \
  --save educativo.aiff
```

## 📊 Comparación de Voces

### Voces Básicas vs Enhanced

```bash
# Comparar calidad: Básica vs Enhanced
uvx --from . tts-macos "Esta es la voz básica de Mónica" --voice "Mónica"
uvx --from . tts-macos "Esta es la voz mejorada de Mónica" --voice "Mónica (Enhanced)"

# Notar la diferencia en naturalidad y claridad
```

## 🆘 Solución de Problemas

```bash
# Si no funciona, limpiar cache de uv
uv cache clean

# Verificar que estás en el directorio correcto
pwd  # Debe mostrar: /ruta/al/proyecto/mcp-tts-macos

# Verificar que say funciona en tu sistema
say -v "Mónica" "Hola mundo"

# Ver todas las voces del sistema
say -v '?' | grep es_
```

## 💡 Tips

1. **Usa --list** frecuentemente para recordar los nombres de las voces
2. **Búsqueda flexible**: No necesitas escribir acentos ni mayúsculas
3. **Velocidad óptima**: 150-200 WPM para audio natural
4. **Voces Enhanced**: Siempre que sea posible, usa voces Enhanced para mejor calidad
5. **Alias**: Crea un alias para acceso rápido

## 📚 Más Información

- **README completo**: `README.md`
- **Documentación técnica**: `CLAUDE.md`
- **Instalación MCP**: Ver sección correspondiente en README.md

---

**¡Disfruta de TTS-macOS! 🎉**
