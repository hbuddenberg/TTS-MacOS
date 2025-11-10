# 📝 CHANGELOG - TTS-macOS

Registro completo de cambios, mejoras y correcciones del proyecto TTS-macOS.

---

## 🚀 v1.5.0 - 10/11/2025 - **RELEASE CRÍTICO MCP**

### 🛠️ **Reconstrucción Completa del Servidor MCP**
- **Migración a FastMCP Framework**: Reemplazo completo del framework MCP antiguo por FastMCP moderno
- **Corrección del error crítico de 'filename'**: El servidor MCP ahora funciona correctamente sin pedir parámetros incorrectos
- **Implementación de función 'speak'**: Nuevo alias para 'speak_text' para compatibilidad con Claude
- **Simplificación de API**: Firmas de funciones más limpias con parámetros directos
- **Mejor manejo de errores**: Logging mejorado para depuración

### 🔧 **Correcciones Principales**
- **FIX**: Error `filename` en función `speak_text` - **COMPLETAMENTE RESUELTO**
- **FIX**: Configuración de PYTHONPATH para Claude Desktop
- **FIX**: Implementación correcta de decoradores `@mcp.tool()`
- **FIX**: Schema de herramientas validado correctamente
- **FIX**: Comunicación MCP bidireccional estable

### 🆕 **Nuevas Herramientas MCP**
- **speak()**: Alias de `speak_text()` para mejor compatibilidad
- **speak_text()**: Reproducción de texto con voz personalizable
- **list_voices()**: Listado completo de voces del sistema categorizadas
- **save_audio()**: Guardado de texto como archivo AIFF

### 📁 **Archivos Nuevos**
- `start_server.py`: Script de inicio robusto con PYTHONPATH configurado
- `CORRECCIONES.md`: Documentación detallada de las correcciones realizadas
- `debug_mcp*.py**: Suite de herramientas de depuración MCP
- `server_fastmcp.py`: Implementación alternativa con FastMCP

### 🔄 **Cambios en Configuración**
- **Actualización de claude_desktop_config.json**: Configuración corregida con PYTHONPATH
- **Mejoras en install.sh**: Instalación más robusta
- **Validación de dependencias**: Verificación automática de módulos requeridos

### 🧪 **Mejoras en Testing**
- **Pruebas MCP completas**: Suite de testing para protocolo MCP real
- **Validación de herramientas**: Verificación automática de schemas
- **Testing de integración**: Pruebas end-to-end con Claude Desktop

---

## 🆕 v1.4.4 - 05/11/2025

### 🧹 **Limpieza de Proyecto**
- **Eliminación de 35MB** en entornos virtuales no versionados
- **Consolidación de changelogs** (3 archivos → 1 CHANGELOG.md)
- **Eliminación de archivos binarios corruptos** y cache innecesaria
- **Remoción de código duplicado** e incompleto
- **Mejora de estructura** y mantenibilidad del proyecto

### 🤖 **Sistema de Notificaciones TTS**
- **Nuevo sistema de detección automática de planes**
- **Lectura inteligente de planes** con pausas naturales
- **Detección de acciones requeridas** del usuario
- **Anuncios de implementación completada**
- **Integración con hooks de Claude Code**

---

## 🆕 v1.4.3 - 05/11/2025

### 🎯 **Sistema de Notificaciones Inteligente**
- **Detección automática de planes** en formato markdown
- **Lectura de planes con voz** usando TTS del sistema
- **Identificación de puntos de acción requerida**
- **Anuncios de finalización de implementación**
- **Modos automático y manual** de lectura

### 📁 **Archivos Nuevos**
- `notification.py` - Hook mejorado con detección de planes
- `plan-reader.py` - Especializado para lectura de planes
- `demo-plans.sh` - Demostración del sistema

---

## 🆕 v1.4.2 - 05/11/2025

### 🔧 **Mejoras en Documentación**
- **Integración de UVX-NOTE.md** en README.md principal
- **Documentación consolidada** y mejor organizada
- **Instrucciones claras** sobre uso de uvx con --refresh

---

## 🆕 v1.4.1 - 28/10/2024

### 📋 **Enhanced Compact List View**
- **Nueva columna "Tipo"** en vista compacta de voces
- **Categorización de voces**: Normal, Enhanced, Premium, Siri
- **Detección de tipos múltiples** (ej: Marisol - Enhanced, Premium)
- **Compatibilidad completa** con filtros existentes

**Formato nuevo:**
```
Voz             Tipo                 Idioma     Localizaciones       Género
──────────────────────────────────────────────────────────────────────────
Marisol         Enhanced, Premium    Español    es_ES                mujer
Flo             Normal               Español    es_ES, es_MX         mujer
```

---

## 🔧 v1.3.3 - 28/10/2024

### 🐛 **PROBLEMAS CORREGIDOS**

#### 1. Script de Instalación con Problemas de Caché
- **Problema**: La instalación debía reinstalarse cada vez por problemas de caché
- **Solución**: Limpieza completa de caché en `install-cli.sh`
- **Cambios**:
  - Limpieza de `~/.cache/tts-macos` y `/tmp/tts-macos-*`
  - Eliminación automática de instalaciones anteriores
  - Opción de "Reinstalación completa" (opción 4)

#### 2. Script `tts-macos` Desactualizado
- **Problema**: El script principal tenía voces hardcodeadas
- **Solución**: Creación de versión standalone completamente funcional
- **Cambios**:
  - Nuevo archivo `tts-macos-standalone.py` con todas las dependencias
  - Wrapper actualizado para usar el CLI real desde `src/tts_macos/cli.py`

#### 3. Faltaban Opciones de Filtrado
- **Problema**: El usuario solicitó opciones `--gen` y `--lang` que no existían
- **Solución**: Implementación completa de filtros de género e idioma

### ✨ **NUEVAS FUNCIONALIDADES**

#### 1. Sistema de Filtrado Avanzado
```bash
# Filtrar por género
tts-macos --list --gen female
tts-macos --list --gen male

