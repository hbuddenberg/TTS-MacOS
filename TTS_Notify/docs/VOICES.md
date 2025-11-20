# Voice Reference - TTS Notify v2.0.0

Complete reference of all available voices in macOS and how to use them with TTS Notify v2.0.0 modular voice system.

## 🎵 Voice System v2.0.0 Overview

The TTS Notify v2.0.0 voice system has been completely redesigned with:
- **84+ Voice Support**: Automatic detection of all system voices
- **Intelligent Categorization**: Español, Enhanced, Premium, Siri, Others
- **3-Tier Search Algorithm**: Exact → Prefix → Partial → Fallback
- **75% Faster Detection**: 5-minute TTL caching system
- **Flexible Search**: Case-insensitive, accent-insensitive matching

## 🔍 Voice Detection System

### Automatic Detection Process

1. **System Scan**: Executes `say -v ?` to discover all voices
2. **Smart Parsing**: Extracts names, languages, and metadata
3. **Intelligent Categorization**: Groups voices by type and quality
4. **Normalization**: Creates lowercase aliases for flexible search
5. **Caching**: Stores results for 5 minutes with TTL

### Search Algorithm v2.0

```bash
# Exact match (highest priority)
tts-notify --voice monica "Test"

# Case-insensitive search
tts-notify --voice MONICA "Test"
tts-notify --voice Monica "Test"

# Partial match (finds Angélica)
tts-notify --voice angel "Test"

# Quality variants
tts-notify --voice "monica enhanced" "Test"
tts-notify --voice "jorge premium" "Test"

# Fallback system
tts-notify --voice nonexistent_voice "Test"  # → First Spanish voice → Monica
```

## 🗣️ Voice Categories

### 1. Español (16 voices)

#### Spain Voices

| Voice | Type | Quality | Best Use | Search Aliases |
|-------|------|---------|----------|----------------|
| **jorge** | Premium | High | General male | jorge, jor |
| **monica** | Premium | High | General female | monica, mon |
| **marisol** | Premium | High | Formal reading | marisol, mari |
| **carlos** | Enhanced | Medium | News content | carlos, car |
| **diego** | Enhanced | Medium | Conversational | diego, die |
| **isabela** | Enhanced | Medium | Friendly tone | isabela, isa |

#### Mexico Voices

| Voice | Type | Quality | Best Use | Search Aliases |
|-------|------|---------|----------|----------------|
| **ángelica** | Premium | High | Primary female | angelica, angel, ang |
| **paulina** | Premium | High | Professional | paulina, paul |
| **juan** | Enhanced | Medium | Standard male | juan, jua |
| **eddy** | Standard | Low | Casual tone | eddy, edd |
| **reed** | Standard | Low | Youthful | reed, ree |

#### Chile Voices

| Voice | Type | Quality | Best Use | Search Aliases |
|-------|------|---------|----------|----------------|
| **francisca** | Premium | High | Neutral/professional | francisca, franc |

#### Colombia Voices

| Voice | Type | Quality | Best Use | Search Aliases |
|-------|------|---------|----------|----------------|
| **carlos** | Premium | High | News anchor | carlos, car |
| **soledad** | Premium | High | Formal tone | soledad, sol |
| **jimena** | Premium | High | Friendly | jimena, jim |

#### Argentina Voices

| Voice | Type | Quality | Best Use | Search Aliases |
|-------|------|---------|----------|----------------|
| **diego** | Premium | High | Conversational | diego, die |
| **isabela** | Premium | High | Clear/neutral | isabela, isa |

#### Universal Legacy Voices

| Voice | Characteristics | Best Use | Search Aliases |
|-------|-----------------|----------|----------------|
| **grandma** | Elderly tone | Storytelling | grandma, grand |
| **grandpa** | Elderly male | Narration | grandpa, grand |
| **flo** | Soft gentle | Short messages | flo |
| **rocko** | Energetic | Alerts | rocko, rock |
| **sandy** | Youthful | Informal | sandy, sand |
| **shelley** | Neutral | General purpose | shelley, shell |

### 2. Enhanced/Premium Voices (12 voices)

Quality-tuned voices with enhanced synthesis:

