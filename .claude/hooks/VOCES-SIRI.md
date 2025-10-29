# 🤖 Guía de Voces de Siri y Voces Mejoradas

## Voces de Siri Disponibles

macOS incluye voces de Siri de alta calidad que puedes usar con los hooks TTS-macOS:

### Voces de Siri Estándar

Las voces de Siri suelen aparecer con estos nombres:
- `Siri Female` - Voz femenina de Siri
- `Siri Male` - Voz masculina de Siri

### Voces de Siri Mejoradas (Neural)

Dependiendo de tu versión de macOS, puede haber voces mejoradas:
- Voces con calidad "Premium"
- Voces con tecnología "Neural"
- Voces "Enhanced" (Mejoradas)

## Cómo Usar Voces de Siri

### Opción 1: Nombre Exacto
```bash
export TTS_VOICE="Siri Female"
export TTS_VOICE="Siri Male"
```

### Opción 2: Búsqueda Parcial
Los hooks detectan automáticamente voces de Siri:
```bash
export TTS_VOICE=siri          # Encontrará la primera voz Siri
export TTS_VOICE="siri female" # Buscará voz femenina de Siri
export TTS_VOICE="siri male"   # Buscará voz masculina de Siri
```

## Listar Todas las Voces Disponibles

### Ver Todas las Voces
```bash
./.claude/hooks/list-all-voices.sh
```

### Ver Solo Voces de Siri
```bash
say -v \? | grep -i siri
```

### Ver Solo Voces en Español
```bash
say -v \? | grep -iE "(spanish|español)"
```

## Voces Mejoradas y Premium

### Qué Son

Las voces mejoradas son versiones de mayor calidad que:
- Suenan más naturales
- Tienen mejor entonación
- Requieren más espacio de descarga
- Pueden incluir tecnología Neural

### Cómo Identificarlas

```bash
# Ver voces premium/mejoradas
say -v \? | grep -iE "(premium|enhanced|neural|superior)"
```

### Cómo Descargarlas

1. Abre **Preferencias del Sistema** (System Preferences)
2. Ve a **Accesibilidad** → **Contenido Hablado** (Accessibility → Spoken Content)
3. Haz clic en **Voces del Sistema** (System Voices)
4. Busca voces con etiquetas:
   - "Premium Quality"
   - "Enhanced"
   - "Siri"
5. Haz clic en el ícono de descarga para instalarlas

## Ejemplos de Configuración

### Usar Voz de Siri Femenina
```bash
export TTS_ENABLED=true
export TTS_VOICE="Siri Female"
export TTS_RATE=175
```

### Usar Voz de Siri Masculina
```bash
export TTS_ENABLED=true
export TTS_VOICE="Siri Male"
export TTS_RATE=175
```

### Buscar Automáticamente Voz Siri
```bash
# El hook buscará automáticamente
export TTS_ENABLED=true
export TTS_VOICE=siri
export TTS_RATE=175
```

### Combinar Siri para Respuestas y Español para Confirmaciones
```bash
export TTS_ENABLED=true
export TTS_VOICE="Siri Female"
export TTS_RATE=175

export TTS_PROMPT_ENABLED=true
export TTS_PROMPT_VOICE=Monica
export TTS_PROMPT_RATE=200
```

## Voces Detectadas Automáticamente

Los hooks actualizados detectan automáticamente:

1. **Búsqueda exacta**: Coincidencia exacta del nombre
2. **Búsqueda parcial**: Coincidencia parcial (útil para Siri)
3. **Fallback español**: Si no encuentra, busca voz en español
4. **Fallback final**: Monica o primera voz disponible

### Ejemplos de Detección

```bash
# Nombre exacto
export TTS_VOICE=Monica          # → Monica

# Búsqueda parcial
export TTS_VOICE=siri            # → Siri Female (primera encontrada)
export TTS_VOICE="siri fem"      # → Siri Female
export TTS_VOICE="siri male"     # → Siri Male

# Case-insensitive
export TTS_VOICE=MONICA          # → Monica
export TTS_VOICE=jorge           # → Jorge
export TTS_VOICE=SIRI            # → Siri Female
```

## Probar Voces de Siri

### Test Rápido
```bash
# Probar voz de Siri directamente
say -v "Siri Female" "Hola, soy la voz de Siri femenina"
say -v "Siri Male" "Hola, soy la voz de Siri masculina"
```

