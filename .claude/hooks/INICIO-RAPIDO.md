# 🚀 Inicio Rápido - Hooks TTS-macOS

## ⚡ Configuración en 3 Pasos

### Paso 1: Habilitar TTS

```bash
export TTS_ENABLED=true
```

### Paso 2: (Opcional) Elegir Voz

```bash
export TTS_VOICE=monica    # o jorge, paulina, juan, diego, angelica
```

### Paso 3: Usar Claude Code

```bash
# Ahora todas las respuestas se leerán en voz alta
claude-code
```

---

## 📋 Configuración Completa (Copiar y Pegar)

```bash
# Configuración básica recomendada
export TTS_ENABLED=true
export TTS_VOICE=monica
export TTS_RATE=175

# Iniciar Claude Code
claude-code
```

---

## 🎛️ Configuración Interactiva

```bash
# Usar el script de configuración guiada
source .claude/hooks/enable-tts.sh
```

Este script te preguntará:
- ¿Habilitar TTS?
- ¿Qué voz usar?
- ¿Qué velocidad?
- ¿Confirmar prompts?

---

## 🧪 Probar los Hooks

```bash
# Ejecutar demostración completa
./.claude/hooks/demo.sh
```

Esto reproducirá ejemplos de:
- Diferentes voces
- Diferentes velocidades
- Filtrado de código
- Confirmación de prompts

---

## 🎤 Voces Disponibles

| Alias | Descripción | Región |
|-------|-------------|--------|
| monica | Mujer | México |
| paulina | Mujer | México |
| jorge | Hombre | España |
| juan | Hombre | España |
| diego | Hombre | Argentina |
| angelica | Mujer | México |

---

## ⚙️ Variables de Configuración

### Para Respuestas de Claude

| Variable | Default | Descripción |
|----------|---------|-------------|
| `TTS_ENABLED` | `false` | Habilitar/deshabilitar TTS |
| `TTS_VOICE` | `monica` | Voz a utilizar |
| `TTS_RATE` | `175` | Velocidad (100-300 WPM) |
| `TTS_MAX_LENGTH` | `500` | Máximo de caracteres a leer |

### Para Confirmación de Prompts

| Variable | Default | Descripción |
|----------|---------|-------------|
| `TTS_PROMPT_ENABLED` | `false` | Confirmar envío de prompts |
| `TTS_PROMPT_VOICE` | `jorge` | Voz para confirmaciones |
| `TTS_PROMPT_RATE` | `200` | Velocidad para confirmaciones |

---

## 💡 Ejemplos Rápidos

### Solo Habilitar
```bash
export TTS_ENABLED=true
```

### Voz Masculina Española
```bash
export TTS_ENABLED=true
export TTS_VOICE=jorge
```

### Lectura Rápida
```bash
export TTS_ENABLED=true
export TTS_RATE=250
```

### Respuestas Cortas
```bash
export TTS_ENABLED=true
export TTS_MAX_LENGTH=200
```

---

## 🔧 Hacer Permanente

Para que la configuración se mantenga entre sesiones, agrega a `~/.zshrc`:

```bash
# TTS-macOS para Claude Code
export TTS_ENABLED=true
export TTS_VOICE=monica
export TTS_RATE=175
```

Luego recarga:
```bash
source ~/.zshrc
```

---

## 🎯 Alias Útiles

Agrega a `~/.zshrc`:

```bash
# Alias para diferentes configuraciones
alias claude-tts='TTS_ENABLED=true claude-code'
alias claude-monica='TTS_ENABLED=true TTS_VOICE=monica claude-code'
alias claude-jorge='TTS_ENABLED=true TTS_VOICE=jorge claude-code'
alias claude-silent='TTS_ENABLED=false claude-code'
```

Uso:
```bash
claude-tts        # Con voz por defecto
claude-monica     # Con voz Monica
claude-jorge      # Con voz Jorge
claude-silent     # Sin voz
```

---

## 🛑 Deshabilitar TTS

```bash
# Opción 1: Variable de entorno
export TTS_ENABLED=false

# Opción 2: Desactivar
unset TTS_ENABLED

# Opción 3: Usar alias
claude-silent
```

---

## 📚 Más Información

- **README Completo**: `.claude/hooks/README.md`
- **Ejemplos Detallados**: `.claude/hooks/EJEMPLOS.md`
- **Demo Interactiva**: `./.claude/hooks/demo.sh`
- **Configuración Guiada**: `source .claude/hooks/enable-tts.sh`

---

## ✅ Checklist

- [ ] Ejecuté `export TTS_ENABLED=true`
- [ ] Elegí una voz con `export TTS_VOICE=monica`
- [ ] (Opcional) Ajusté velocidad con `export TTS_RATE=175`
- [ ] Ejecuté Claude Code
- [ ] ¡Las respuestas se leen en voz alta! 🎉

---

## 🐛 Problemas Comunes

### No se escucha nada

```bash
# Verificar que TTS_ENABLED esté en true
echo $TTS_ENABLED

# Debe mostrar: true
# Si no, ejecutar:
export TTS_ENABLED=true
```

### La voz no se encuentra

```bash
# Listar voces disponibles
tts-macos --list

# o
say -v ? | grep -i spanish
```

### Los hooks no tienen permisos

```bash
chmod +x .claude/hooks/post-response
chmod +x .claude/hooks/user-prompt-submit
```

---

## 🎉 ¡Listo!

Ahora puedes usar Claude Code con respuestas en voz alta en español.

**Siguiente paso**: Ejecuta `claude-code` y pregunta algo a Claude. ¡La respuesta se leerá en voz alta!

```bash
export TTS_ENABLED=true
claude-code
```

---

**¿Necesitas ayuda?** Consulta `.claude/hooks/README.md` o ejecuta `.claude/hooks/demo.sh`