```bash
# Enhanced voices automatically detected
tts-notify --list

# Expected output:
Enhanced/Premium (12 voces):
  •ángelica (enhanced)    • francisca (enhanced)
  • jorge (enhanced)       • paulina (enhanced)
  • monica (enhanced)      • juan (enhanced)
  • diego (enhanced)       • carlos (enhanced)
  • isabela (enhanced)     • marisol (enhanced)
  • soledad (enhanced)     • jimena (enhanced)
```

#### Quality Comparison

| Quality | Size | Processing | Speed | Naturalness |
|---------|------|------------|-------|-------------|
| **Standard** | ~10MB | Fast | High | Basic |
| **Enhanced** | ~50MB | Medium | Medium | Good |
| **Premium** | ~200MB | Slower | Medium-High | Excellent |

### 3. Siri Voices (2 voices)

Neural-network based voices with superior quality:

#### Availability Check

```bash
# Verify Siri voices are installed
say -v ? | grep -i siri

# Expected output if installed:
# Siri Female    es-ES    _Neural TTS_
# Siri Male      es-ES    _Neural TTS_
```

#### Siri Voice Characteristics

| Feature | Description |
|---------|-------------|
| **Neural Synthesis** | Advanced neural network TTS |
| **Natural Prosody** | Superior intonation and rhythm |
| **High Expressivity** | Better emotional range |
| **macOS 10.14+** | Requires Mojave or later |
| **Optional Download** | ~300MB per voice |

#### Using Siri Voices

```bash
# Direct usage (if installed)
tts-notify --voice "siri female" "Texto con calidad neural"
tts-notify --voice "siri male" "Texto con voz masculina neural"

# Flexible search works
tts-notify --voice siri "Texto"  # Finds Siri Female first
tts-notify --voice "siri m" "Texto"  # Finds Siri Male
```

### 4. Other System Voices (50+)

Additional voices in various languages:

#### English (United States)

| Voice | Type | Best Use |
|-------|------|----------|
| **samantha** | Premium | Primary female voice |
| **alex** | Enhanced | Standard male voice |
| **victoria** | Enhanced | Clear, professional |
| **daniel** | Premium | News and formal content |
| **karen** | Enhanced | Conversational |
| **moira** | Enhanced | Irish accent |

#### English (British)

| Voice | Type | Best Use |
|-------|------|----------|
| **daniel** | Enhanced | Standard British |
| **karen** | Enhanced | Female British |
| **serena** | Enhanced | Formal British |

#### Other Languages

```bash
# Discover voices by language
say -v ? | grep -i "french"     # French voices
say -v ? | grep -i "german"     # German voices
say -v ? | grep -i "italian"    # Italian voices
say -v ? | grep -i "japanese"   # Japanese voices
```

## ⚙️ Voice Management v2.0.0

### Voice Filtering Commands

```bash
# Filter by gender
tts-notify --list --gen female    # Female voices only
tts-notify --list --gen male      # Male voices only

# Filter by language
tts-notify --list --lang es_ES    # Spanish voices only
tts-notify --list --lang en_US    # English voices only

# Filter by voice type
tts-notify --list --type enhanced  # Enhanced voices only
tts-notify --list --type premium   # Premium voices only
tts-notify --list --type siri      # Siri voices only

# Compact output format
tts-notify --list --compact

# Verbose with metadata
tts-notify --list --verbose
```

### Voice Caching System

```bash
# Caching configuration (v2.0.0)
export TTS_NOTIFY_CACHE_ENABLED=true      # Enable caching (default)
export TTS_NOTIFY_CACHE_TTL=300           # Cache TTL in seconds (5 min)

# Clear cache manually
rm -rf ~/.cache/tts-notify/

# Cache status
tts-notify --info | grep cache
```

### Voice Quality Selection

```bash
# Force specific quality levels
export TTS_NOTIFY_QUALITY=enhanced        # Prefer enhanced voices
export TTS_NOTIFY_QUALITY=premium         # Prefer premium voices
export TTS_NOTIFY_QUALITY=standard        # Use standard voices

# Configuration profiles
tts-notify --profile claude-desktop       # Optimized for Claude Desktop
tts-notify --profile accessibility        # Accessibility focused
```

## 🛠️ Voice Installation & Management

### System Voice Installation

#### Via System Preferences

```bash
# Open speech preferences
open "x-apple.systempreferences:com.apple.preference.speech?Synthesizing"
```