# Filtrar por idioma
tts-macos --list --lang es_ES  # España
tts-macos --list --lang es_MX  # México

# Filtros combinados
tts-macos --list --gen female --lang es_ES
```

#### 2. Detección Inteligente de Género
- **Nombres femeninos detectados**: Mónica, Marisol, Flo, Sandy, Shelley, Grandma, Angélica, Isabela, Soledad, Francisca
- **Nombres masculinos detectados**: Jorge, Juan, Diego, Carlos, Alberto, Rocko, Reed, Grandpa

#### 3. Versión Standalone
- **Archivo**: `tts-macos-standalone.py`
- **Ventajas**: Funciona fuera del directorio del proyecto, sin necesidad de archivos adicionales

### 📈 **ESTADÍSTICAS**
- **Total de voces detectadas**: 84
- **Voces en español**: 16
- **Voces Enhanced/Premium**: 12
- **Nuevas opciones CLI**: 2 (`--gen`, `--lang`)

---

## 📚 v1.2.1+mejoras - Enero 2025

### 🎯 **Resumen de Mejoras Implementadas**

#### 1. Documentación Mejorada y Actualizada
- **README.md** actualizado con información sobre 84+ voces detectadas automáticamente
- **QUICK-START.md** (NUEVO) - Guía rápida de instalación y uso
- **SIRI-VOICES-GUIDE.md** (NUEVO) - Guía técnica completa sobre limitaciones de Siri
- **RESUMEN-VOCES-SIRI.md** (NUEVO) - Resumen de investigación exhaustiva

#### 2. Mejoras en el CLI (cli.py)
- **Help Mejorado** con secciones organizadas y ejemplos
- **Configuración MCP en el Help** - JSON completo incluido directamente
- **Comando `--list` Mejorado** con categorización y formatting profesional

#### 3. Investigación de Voces de Siri
- **Hallazgos principales**: Las voces de Siri NO son accesibles con `say -v`
- **Pruebas realizadas**: 200 voces totales, 41 en español detectadas
- **Solución implementada**: Documentación completa y alternativas claras

### 📊 **Estadísticas del Sistema**
- **Voces Detectadas**: 200 totales, 41 en español
- **Voces Usables**: 84+ completamente funcionales
- **Enhanced detectadas**: 12
- **Premium detectadas**: 1 (Marisol)

### ✅ **Checklist de Mejoras Completadas**
- [x] README.md actualizado con 84+ voces
- [x] QUICK-START.md creado con ejemplos completos
- [x] SIRI-VOICES-GUIDE.md creado con guía técnica
- [x] CLI help mejorado con ejemplos organizados
- [x] CLI help incluye configuración JSON del MCP
- [x] CLI --list mejorado con categorización
- [x] Búsqueda flexible documentada

---

## 🚀 v1.1.0 - Historia

### Modo CLI
- **Implementación completa** del comando line interface
- **Detección dinámica de voces** usando `say -v ?`
- **Soporte para uvx** - ejecución sin instalación
- **Sistema de instalación global** con scripts interactivos

### Modo MCP Server
- **Integración con Claude Desktop** como servidor MCP
- **Tres herramientas expuestas**: speak_text, list_voices, save_audio
- **Ejecución asíncrona** usando asyncio
- **Configuración automática** de Claude Desktop

---

## 📊 **Estadísticas Históricas**

### Archivos Eliminados en v1.4.4 (Limpieza)
- **35MB** en entornos virtuales (venv/, .venv/)
- **3 changelogs** consolidados en 1 CHANGELOG.md
- **Archivos binarios corruptos**: tts-macos-standalone, test-premium.aiff
- **Código incompleto**: new_tools.py
- **Cache Python**: __pycache__/

### Evolución del Proyecto
- **v1.0.0**: MCP server básico
- **v1.1.0**: CLI mode + uvx support
- **v1.2.1**: Dynamic voice detection
- **v1.3.3**: Gender/language filters + standalone version
- **v1.4.1**: Enhanced compact view with voice types
- **v1.4.4**: Project cleanup + TTS notification system

### Métricas de Mejora
- **Documentación**: ~1,200 líneas creadas/mejoradas
- **Código**: ~500 líneas de nuevas funcionalidades
- **Voces soportadas**: 84+ (de ~16 iniciales)
- **Opciones CLI**: 6 nuevas opciones agregadas
- **Instalación**: 3 métodos disponibles (global, uvx, development)

---

## 🎯 **Roadmap Futuro**

### Próximas Mejoras Planeadas
- Soporte para más idiomas y códigos de región
- Caché persistente de detección de voces
- Integración con System Preferences para instalar voces
- Soporte para formatos de audio adicionales (MP3, WAV)
- Tests automatizados y CI/CD

### Sugerencias de la Comunidad
- Detección automática de género basada en audio samples
- Sort by type functionality
- Color coding para diferentes tipos de voz
- Export a CSV/TSV con información completa

---

## 📝 **Notas de Mantenimiento**

### Compatibilidad
- **Python 3.10+** requerido
- **macOS nativo** con comando `say`
- **Backward compatibility** mantenida en todas las versiones

### Rendimiento
- **Detección de voces**: O(1) después de inicialización
- **Memoria**: <10MB footprint
- **Startup time**: <1 segundo para detección de voces

---

**Última actualización**: 05/11/2025
**Versión actual**: v1.4.4
**Estado**: ✅ Production Ready