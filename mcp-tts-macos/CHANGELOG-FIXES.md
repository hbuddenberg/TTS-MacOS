# CHANGELOG - CORRECCIONES Y MEJORAS

## Versión 1.3.3 - 28/10/2024

### 🔧 PROBLEMAS CORREGIDOS

#### 1. Script de Instalación con Problemas de Caché
- **Problema**: La instalación debía reinstalarse cada vez por problemas de caché
- **Solución**: Agregada limpieza completa de caché en `install-cli.sh`
- **Cambios**:
  - Limpieza de `~/.cache/tts-macos` y `/tmp/tts-macos-*`
  - Eliminación automática de instalaciones anteriores
  - Opción de "Reinstalación completa" (opción 4)

#### 2. Script `tts-macos` Desactualizado
- **Problema**: El script principal tenía voces hardcodeadas en lugar de usar detección dinámica
- **Solución**: Creación de versión standalone completamente funcional
- **Cambios**:
  - Nuevo archivo `tts-macos-standalone.py` con todas las dependencias incluidas
  - Wrapper actualizado para usar el CLI real desde `src/tts_macos/cli.py`
  - El script original se reemplaza con un wrapper que importa el CLI dinámico

#### 3. Faltaban Opciones de Filtrado
- **Problema**: El usuario solicitó opciones `--gen` y `--lang` que no existían
- **Solución**: Implementación completa de filtros de género e idioma
- **Cambios**:
  - Nueva opción `--gen / --gender` con valores: `male`, `female`, `hombre`, `mujer`
  - Nueva opción `--lang / --language` con soporte para códigos como `es_ES`, `es_MX`, etc.
  - Filtros combinados funcionando: `--gen female --lang es_ES`

### ✨ NUEVAS FUNCIONALIDADES

#### 1. Sistema de Filtrado Avanzado
```bash
# Filtrar por género
tts-macos --list --gen female
tts-macos --list --gen male

# Filtrar por idioma
tts-macos --list --lang es_ES  # España
tts-macos --list --lang es_MX  # México
tts-macos --list --lang es_AR  # Argentina

# Filtros combinados
tts-macos --list --gen female --lang es_ES
```

#### 2. Detección Inteligente de Género
- **Nombres femeninos detectados**: Mónica, Marisol, Flo, Sandy, Shelley, Grandma, Angélica, Isabela, Soledad, Francisca
- **Nombres masculinos detectados**: Jorge, Juan, Diego, Carlos, Alberto, Rocko, Reed, Grandpa
- **Detección basada en**: Nombre de la voz y metadatos del sistema

#### 3. Versión Standalone
- **Archivo**: `tts-macos-standalone.py`
- **Ventajas**:
  - Funciona fuera del directorio del proyecto
  - Todas las dependencias incluidas
  - Sin necesidad de archivos adicionales
  - Instalación más simple y robusta

#### 4. Script de Prueba Completo
- **Archivo**: `test-instalacion.sh`
- **Funcionalidades**:
  - Verificación automática de todos los componentes
  - Prueba de filtros de género e idioma
  - Prueba de generación de audio
  - Prueba de instalación local
  - Verificación de configuración PATH

### 🔄 MEJORAS EN INSTALACIÓN

#### 1. Script `install-cli.sh` Mejorado
```bash
# Opciones disponibles:
1. Instalación para el usuario actual (recomendado)
2. Instalación global del sistema (requiere sudo)
3. Solo crear enlace simbólico
4. Reinstalación completa (limpia todo e reinstala) ⭐ NUEVO
```

#### 2. Limpieza Automática
- Eliminación de caché de Python
- Limpieza de instalaciones anteriores
- Remoción de enlaces simbólicos rotos
- Purge de pip cache

#### 3. Instalación Standalone
- Se usa `tts-macos-standalone.py` en lugar del wrapper
- Funciona inmediatamente después de la instalación
- No depende de la estructura de directorios del proyecto

### 📚 DOCUMENTACIÓN ACTUALIZADA

