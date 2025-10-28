# Hooks de TTS-macOS para Claude Code

Este directorio contiene hooks que integran el sistema TTS-macOS con Claude Code para proporcionar respuestas de voz en español.

## Hooks Disponibles

### 1. `post-response`
Lee las respuestas de Claude en voz alta después de generarlas.

**Variables de configuración:**
- `TTS_ENABLED` - Habilitar/deshabilitar el TTS (default: `false`)
- `TTS_VOICE` - Voz a utilizar (default: `monica`)
  - Opciones: `monica`, `paulina`, `jorge`, `juan`, `diego`, `angelica`
- `TTS_RATE` - Velocidad en palabras por minuto (default: `175`)
  - Rango: 100-300
- `TTS_MAX_LENGTH` - Longitud máxima de texto a leer (default: `500`)

### 2. `user-prompt-submit`
Confirma cuando se envía un prompt del usuario.

**Variables de configuración:**
- `TTS_PROMPT_ENABLED` - Habilitar confirmación de prompts (default: `false`)
- `TTS_PROMPT_VOICE` - Voz para confirmaciones (default: `jorge`)
- `TTS_PROMPT_RATE` - Velocidad para confirmaciones (default: `200`)

## Configuración

### Opción 1: Variables de Entorno Globales

Agrega a tu `~/.zshrc` o `~/.bash_profile`:

```bash
# Habilitar TTS para respuestas
export TTS_ENABLED=true
export TTS_VOICE=monica
export TTS_RATE=175
export TTS_MAX_LENGTH=500

# Habilitar confirmación de prompts (opcional)
export TTS_PROMPT_ENABLED=false
export TTS_PROMPT_VOICE=jorge
export TTS_PROMPT_RATE=200
```

Luego recarga tu shell:
```bash
source ~/.zshrc
```

### Opción 2: Variables de Entorno por Sesión

```bash
# Solo para esta sesión
export TTS_ENABLED=true TTS_VOICE=paulina TTS_RATE=200
claude-code
```

### Opción 3: Script de Activación

Crea un script `enable-tts.sh`:

```bash
#!/bin/bash
export TTS_ENABLED=true
export TTS_VOICE=monica
export TTS_RATE=175
echo "✅ TTS habilitado con voz $TTS_VOICE a $TTS_RATE WPM"
```

Úsalo antes de iniciar Claude Code:
```bash
source enable-tts.sh
claude-code
```

## Permisos

Asegúrate de que los hooks sean ejecutables:

```bash
chmod +x .claude/hooks/*
```

## Ejemplos de Uso

### Uso Básico
```bash
# Habilitar TTS con configuración por defecto
export TTS_ENABLED=true
```

### Voz Masculina Española
```bash
export TTS_ENABLED=true
export TTS_VOICE=jorge
export TTS_RATE=180
```

### Voz Rápida
```bash
export TTS_ENABLED=true
export TTS_VOICE=paulina
export TTS_RATE=250
```

### Leer Solo Respuestas Cortas
```bash
export TTS_ENABLED=true
export TTS_MAX_LENGTH=200
```

### Con Confirmación de Prompts
```bash
export TTS_ENABLED=true
export TTS_PROMPT_ENABLED=true
```

## Deshabilitar Temporalmente

```bash
# Opción 1: Variable de entorno
export TTS_ENABLED=false

# Opción 2: Desactivar en tiempo real
unset TTS_ENABLED
```

## Solución de Problemas

### El hook no se ejecuta

1. Verifica permisos:
   ```bash
   ls -la .claude/hooks/
   # Deben tener permisos de ejecución (x)
   ```

2. Hazlos ejecutables:
   ```bash
   chmod +x .claude/hooks/post-response
   chmod +x .claude/hooks/user-prompt-submit
   ```

3. Verifica que `TTS_ENABLED=true`

### No se escucha audio

1. Verifica que tts-macos esté instalado:
   ```bash
   which tts-macos
   ```

2. Prueba el comando say directamente:
   ```bash
   say -v Monica "Prueba de audio"
   ```

3. Verifica el volumen del sistema

### Las voces no se encuentran

Lista las voces disponibles:
```bash
tts-macos --list
# o
say -v ? | grep -i spanish
```

Instala voces desde: System Preferences → Accessibility → Spoken Content → System Voices

## Personalización Avanzada

### Filtrar Respuestas por Contenido

Edita `post-response` para agregar filtros:

```bash
# Solo leer respuestas cortas
if [ ${#TEXT} -gt 1000 ]; then
    exit 0
fi

# No leer código
if echo "$RESPONSE" | grep -q '```'; then
    exit 0
fi
```

### Diferentes Voces por Tipo de Respuesta

```bash
# Usar voz de error para mensajes de error
if echo "$TEXT" | grep -iq "error"; then
    VOICE="diego"
    RATE=150
fi
```

### Guardar Respuestas como Audio

```bash
# Guardar en archivo
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
tts-macos "$TEXT" --voice "$VOICE" --save "~/Desktop/claude_${TIMESTAMP}.aiff"
```

## Integración con MCP Server

Estos hooks funcionan independientemente del servidor MCP. Si quieres usar el servidor MCP en lugar del CLI:

```bash
# Modificar post-response para usar el MCP (requiere configuración adicional)
# Esto es más complejo y requiere comunicación con el servidor MCP
```

## Tips

1. **Inicio Rápido**: Crea un alias en tu shell:
   ```bash
   alias claude-tts='TTS_ENABLED=true claude-code'
   ```

2. **Perfiles de Voz**: Crea diferentes perfiles:
   ```bash
   alias claude-monica='TTS_ENABLED=true TTS_VOICE=monica claude-code'
   alias claude-jorge='TTS_ENABLED=true TTS_VOICE=jorge claude-code'
   ```

3. **Solo para Debugging**: Habilita solo cuando necesites:
   ```bash
   # En una terminal
   export TTS_ENABLED=true
   # Claude Code leerá las respuestas en esta sesión
   ```

## Notas

- Los hooks se ejecutan en segundo plano (`&`) para no bloquear Claude Code
- El texto se limpia de markdown antes de leerse
- Los bloques de código no se leen por defecto
- Las respuestas muy largas se truncan según `TTS_MAX_LENGTH`

## Contribuir

Para mejorar estos hooks:
1. Edita los archivos en `.claude/hooks/`
2. Prueba con `TTS_ENABLED=true`
3. Comparte tus mejoras

---

**¡Disfruta de Claude Code con voz en español! 🎤🇪🇸**