1. **System Preferences** → **Accessibility** → **Spoken Content**
2. **System Voice** → **Customize...**
3. **Download additional voices**

#### Via Terminal

```bash
# List available voice downloads
sudo softwareupdate --list

# Install specific voice packs
sudo softwareupdate --install "Voice Data Spanish (Mexico)"
sudo softwareupdate --install "Voice Data Spanish (Spain)"
sudo softwareupdate --install "Voice Data Enhanced"

# Install all available voices
sudo softwareupdate --install-all

# Check what's installed
say -v ? | wc -l        # Total voice count
say -v ? | grep spanish  # Spanish voices specifically
```

### Download Sizes

| Voice Type | Size per Voice | Download Time |
|------------|----------------|---------------|
| **Standard** | ~10MB | ~30 seconds |
| **Enhanced** | ~50-100MB | ~2-5 minutes |
| **Premium** | ~200-500MB | ~10-20 minutes |
| **Siri** | ~300MB | ~5-10 minutes |

## 🌍 Regional Configuration

### Region-Specific Defaults

```bash
# Spain configuration
export TTS_NOTIFY_VOICE=jorge
export TTS_NOTIFY_LANGUAGE=es_ES
export TTS_NOTIFY_REGION=spain

# Mexico configuration
export TTS_NOTIFY_VOICE=ángelica
export TTS_NOTIFY_LANGUAGE=es_MX
export TTS_NOTIFY_REGION=mexico

# Argentina configuration
export TTS_NOTIFY_VOICE=diego
export TTS_NOTIFY_LANGUAGE=es_AR
export TTS_NOTIFY_REGION=argentina

# Colombia configuration
export TTS_NOTIFY_VOICE=carlos
export TTS_NOTIFY_LANGUAGE=es_CO
export TTS_NOTIFY_REGION=colombia
```

### Voice Profiles by Use Case

```bash
# News/Information profile
export TTS_NOTIFY_VOICE=jorge
export TTS_NOTIFY_RATE=180
export TTS_NOTIFY_QUALITY=premium

# Accessibility profile
export TTS_NOTIFY_VOICE="siri female"
export TTS_NOTIFY_RATE=200
export TTS_NOTIFY_QUALITY=enhanced

# Conversational profile
export TTS_NOTIFY_VOICE=eddy
export TTS_NOTIFY_RATE=175
export TTS_NOTIFY_QUALITY=standard

# Professional profile
export TTS_NOTIFY_VOICE=ángelica
export TTS_NOTIFY_RATE=165
export TTS_NOTIFY_QUALITY=premium
```

## 🚀 Performance Optimization

### Voice Selection by Performance

```bash
# Fastest processing (standard voices)
tts-notify --voice monica "Quick message"

# Balanced (enhanced voices)
tts-notify --voice "monica enhanced" "Balanced quality"

# Best quality (premium/siri voices)
tts-notify --voice "siri female" "Highest quality"
```

### Speed Optimization by Voice Type

| Voice Type | Max Recommended Rate | Quality |
|------------|---------------------|---------|
| **Standard** | 175 WPM | Basic clarity |
| **Enhanced** | 200 WPM | Good clarity |
| **Premium** | 225 WPM | Excellent clarity |
| **Siri** | 250 WPM | Superior clarity |

### Caching for Performance

```bash
# Pre-load voices for instant access
tts-notify --list > /dev/null

# Warm up cache with preferred voice
tts-notify --voice jorge "Cache warmed up"
```

## 🔧 Advanced Voice Features

### Voice Variants and Modifiers

```bash
# Quality-specific variants
tts-notify --voice "monica enhanced" "Enhanced quality"
tts-notify --voice "jorge premium" "Premium quality"

# Regional variants
tts-notify --voice "jorge spain" "Spanish Spain variant"
tts-notify --voice "ángelica mexico" "Mexican variant"

# Speed optimization by voice
tts-notify --voice "siri female" --rate 250 "Fast neural speech"
tts-notify --voice monica --rate 150 "Slower standard speech"
```

### Voice Testing and Comparison

```bash
# Compare voice quality
for voice in "monica" "monica enhanced" "siri female"; do
    echo "Testing: $voice"
    tts-notify --voice "$voice" "This is a test of the $voice voice system"
    sleep 2
done

# Speed comparison
for rate in 150 175 200 225; do
    echo "Testing rate: $rate"
    tts-notify --voice jorge --rate "$rate" "Testing speech rate $rate"
    sleep 2
done
```

