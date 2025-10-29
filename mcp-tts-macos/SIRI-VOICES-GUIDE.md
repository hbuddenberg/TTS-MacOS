# 🤖 Guía Completa: Voces de Siri en macOS

## 📋 Información Importante

Las **voces de Siri** tienen limitaciones técnicas en macOS que afectan cómo pueden usarse con el comando `say` y herramientas TTS:

### ❌ Limitaciones Técnicas

1. **NO aparecen en `say -v ?`** - Las voces de Siri no se listan en el comando estándar
2. **NO se pueden usar con `say -v "nombre"`** - El flag `-v` no funciona con voces de Siri
3. **Requieren configuración especial** - Solo funcionan como voz del sistema
4. **Disponibles desde macOS Ventura (13.0+)** - Versiones anteriores no soportan esta funcionalidad

### ✅ Qué SÍ Funciona

- Usar voces de Siri **SOLO** como voz del sistema (sin especificar `-v`)
- Funciona en macOS Ventura, Sonoma y Sequoia
- Se puede usar con `say "texto"` (sin el flag `-v`)

## 🔍 Voces de Siri Disponibles

Las voces de Siri tienen nombres internos que incluyen:

### Voces en Inglés (EE.UU.)
- **NoraSiri** - Femenina (Voice 1)
- **AaronSiri** - Masculina (Voice 2)
- **EvanSiri** - Masculina (Voice 3)
- **ShelleySiri** - Femenina (Voice 4)

### Voces en Otros Idiomas
- **HelenaSiri** - Alemán
- **YelenaSiri** - Ruso
- Y más voces de Siri en diferentes idiomas

### Voces en Español
Apple no ha publicado voces de Siri específicamente para español en el mismo nivel que las voces en inglés. Sin embargo, puedes usar las **voces Enhanced** que ofrecen calidad similar:

- **Mónica (Enhanced)** - España
- **Angélica (Enhanced)** - México
- **Jorge (Enhanced)** - España
- **Paulina (Enhanced)** - México
- **Juan (Enhanced)** - México
- **Diego (Enhanced)** - Argentina
- **Carlos (Enhanced)** - Colombia
- **Francisca (Enhanced)** - Chile

## 🛠️ Cómo Verificar si Tienes Voces de Siri Instaladas

### Método 1: Configuraciones del Sistema

1. Abre **Configuraciones del Sistema** (System Settings)
2. Ve a **Accesibilidad** (Accessibility)
3. Selecciona **Contenido Hablado** (Spoken Content)
4. Haz clic en **Voz del Sistema** (System Voice)
5. Busca voces que digan "Siri" en el nombre (por ejemplo: "Siri Voice 1", "Siri Voice 2")

### Método 2: Verificar en el Directorio del Sistema

Las voces de Siri se almacenan en:
```bash
/System/Library/Speech/Voices/
```

Con nombres como:
- `NoraSiri.SpeechVoice`
- `AaronSiri.SpeechVoice`
- `HelenaSiri.SpeechVoice`

## 🎤 Cómo Usar Voces de Siri

### Paso 1: Instalar Voces de Siri (si no están instaladas)

1. **Configuraciones del Sistema** → **Accesibilidad** → **Contenido Hablado**
2. Haz clic en **Voz del Sistema**
3. Haz clic en **Administrar Voces** (Manage Voices)
4. Busca las voces de Siri disponibles para tu idioma
5. Haz clic en el botón de descarga (⬇️) junto a cada voz

### Paso 2: Configurar como Voz del Sistema

1. **Configuraciones del Sistema** → **Accesibilidad** → **Contenido Hablado**
2. Haz clic en **Voz del Sistema**
3. Selecciona una voz de Siri (por ejemplo: "Siri Voice 1 (Nora)")
4. Haz clic en **Aceptar**

### Paso 3: Usar con el Comando `say`

Una vez configurada como voz del sistema:

```bash
# ✅ ESTO FUNCIONA - sin especificar voz
say "Hello, this is Siri speaking"

# ❌ ESTO NO FUNCIONA - con flag -v
say -v "Siri Voice 1" "Hello"  # Error: Voice not found
say -v "NoraSiri" "Hello"       # Error: Voice not found
```

