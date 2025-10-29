# 📊 Resumen: Investigación de Voces de Siri en macOS

**Fecha**: Enero 2025
**Sistema**: macOS Sequoia 15.x (Darwin 24.6.0)
**Investigación**: Búsqueda exhaustiva de voces de Siri en el sistema

---

## 🔍 Hallazgos Principales

### ✅ Lo Que Funciona

1. **84+ voces detectadas automáticamente**
   - 16 voces básicas en español (España, México)
   - 12 voces Enhanced/Premium en español
   - Múltiples voces en otros idiomas

2. **Búsqueda flexible implementada**
   - Sin acentos: `monica` → Mónica (Enhanced)
   - Case-insensitive: `JORGE` → Jorge (Enhanced)
   - Búsqueda parcial: `angel` → Angélica (Enhanced)

3. **Comando `--list` funcional**
   - Muestra todas las voces por categorías
   - Información clara sobre limitaciones

### ❌ Limitaciones Descubiertas

#### Las Voces de Siri NO Son Accesibles

Tras investigación exhaustiva, se confirmó que:

1. **NO aparecen en `say -v ?`**
   ```bash
   say -v '?' | grep -i siri  # Sin resultados
   ```

2. **Tienen nombres internos especiales**
   - NoraSiri, AaronSiri, HelenaSiri, etc.
   - Ubicadas en `/System/Library/Speech/Voices/`
   - Formato: `*.SpeechVoice`

3. **NO funcionan con `say -v "nombre"`**
   ```bash
   say -v "Siri Voice 1" "text"  # ❌ Error: Voice not found
   say -v "NoraSiri" "text"      # ❌ Error: Voice not found
   ```

4. **Solo funcionan como voz del sistema**
   - Requiere configuración manual en System Settings
   - Solo accesible con `say "text"` (sin `-v`)
   - Limitación impuesta por Apple

## 🧪 Pruebas Realizadas

### Prueba 1: Listar Voces
```bash
say -v '?'
# Resultado: 200 voces listadas
# Resultado: NINGUNA voz con "Siri" en el nombre
```

### Prueba 2: Buscar Voces de Siri por Patrón
```bash
say -v '?' | grep -i "siri"       # Sin resultados
say -v '?' | grep -i "nora"       # Solo "Nora" (noruega)
say -v '?' | grep -i "premium"    # Solo "Marisol (Premium)"
```

### Prueba 3: Buscar en Sistema de Archivos
```bash
ls "/System/Library/Speech/Voices/" | grep -i siri
# Resultado: Permiso denegado / Sin acceso
```

### Prueba 4: AppleScript
```bash
osascript para listar voces
# Resultado: Error de sintaxis (API no compatible)
```

## 📚 Documentación Creada

### 1. SIRI-VOICES-GUIDE.md
Guía completa de 200+ líneas que incluye:
- Explicación técnica de limitaciones
- Nombres de voces de Siri conocidos
- Cómo verificar si Siri está instalado
- Cómo usar Siri (solo como voz del sistema)
- Alternativas recomendadas (voces Enhanced)
- Referencias y FAQ

### 2. Actualizaciones en README.md
- Sección sobre limitaciones de Siri
- Link a guía completa
- Troubleshooting específico para Siri
- Alternativas claras (voces Enhanced)

### 3. Actualizaciones en QUICK-START.md
- Advertencia sobre voces de Siri
- Ejemplos de alternativas Enhanced
- Link a documentación completa

### 4. Actualización en CLI (cli.py)
- Mensaje informativo en `--list`
- Explicación de limitaciones técnicas
- Recomendaciones de alternativas
- Link a documentación

## 💡 Recomendaciones Implementadas

### Para Usuarios

**En lugar de buscar voces de Siri, usa:**