## 🔍 Voice Troubleshooting

### Voice Detection Issues

```bash
# Check system voice detection
say -v ? | head -5

# Verify TTS Notify detection
tts-notify --list | head -5

# Compare results
echo "System voices:"
say -v ? | wc -l
echo "TTS Notify voices:"
tts-notify --list | grep -c "•"
```

### Voice Quality Problems

```bash
# Test voice directly with macOS
say -v monica "Direct macOS test"
say -v "Mónica" "Enhanced voice test"

# Test through TTS Notify
tts-notify --voice monica "TTS Notify standard test"
tts-notify --voice "monica enhanced" "TTS Notify enhanced test"

# Check for voice corruption
say -v ? | grep -i monica
```

### Missing Voice Solutions

```bash
# Voice not found - check similar voices
say -v ? | grep -i "part_of_voice_name"

# Install missing voices
sudo softwareupdate --list | grep -i voice

# Fallback to universal voice
tts-notify --voice nonexistent_voice "This will use fallback"
```

## 📊 Voice Reference Quick Guide

### Recommended Voices by Use Case

| Use Case | Primary Voice | Backup | Command |
|----------|---------------|---------|---------|
| **General Spanish** | `jorge` | `monica` | `tts-notify --voice jorge` |
| **Female Spanish** | `ángelica` | `monica` | `tts-notify --voice angelica` |
| **High Quality** | `siri female` | `monica enhanced` | `tts-notify --voice "siri female"` |
| **Fast Alerts** | `siri male` | `rocko` | `tts-notify --voice "siri male" --rate 250` |
| **News Content** | `carlos` | `jorge` | `tts-notify --voice carlos` |
| **Conversational** | `eddy` | `juan` | `tts-notify --voice eddy` |
| **Accessibility** | `siri female` | `ángelica premium` | `tts-notify --profile accessibility` |
| **System Fallback** | `monica` | `first spanish voice` | Automatic |

### Essential Commands

```bash
# List all voices with categories
tts-notify --list

# Compact voice list
tts-notify --list --compact

# Filter by gender
tts-notify --list --gen female
tts-notify --list --gen male

# System voice information
tts-notify --info

# Voice search examples
tts-notify --voice angel "Test"      # Finds Ángelica
tts-notify --voice siri "Test"       # Finds Siri Female
tts-notify --voice enhanced "Test"   # Uses enhanced quality

# Performance testing
time tts-notify --list               # Test voice detection speed
tts-notify --voice monica "Test"     # Basic functionality test
```

### Voice Discovery

```bash
# Total voice count
say -v ? | wc -l

# Spanish voices only
say -v ? | grep -i -E "(spanish|español|es-)"

# Enhanced/premium voices
say -v ? | grep -i -E "(enhanced|premium|compact)"

# Siri voices check
say -v ? | grep -i siri

# Voice metadata inspection
say -v ? | grep -A2 -B2 "jorge"
```

This v2.0.0 voice reference provides comprehensive information about the enhanced voice system, enabling users to leverage the full power of the 84+ voice support with intelligent categorization and flexible search capabilities.

## Sistema de Detección de Voces

TTS Notify detecta automáticamente todas las voces instaladas en el sistema usando el comando `say -v ?`.

### Proceso de Detección

1. **Ejecuta**: `say -v ?` para listar todas las voces del sistema
2. **Parsea**: Salida para extraer nombres y metadatos
3. **Categoriza**: Voces por tipo y idioma
4. **Normaliza**: Nombres para búsqueda sin acentos

### Búsqueda Flexible

```bash
# Estas búsquedas encuentran la misma voz "Angélica"
tts-notify --voice "Angélica" "Texto"
tts-notify --voice "angelica" "Texto"
tts-notify --voice "Angelica" "Texto"
tts-notify --voice "angel" "Texto"
```

## Voces en Español

### España

| Voz | Tipo | Calidad | Uso Recomendado |
|-----|------|---------|-----------------|
| **Jorge** | Premium | Alta | Voz masculina principal |
| **Mónica** | Premium | Alta | Voz femenina principal |
| **Marisol** | Premium | Alta | Lectura formal |
| **Carlos** | Enhanced | Media | Noticias |
| **Diego** | Enhanced | Media | Conversacional |
| **Isabela** | Enhanced | Media | Amistosa |

