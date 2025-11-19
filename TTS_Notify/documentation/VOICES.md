# Referencia de Voces - TTS Notify

Guía completa de voces disponibles en macOS y cómo usarlas con TTS Notify v1.5.0.

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