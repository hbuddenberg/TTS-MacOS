# Ejemplos de Uso de Hooks TTS-macOS

## Configuraciones Rápidas

### Ejemplo 1: Uso Básico (Voz Monica)

```bash
# Habilitar TTS con configuración por defecto
export TTS_ENABLED=true

# Iniciar Claude Code
# Ahora todas las respuestas se leerán en voz alta con Monica
```

### Ejemplo 2: Voz Masculina Española

```bash
# Configurar voz Jorge (España - Hombre)
export TTS_ENABLED=true
export TTS_VOICE=jorge
export TTS_RATE=180

# Las respuestas se leerán con voz masculina española
```

### Ejemplo 3: Lectura Rápida

```bash
# Configurar velocidad rápida para respuestas cortas
export TTS_ENABLED=true
export TTS_VOICE=paulina
export TTS_RATE=250
export TTS_MAX_LENGTH=300
```

### Ejemplo 4: Solo Respuestas Cortas

```bash
# Leer solo los primeros 200 caracteres
export TTS_ENABLED=true
export TTS_MAX_LENGTH=200
```

### Ejemplo 5: Con Confirmación de Prompts

```bash
# Confirmar tanto prompts como respuestas
export TTS_ENABLED=true
export TTS_VOICE=monica
export TTS_PROMPT_ENABLED=true
export TTS_PROMPT_VOICE=jorge
```

## Alias Útiles

Agrega estos alias a tu `~/.zshrc` o `~/.bash_profile`:

```bash
# Alias para diferentes configuraciones de TTS
alias claude-silent='TTS_ENABLED=false claude-code'
alias claude-tts='TTS_ENABLED=true claude-code'
alias claude-monica='TTS_ENABLED=true TTS_VOICE=monica claude-code'
alias claude-jorge='TTS_ENABLED=true TTS_VOICE=jorge claude-code'
alias claude-fast='TTS_ENABLED=true TTS_RATE=250 claude-code'
alias claude-slow='TTS_ENABLED=true TTS_RATE=125 claude-code'

# Función para configuración dinámica
function claude-voz() {
    local voz=${1:-monica}
    local velocidad=${2:-175}
    TTS_ENABLED=true TTS_VOICE=$voz TTS_RATE=$velocidad claude-code
}

# Uso:
# claude-voz monica 200
# claude-voz jorge 150
```

## Perfiles de Uso

### Perfil: Trabajo Concentrado
```bash
# Voz suave y velocidad media
export TTS_ENABLED=true
export TTS_VOICE=paulina
export TTS_RATE=160
export TTS_MAX_LENGTH=400
export TTS_PROMPT_ENABLED=false
```

### Perfil: Desarrollo Rápido
```bash
# Voz clara y velocidad rápida
export TTS_ENABLED=true
export TTS_VOICE=monica
export TTS_RATE=220
export TTS_MAX_LENGTH=200
export TTS_PROMPT_ENABLED=false
```

### Perfil: Aprendizaje
```bash
# Voz clara y velocidad lenta para mejor comprensión
export TTS_ENABLED=true
export TTS_VOICE=jorge
export TTS_RATE=140
export TTS_MAX_LENGTH=1000
export TTS_PROMPT_ENABLED=true
```

### Perfil: Presentación
```bash
# Voz profesional para demostraciones
export TTS_ENABLED=true
export TTS_VOICE=juan
export TTS_RATE=165
export TTS_MAX_LENGTH=800
export TTS_PROMPT_ENABLED=true
export TTS_PROMPT_VOICE=angelica
```

## Scripts de Automatización

### Script 1: Activar/Desactivar TTS

```bash
#!/bin/bash
# toggle-tts.sh

if [ "$TTS_ENABLED" = "true" ]; then
    export TTS_ENABLED=false
    echo "🔇 TTS deshabilitado"
else
    export TTS_ENABLED=true
    echo "🔊 TTS habilitado (voz: ${TTS_VOICE:-monica})"
fi
```

Uso:
```bash
source toggle-tts.sh
```

### Script 2: Cambiar Voz Rápidamente

```bash
#!/bin/bash
# cambiar-voz.sh

case $1 in
    1|monica)   export TTS_VOICE=monica   ; echo "🎤 Voz: Monica" ;;
    2|paulina)  export TTS_VOICE=paulina  ; echo "🎤 Voz: Paulina" ;;
    3|jorge)    export TTS_VOICE=jorge    ; echo "🎤 Voz: Jorge" ;;
    4|juan)     export TTS_VOICE=juan     ; echo "🎤 Voz: Juan" ;;
    5|diego)    export TTS_VOICE=diego    ; echo "🎤 Voz: Diego" ;;
    6|angelica) export TTS_VOICE=angelica ; echo "🎤 Voz: Angelica" ;;
    *) echo "Uso: $0 [monica|paulina|jorge|juan|diego|angelica]" ;;
esac
```

Uso:
```bash
source cambiar-voz.sh jorge
source cambiar-voz.sh 3
```

### Script 3: Iniciar Claude con Selección Interactiva