### México

| Voz | Tipo | Calidad | Uso Recomendado |
|-----|------|---------|-----------------|
| **Angélica** | Premium | Alta | Voz femenina principal |
| **Paulina** | Premium | Alta | Profesional |
| **Juan** | Enhanced | Media | Masculina estándar |
| **Eddy** | Standard | Baja | Casual |
| **Reed** | Standard | Baja | juvenil |

### Chile

| Voz | Tipo | Calidad | Uso Recomendado |
|-----|------|---------|-----------------|
| **Francisca** | Premium | Alta | Neutral/profesional |

### Colombia

| Voz | Tipo | Calidad | Uso Recomendado |
|-----|------|---------|-----------------|
| **Carlos** | Premium | Alta | Noticiero |
| **Soledad** | Premium | Alta | Formal |
| **Jimena** | Premium | Alta | Amigable |

### Argentina

| Voz | Tipo | Calidad | Uso Recomendado |
|-----|------|---------|-----------------|
| **Diego** | Premium | Alta | Conversacional |
| **Isabela** | Premium | Alta | Clara/neutral |

### Voces Legacy (Disponibles en todos los macOS)

| Voz | Características | Uso |
|-----|-----------------|-----|
| **Monica** | Voz por defecto | Fiable en todos los sistemas |
| **Grandma** | Tono老年人 | Narración |
| **Grandpa** | Tono老年人 | Narración |
| **Flo** | Suave | Mensajes cortos |
| **Rocko** | Energética | Alertas |
| **Sandy** | Juvenil | Mensajes informales |
| **Shelley** | Neutral | General |

## Voces Siri

### Disponibilidad

Las voces Siri están disponibles en:
- **macOS 10.14 (Mojave) o superior**
- **Requieren descarga opcional**

### Voces Siri Disponibles

```bash
# Verificar si Siri voices están instaladas
say -v ? | grep -i siri

# Salida esperada:
# Siri Female    es-ES    _神经网络的TTS_
# Siri Male      es-ES    _神经网络的TTS_
```

### Características de Voces Siri

- **Calidad superior**: Voces neurales de alta fidelidad
- **Prosodia natural**: Mejor entonación y ritmo
- **Soporte extendido**: Más expresividad

### Uso de Voces Siri

```bash
# Si están instaladas, usar directamente
tts-notify --voice "Siri Female" "Texto con Siri"
tts-notify --voice "Siri Male" "Texto con Siri masculina"

# Búsqueda flexible también funciona
tts-notify --voice "siri" "Texto"  # Encontrará Siri Female
```

## Voces Enhanced y Premium

### Diferencias

| Tipo | Calidad | Tamaño | Procesamiento |
|------|---------|--------|---------------|
| **Standard** | Básica | ~10MB | Rápido |
| **Enhanced** | Media | ~50MB | Moderado |
| **Premium** | Alta | ~200MB | Lento pero mejor calidad |

### Identificación

TTS Notify marca automáticamente las voces Enhanced/Premium:

```bash
tts-notify --list

# Salida muestra categorías:
Enhanced/Premium (12 voces):
  • Angélica (Enhanced)    • Jorge (Enhanced)
  • Mónica (Enhanced)      • Francisca (Enhanced)
  • ...
```

## Voces en Otros Idiomas

### Inglés (Americano)

| Voz | Tipo | Uso |
|-----|------|-----|
| **Samantha** | Premium | Voz femenina principal |
| **Alex** | Enhanced | Masculina estándar |
| **Victoria** | Enhanced | Clara/profesional |
| **Daniel** | Premium | Noticias |
| **Karen** | Enhanced | Conversacional |
| **Moira** | Enhanced | Irlandesa |

### Inglés (Británico)

| Voz | Tipo | Uso |
|-----|------|-----|
| **Daniel** | Enhanced | Estándar británico |
| **Karen** | Enhanced | Femenina británica |
| **Serena** | Enhanced | Formal |

### Otros Idiomas

```bash
# Listar voces por idioma específico
say -v ? | grep -i "franco"  # Francés
say -v ? | grep -i "deutsch"  # Alemán
say -v ? | grep -i "italiano"  # Italiano
```

## Instalación de Voces Adicionales