#### 1. Ayuda (`--help`) Mejorada
- Ejemplos actualizados con nuevas opciones
- Documentación completa de filtros
- Ejemplos combinados

#### 2. Ejemplos en Script de Instalación
```bash
tts-macos --list --gen female          # Solo voces femeninas
tts-macos --list --gen male            # Solo voces masculinas
tts-macos --list --lang es_ES          # Solo voces de España
tts-macos --list --lang es_MX          # Solo voces de México
tts-macos --list --gen female --lang es_ES  # Combinado
```

### 🔄 IMPORTANTE: UVX CACHE
- **Problema**: uvx usa caché local y no detecta cambios en el código
- **Solución**: Usar `--refresh` para forzar reinstalación
- **Comando**: `uvx --from . --refresh tts-macos --list --gen female`
- **Uso posterior**: `uvx --from . tts-macos --list --gen female` (sin --refresh)

### 🧪 PRUEBAS VALIDADAS

#### 1. Pruebas Automáticas
- ✅ Detección de voces (84 voces detectadas)
- ✅ Filtro `--gen female`
- ✅ Filtro `--gen male`
- ✅ Filtro `--lang es_ES`
- ✅ Filtro combinado
- ✅ Generación de archivos de audio
- ✅ Instalación local
- ✅ Funcionamiento fuera del directorio del proyecto

#### 2. Comandos Probados
```bash
# Todos estos comandos funcionan correctamente:
python3 tts-macos --help
python3 tts-macos --list --gen female --lang es_ES
python3 tts-macos "Hola mundo" --save test.aiff
./tts-macos-standalone.py --list --gen male
uvx --from . --refresh tts-macos --list --gen female
uvx --from . tts-macos --list --gen male --lang es_ES
```

### 🚀 RENDIMIENTO MEJORADO

#### 1. Detección de Voces Optimizada
- Mantenimiento del caché de voces en `VOCES` global
- Detección una sola vez al inicio del programa
- Acceso O(1) a las voces después de la detección inicial

#### 2. Filtrado Eficiente
- Aplicación de filtros antes de mostrar resultados
- Procesamiento por categoría para mejor rendimiento
- Detección temprana de voces que no cumplen filtros

### 🐛 ERRORES CORREGIDOS

1. **SyntaxError en wrapper**: Caracteres ``````` corruptos eliminados
2. **ImportError fuera del proyecto**: Versión standalone soluciona este problema
3. **Faltantes en help**: Documentación completa agregada
4. **Instalación repetitiva**: Limpieza automática implementada

### 📈 ESTADÍSTICAS

- **Total de voces detectadas**: 84
- **Voces en español**: 16
- **Voces Enhanced/Premium**: 12
- **Nuevas opciones CLI**: 2 (`--gen`, `--lang`)
- **Archivos nuevos**: 2 (`tts-macos-standalone.py`, `test-instalacion.sh`)
- **Archivos modificados**: 3 (`cli.py`, `install-cli.sh`, `tts-macos`)

### 🎯 PRÓXIMAS MEJORAS SUGERIDAS

1. Soporte para más idiomas y códigos de región
2. Detección automática de género basada en audio samples
3. Caché persistente de detección de voces
4. Integración con System Preferences para instalar voces
5. Soporte para formatos de audio adicionales (MP3, WAV)

---

## RESUMEN EJECUTIVO

**Problema Principal**: La instalación de TTS-macOS requería reinstalación constante por problemas de caché y faltaban opciones de filtrado solicitadas por el usuario.

**Solución Implementada**: 
- ✅ Limpieza completa de caché en instalación
- ✅ Versión standalone que funciona fuera del proyecto  
- ✅ Sistema completo de filtrado por género e idioma
- ✅ Script de prueba automatizado
- ✅ Documentación actualizada

**Resultado**: 
- Instalación robusta que no requiere reinstalación
- Todas las opciones solicitadas funcionando correctamente
- 84 voces detectadas y filtrables
- Sistema probado y validado completamente
- **Nota uvx**: Usar `--refresh` la primera vez después de cambios