```bash
#!/bin/bash
# claude-con-voz.sh

echo "🎙️  Selecciona configuración de voz:"
echo "1. Monica (Mujer México) - Velocidad normal"
echo "2. Jorge (Hombre España) - Velocidad normal"
echo "3. Paulina (Mujer México) - Velocidad rápida"
echo "4. Sin voz"
read -p "Opción (1-4): " opcion

case $opcion in
    1)
        export TTS_ENABLED=true
        export TTS_VOICE=monica
        export TTS_RATE=175
        ;;
    2)
        export TTS_ENABLED=true
        export TTS_VOICE=jorge
        export TTS_RATE=175
        ;;
    3)
        export TTS_ENABLED=true
        export TTS_VOICE=paulina
        export TTS_RATE=220
        ;;
    4)
        export TTS_ENABLED=false
        ;;
esac

claude-code
```

## Integración con Otras Herramientas

### Con tmux

```bash
# .tmux.conf
# Diferentes sesiones con diferentes voces

# Sesión 1: Desarrollo
bind-key C-1 send-keys "TTS_ENABLED=true TTS_VOICE=monica claude-code" Enter

# Sesión 2: Debugging
bind-key C-2 send-keys "TTS_ENABLED=true TTS_VOICE=jorge TTS_RATE=150 claude-code" Enter

# Sesión 3: Sin voz
bind-key C-3 send-keys "TTS_ENABLED=false claude-code" Enter
```

### Con Keyboard Maestro (macOS)

Crear macro que ejecute:
```applescript
tell application "Terminal"
    activate
    do script "export TTS_ENABLED=true; export TTS_VOICE=monica; cd ~/projects; claude-code"
end tell
```

### Con Alfred Workflow

Crear workflow que ejecute:
```bash
export TTS_ENABLED=true
export TTS_VOICE={query}
open -a Terminal.app
```

## Casos de Uso Específicos

### Caso 1: Programación en Pares Remota

```bash
# Usar voz clara para que ambos escuchen
export TTS_ENABLED=true
export TTS_VOICE=jorge
export TTS_RATE=165
export TTS_MAX_LENGTH=600
```

### Caso 2: Accesibilidad

```bash
# Configuración para usuarios con discapacidad visual
export TTS_ENABLED=true
export TTS_VOICE=monica
export TTS_RATE=180
export TTS_MAX_LENGTH=2000  # Leer respuestas completas
export TTS_PROMPT_ENABLED=true
```

### Caso 3: Multitarea

```bash
# Escuchar respuestas mientras trabajas en otra cosa
export TTS_ENABLED=true
export TTS_VOICE=paulina
export TTS_RATE=190
export TTS_MAX_LENGTH=500
```

### Caso 4: Aprendizaje de Español

```bash
# Diferentes acentos para familiarizarse
# Alternar entre:
export TTS_VOICE=monica   # México
export TTS_VOICE=jorge    # España
export TTS_VOICE=diego    # Argentina
```

## Personalización Avanzada del Hook

### Modificar `post-response` para Casos Especiales

```bash
# Agregar al final de post-response antes de reproducir:

# Solo leer si contiene ciertas palabras clave
if ! echo "$TEXT" | grep -qiE "importante|error|atención|completado"; then
    exit 0
fi

# Usar voz diferente para errores
if echo "$TEXT" | grep -qi "error"; then
    VOICE="diego"
    RATE=150
fi

# Guardar respuestas importantes
if echo "$TEXT" | grep -qi "importante"; then
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    tts-macos "$TEXT" --voice "$VOICE" --save ~/Desktop/importante_${TIMESTAMP}.aiff
fi
```

## Testing de Hooks

```bash
# Probar el hook post-response manualmente
echo "Esta es una respuesta de prueba" | ./.claude/hooks/post-response

# Con configuración específica
TTS_ENABLED=true TTS_VOICE=jorge TTS_RATE=200 \
    echo "Probando con Jorge" | ./.claude/hooks/post-response

# Probar el hook user-prompt-submit
echo "¿Cuál es la capital de España?" | ./.claude/hooks/user-prompt-submit

# Ejecutar la demo completa
./.claude/hooks/demo.sh
```

## Troubleshooting Ejemplos

### Debug: Ver qué se está ejecutando

```bash
# Agregar debug al inicio de post-response
echo "DEBUG: TTS_ENABLED=$TTS_ENABLED" >> /tmp/tts-debug.log
echo "DEBUG: TEXT=$TEXT" >> /tmp/tts-debug.log

# Ver el log
tail -f /tmp/tts-debug.log
```

### Debug: Probar sin hooks

```bash
# Probar comando directo
tts-macos "Prueba directa" --voice monica

# Probar con say
say -v Monica "Prueba con say"

# Verificar permisos
ls -la .claude/hooks/
```

## Recursos Adicionales

- Ver todas las voces: `tts-macos --list`
- Documentación completa: `.claude/hooks/README.md`
- Demo interactiva: `.claude/hooks/demo.sh`
- Configuración rápida: `source .claude/hooks/enable-tts.sh`

---

**💡 Tip**: Empieza con la configuración básica y ve ajustando según tus preferencias:

```bash
# Configuración inicial recomendada
export TTS_ENABLED=true
export TTS_VOICE=monica
export TTS_RATE=175

# Después de probar, ajusta a tu gusto
```