## 🚫 Por Qué TTS-macOS No Puede Usar Voces de Siri Directamente

### Limitación Técnica de Apple

Apple ha diseñado las voces de Siri de manera que:

1. **No son accesibles mediante la API estándar de TTS** (`NSSpeechSynthesizer`)
2. **No aparecen en la lista de voces disponibles** con `say -v ?`
3. **Requieren ser la voz del sistema** para funcionar
4. **No se pueden especificar por nombre** con el flag `-v`

### Impacto en TTS-macOS

Como TTS-macOS usa el comando `say -v "nombre"` para especificar voces:

```python
# Así funciona TTS-macOS
subprocess.run(["say", "-v", "Mónica (Enhanced)", "-r", "175", texto])
```

Y las voces de Siri **NO soportan** el flag `-v`, esto significa que:

- ✅ TTS-macOS detecta y usa: **84+ voces estándar** (Enhanced, Premium, básicas)
- ❌ TTS-macOS NO puede detectar ni usar: **Voces de Siri**

## 💡 Alternativas Recomendadas

### Usa Voces Enhanced en Español (Calidad Similar a Siri)

Las voces **Enhanced** ofrecen calidad profesional muy similar a Siri:

```bash
# Voz femenina española - excelente calidad
uvx --from . tts-macos "Hola mundo" --voice "Mónica (Enhanced)"

# Voz masculina española - muy natural
uvx --from . tts-macos "Hola mundo" --voice "Jorge (Enhanced)"

# Voz femenina mexicana - profesional
uvx --from . tts-macos "Hola mundo" --voice "Angélica (Enhanced)"
```

### Comparación de Calidad

```bash
# Probar diferentes calidades
uvx --from . tts-macos "Esta es la voz básica" --voice "Eddy (Español (España))"
uvx --from . tts-macos "Esta es la voz Enhanced" --voice "Mónica (Enhanced)"
uvx --from . tts-macos "Esta es la voz Premium" --voice "Marisol (Premium)"
```

## 🎯 Recomendación Final

### Para Uso General con TTS-macOS

**Usa voces Enhanced/Premium** en lugar de Siri:

```bash
# Mejor opción para español
uvx --from . tts-macos --list  # Ver todas las voces Enhanced

# Ejemplos recomendados
uvx --from . tts-macos "Mensaje profesional" --voice "Jorge (Enhanced)"
uvx --from . tts-macos "Audio de calidad" --voice "Mónica (Enhanced)"
```

### Si NECESITAS Usar Voces de Siri Específicamente

1. **Configúrala como voz del sistema** en Configuraciones
2. **Usa el comando `say` directamente** (sin TTS-macOS):

```bash
# Configurar Siri como voz del sistema primero
# Luego usar:
say "Your text here"

# O guardar audio:
say -o ~/Desktop/siri_audio.aiff "Your text here"
```

## 📚 Referencias

- [Stack Overflow: Make say work with Siri voices](https://stackoverflow.com/questions/61122378/)
- [Apple Community: Siri voices with say command](https://discussions.apple.com/thread/251273481)
- [Documentación oficial de macOS sobre `say`](https://ss64.com/mac/say.html)

## 🆘 Preguntas Frecuentes

### ¿Por qué no aparecen las voces de Siri en `say -v ?`?

Es una decisión de diseño de Apple. Las voces de Siri usan un sistema diferente al TTS estándar de macOS.

### ¿Se puede forzar el uso de voces de Siri?

No. Apple no proporciona una API pública para usar voces de Siri directamente con el flag `-v`.

### ¿Las voces Enhanced son tan buenas como Siri?

Sí, las voces **Enhanced** y **Premium** ofrecen calidad muy alta, comparable a Siri en muchos casos.

### ¿Funcionará en futuras versiones de macOS?

Esto depende de Apple. Por ahora, la recomendación es usar voces Enhanced/Premium para máxima compatibilidad.

---

**Última actualización**: Enero 2025 - macOS Sequoia (15.x)