### Via Preferencias del Sistema

```bash
# Abrir preferencias de voz
open "x-apple.systempreferences:com.apple.preference.speech?Synthesizing"
```

1. **Sistema Preferencias** → **Accesibilidad** → **Voz**
2. **Voz del Sistema** → **Personalizar...**
3. **Descargar voces adicionales**

### Via Terminal

```bash
# Listar voces disponibles para descarga
sudo softwareupdate --list

# Descargar voces específicas (ejemplos)
sudo softwareupdate --install "Voice Data Spanish (Mexico)"
sudo softwareupdate --install "Voice Data Spanish (Spain)"

# Instalar todas las voces
sudo softwareupdate --install-all
```

### Vozy Descargables

Algunas voces requieren descarga específica:

- **Voz Enhanced**: ~50-100MB por voz
- **Voz Premium**: ~200-500MB por voz
- **Voz Siri**: ~300MB por voz

## Configuración por Región

### España

```bash
export TTS_DEFAULT_VOICE="Jorge"
export TTS_SPANISH_REGION="es-ES"
```

### México

```bash
export TTS_DEFAULT_VOICE="Angélica"
export TTS_SPANISH_REGION="es-MX"
```

### Argentina

```bash
export TTS_DEFAULT_VOICE="Diego"
export TTS_SPANISH_REGION="es-AR"
```

## Optimización de Uso

### Selección por Tipo de Contenido

```bash
# Noticias/Información
tts-notify --voice "Jorge" "Noticias del día..."

# Narración/Storytelling
tts-notify --voice "Monica" "Érase una vez..."

# Alertas/Notificaciones
tts-notify --voice "Siri Female" "Alerta importante"

# Conversación informal
tts-notify --voice "Eddy" "¿Qué tal amigo?"

# Lectura técnica
tts-notify --voice "Marisol" "El protocolo TCP/IP..."
```

### Ajuste de Velocidad por Voz

```bash
# Voces Premium (pueden hablar más rápido)
tts-notify --voice "Jorge" --rate 200 "Texto rápido"

# Voces Standard (mejor velocidad moderada)
tts-notify --voice "Monica" --rate 175 "Texto normal"

# Voces Siri (soportan alta velocidad)
tts-notify --voice "Siri Female" --rate 250 "Texto muy rápido"
```

## Solución de Problemas

### Voz No Disponible

```bash
# Verificar si voz existe
say -v "NombreVoz" "test" 2>&1

# Salida si no existe:
# Voice "NombreVoz" is not a valid voice.

# Encontrar voces similares
say -v ? | grep -i "parte_del_nombre"
```

### Calidad de Audio

```bash
# Probar diferentes calidades
tts-notify --voice "Monica" "Standard voice"
tts-notify --voice "Mónica (Enhanced)" "Enhanced voice"

# Verificar diferencia
say -v ? | grep Monica
# Monica     es-ES    _# Standard Quality
# Mónica     es-ES    _# Enhanced Quality
```

### Problemas de Región

```bash
# Verificar configuración regional
defaults read -g AppleLocale

# Forzar configuración española
defaults write -g AppleLocale "es_ES"
```

## Referencia Rápida

### Voces Recomendadas

| Propósito | Voz | Comando |
|-----------|-----|---------|
| **Uso general** | Jorge | `tts-notify --voice Jorge` |
| **Voz femenina** | Angélica | `tts-notify --voice Angelica` |
| **Alta calidad** | Mónica Enhanced | `tts-notify --voice "Mónica (Enhanced)"` |
| **Rápida/Alerta** | Siri Female | `tts-notify --voice "Siri Female"` |
| **Noticias** | Carlos | `tts-notify --voice Carlos` |
| **Conversacional** | Eddy | `tts-notify --voice Eddy` |
| **Fallback universal** | Monica | `tts-notify --voice Monica` |

### Comandos Útiles

```bash
# Ver todas las voces españolas
say -v ? | grep -i -E "(spanish|español)"

# Contar voces totales
say -v ? | wc -l

# Probar voz específica
say -v Jorge "Hola, soy Jorge"

# Buscar voces por substring
say -v ? | grep -i mon

# Ver metadata completa
say -v ? | head -20
```

Esta referencia proporciona toda la información necesaria para aprovechar al máximo las capacidades de voz de macOS con TTS Notify.