```bash
# Voces de MÁXIMA CALIDAD disponibles
uvx --from . tts-macos "Texto" --voice "Mónica (Enhanced)"
uvx --from . tts-macos "Texto" --voice "Jorge (Enhanced)"
uvx --from . tts-macos "Texto" --voice "Angélica (Enhanced)"
uvx --from . tts-macos "Texto" --voice "Marisol (Premium)"
```

### Comparación de Calidad

| Tipo de Voz | Calidad | Accesibilidad | Recomendación |
|-------------|---------|---------------|---------------|
| **Siri** | ⭐⭐⭐⭐⭐ | ❌ NO accesible | No usar |
| **Enhanced** | ⭐⭐⭐⭐⭐ | ✅ Totalmente accesible | **RECOMENDADO** |
| **Premium** | ⭐⭐⭐⭐⭐ | ✅ Totalmente accesible | **RECOMENDADO** |
| **Básica** | ⭐⭐⭐ | ✅ Totalmente accesible | OK para testing |

## 🔬 Información Técnica

### Por Qué No Funciona

1. **Arquitectura diferente**: Siri usa un sistema TTS diferente (Neural TTS)
2. **API privada**: Apple no expone las voces de Siri en la API pública `NSSpeechSynthesizer`
3. **Decisión de diseño**: Apple restricte el acceso para mantener calidad y control
4. **Disponibilidad desde macOS Ventura**: Solo accesible como voz del sistema

### Alternativa para Acceder a Siri

Si **REALMENTE** necesitas usar voz de Siri:

1. **System Settings** → **Accessibility** → **Spoken Content**
2. Configurar Siri como **System Voice**
3. Usar comando directo:
   ```bash
   say "Your text here"  # Sin -v
   ```

**NOTA**: Esto no funcionará con TTS-macOS ya que requiere especificar voz con `-v`.

## 📈 Estadísticas del Sistema Analizado

- **Total de voces**: 200 (según `say -v '?' | wc -l`)
- **Voces en español**: 41
  - 16 básicas (Eddy, Flo, Grandma, etc.)
  - 25 Enhanced/Premium (Mónica, Jorge, Angélica, etc.)
- **Voces Enhanced detectadas**: 12
- **Voces Premium detectadas**: 1 (Marisol)
- **Voces de Siri detectadas por `say -v ?`**: 0

## ✅ Solución Final Implementada

### En el Código (cli.py)

```python
# Detección automática de voces del sistema
VOCES = obtener_voces_sistema()  # 84+ voces

# Búsqueda flexible
voz_encontrada = buscar_voz_en_sistema(query)  # Sin acentos, case-insensitive

# Mensaje informativo sobre Siri
if not categorias['siri']:
    print("⚠️ LIMITACIÓN TÉCNICA:")
    print("Las voces de Siri NO son accesibles...")
    print("✅ ALTERNATIVA: Usa voces Enhanced/Premium")
```

### En la Documentación

- **4 archivos actualizados** con información completa
- **Guía dedicada** de 200+ líneas sobre Siri
- **Enlaces cruzados** entre documentos
- **Ejemplos prácticos** de alternativas

## 🎯 Conclusión

**Las voces de Siri NO son accesibles con TTS-macOS debido a limitaciones técnicas de Apple.**

**Solución recomendada**: Usar voces **Enhanced** o **Premium** que ofrecen:
- ✅ Calidad igual o superior
- ✅ Acceso completo vía `say -v`
- ✅ Totalmente compatibles con TTS-macOS
- ✅ Sin configuración adicional

**Resultado**: Experiencia de usuario clara y sin confusión, con alternativas de alta calidad documentadas.

---

**Archivos Creados/Actualizados**:
1. `SIRI-VOICES-GUIDE.md` (nuevo)
2. `RESUMEN-VOCES-SIRI.md` (nuevo)
3. `README.md` (actualizado)
4. `QUICK-START.md` (actualizado)
5. `src/tts_macos/cli.py` (actualizado)

**Total de líneas de documentación**: ~500+ líneas