### Test con los Hooks
```bash
export TTS_ENABLED=true
export TTS_VOICE="Siri Female"
echo "Prueba con voz de Siri" | ./.claude/hooks/post-response
```

### Test Interactivo
```bash
# Usar script de configuración
source .claude/hooks/enable-tts.sh
# Selecciona voz de Siri cuando te pregunte
```

## Comparación de Voces

| Tipo | Calidad | Naturalidad | Tamaño | Idiomas |
|------|---------|-------------|--------|---------|
| Voces Estándar | Media | Buena | Pequeño | Español |
| Voces Premium | Alta | Muy Buena | Mediano | Español |
| Voces Siri | Muy Alta | Excelente | Grande | Multi-idioma |

## Voces en Español Disponibles

### Voces Estándar
- Monica (México - Mujer)
- Paulina (México - Mujer)
- Jorge (España - Hombre)
- Juan (España - Hombre)
- Diego (Argentina - Hombre)

### Voces Adicionales
- Angelica (México - Mujer)
- Francisca (puede variar según instalación)

### Voces de Siri
- Siri Female (Multi-región)
- Siri Male (Multi-región)

## Configuración Recomendada por Uso

### Para Trabajo Profesional
```bash
export TTS_VOICE="Siri Female"  # Voz clara y profesional
export TTS_RATE=165              # Velocidad moderada
```

### Para Desarrollo Rápido
```bash
export TTS_VOICE=Monica          # Voz familiar en español
export TTS_RATE=220              # Velocidad rápida
```

### Para Aprendizaje
```bash
export TTS_VOICE=Jorge           # Voz clara masculina
export TTS_RATE=150              # Velocidad lenta para comprensión
```

### Para Presentaciones
```bash
export TTS_VOICE="Siri Male"     # Voz profesional
export TTS_RATE=175              # Velocidad estándar
```

## Troubleshooting

### "Voz Siri no encontrada"

```bash
# Verificar si está instalada
say -v \? | grep -i siri

# Si no aparece nada:
# 1. System Preferences → Accessibility → Spoken Content
# 2. System Voices
# 3. Buscar "Siri" y descargar
```

### "La voz suena robótica"

```bash
# Puede que tengas la versión estándar
# Descarga la versión Premium/Enhanced desde System Voices
```

### "No puedo encontrar voces premium"

```bash
# Verificar voces premium disponibles
say -v \? | grep -iE "(premium|enhanced)"

# Si no hay ninguna, descarga desde:
# System Preferences → Accessibility → Spoken Content → System Voices
# Busca voces marcadas con "Premium Quality"
```

## Scripts Útiles

### Listar Solo Voces de Siri
```bash
#!/bin/bash
echo "🤖 Voces de Siri disponibles:"
say -v \? | grep -i siri
```

### Probar Todas las Voces de Siri
```bash
#!/bin/bash
say -v \? | grep -i "siri" | while read line; do
    voz=$(echo "$line" | awk '{print $1}')
    echo "Probando: $voz"
    say -v "$voz" "Hola, soy $voz"
    sleep 2
done
```

### Comparar Voz Estándar vs Siri
```bash
#!/bin/bash
echo "Voz estándar (Monica):"
say -v Monica "Hola, esta es la voz Monica"
sleep 2

echo "Voz de Siri:"
say -v "Siri Female" "Hola, esta es la voz de Siri"
```

## Notas Importantes

1. **Las voces de Siri requieren descarga**: Son archivos grandes (100-300 MB)
2. **Mejor calidad**: Las voces de Siri suenan más naturales
3. **Multi-idioma**: Siri puede hablar varios idiomas con buena pronunciación
4. **Detección automática**: Los hooks detectan automáticamente las voces disponibles
5. **Fallback inteligente**: Si no encuentra Siri, usa voces en español disponibles

## Recursos

- **Documentación completa**: `.claude/hooks/README.md`
- **Listar voces**: `./.claude/hooks/list-all-voices.sh`
- **Configuración guiada**: `source .claude/hooks/enable-tts.sh`
- **Tests**: `./.claude/hooks/test-voices.sh`

---

**¡Disfruta de las voces de Siri con Claude Code! 🤖**
