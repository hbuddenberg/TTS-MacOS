# Configuración Global de MCP Server TTS-Notify en Claude Code

Este documento explica cómo configurar un servidor MCP (Model Context Protocol) globalmente para que esté disponible en todos los proyectos de Claude Code.

## 🎯 Objetivo

Configurar el servidor `tts-notify` a nivel de usuario para que esté disponible en todos los proyectos sin necesidad de configurarlo individualmente en cada uno.

## 📋 Prerrequisitos

- Claude Code instalado
- Acceso a terminal/comandos del sistema
- Proyecto TTS-Notify con entorno virtual configurado
- Python y entorno virtual funcionando

## 🔧 Proceso de Configuración Global

### 1. Verificar Configuración Actual

Primero, verificar si existe alguna configuración previa:

```bash
claude mcp list
```

### 2. Eliminar Configuraciones Existentes (si las hay)

Si existe configuración local o de proyecto, eliminarla:

```bash
# Eliminar configuración de proyecto (si existe)
claude mcp remove tts-notify -s project

# Eliminar configuración de usuario (si existe)
claude mcp remove tts-notify -s user
```

### 3. Configurar el Servidor Globalmente

Agregar el servidor MCP con scope `user` y todas las variables de entorno necesarias:

```bash
claude mcp add --scope user tts-notify --transport stdio \
  --env TTS_NOTIFY_VOICE="Siri Female (Spanish Spain)" \
  --env TTS_NOTIFY_RATE=175 \
  --env TTS_NOTIFY_LANGUAGE=es \
  --env TTS_NOTIFY_QUALITY=siri \
  -- "/ruta/a/tu/entorno/virtual/bin/python" "-m" "tts_notify" "--mode" "mcp"
```

**Reemplazar** `/ruta/a/tu/entorno/virtual/bin/python` con la ruta real de tu entorno virtual.

### 4. Verificar la Configuración

Verificar que el servidor está correctamente configurado y conectado:

```bash
claude mcp list
```

La salida debería mostrar:
```
tts-notify: /ruta/al/python -m tts_notify --mode mcp - ✓ Connected
```

## 📁 Estructura de Archivos

### Archivos Modificados

1. **`~/.claude.json`**: Configuración global de usuario
   - Agrega la sección `mcpServers` con la configuración del servidor

2. **`~/.claude/.mcp.json`**: Configuración local (eliminada)
   - Se elimina para evitar conflictos

### Formato JSON

La configuración final en `~/.claude.json` se ve así:

```json
{
  "mcpServers": {
    "tts-notify": {
      "type": "stdio",
      "command": "/ruta/a/tu/entorno/virtual/bin/python",
      "args": [
        "-m",
        "tts_notify",
        "--mode",
        "mcp"
      ],
      "env": {
        "TTS_NOTIFY_VOICE": "Siri Female (Spanish Spain)",
        "TTS_NOTIFY_RATE": "175",
        "TTS_NOTIFY_LANGUAGE": "es",
        "TTS_NOTIFY_QUALITY": "siri"
      }
    }
  }
}
```

## 🧪 Testing y Verificación

### Probar Funciones Básicas

1. **Listar voces disponibles**:
   ```javascript
   mcp__tts-notify__list_voices()
   ```

2. **Probar texto a voz**:
   ```javascript
   mcp__tts-notify__speak_text({
     text: "¡Hola! Esto es una prueba del servidor TTS-Notify",
     voice: "Siri Female (Spanish Spain)",
     rate: 175
   })
   ```

3. **Guardar audio en archivo**:
   ```javascript
   mcp__tts-notify__save_audio({
     text: "Este audio se guardará en un archivo",
     output_path: "/ruta/a/archivo.aiff",
     voice: "Siri Female (Spanish Spain)",
     rate: 175
   })
   ```

## 🔍 Troubleshooting

### Problema: No aparece en `/mcp`

**Solución**: Verificar que el servidor está configurado a nivel de usuario:
```bash
claude mcp list
```

### Problema: Error de conexión

**Solución**: Verificar la ruta al ejecutable de Python:
```bash
# Verificar que la ruta es correcta
/ruta/a/tu/entorno/virtual/bin/python --version

# Verificar que el módulo está instalado
/ruta/a/tu/entorno/virtual/bin/python -m tts_notify --help
```

### Problema: Variables de entorno no aplicadas

**Solución**: Eliminar y volver a agregar el servidor con las variables correctas:
```bash
claude mcp remove tts-notify -s user
claude mcp add --scope user tts-notify --transport stdio \
  --env VAR1="valor1" --env VAR2="valor2" \
  -- "/ruta/al/python" "-m" "tts_notify" "--mode" "mcp"
```

## 🚀 Comandos Útiles

### Listar todos los servidores MCP
```bash
claude mcp list
```

### Eliminar servidor
```bash
claude mcp remove tts-notify -s user
```

### Verificar estado de salud
```bash
claude mcp doctor
```

### Mostrar detalles de un servidor
```bash
claude mcp view tts-notify
```

## 📚 Referencias

- [Documentación oficial de Claude Code MCP](https://code.claude.com/docs/en/mcp)
- [Guía de configuración de MCP servers](https://code.claude.com/docs/en/mcp/configuration)

## 🎉 Resultado Final

Una vez completado el proceso:

- ✅ El servidor `tts-notify` está disponible **globalmente**
- ✅ Funciona en **cualquier proyecto** sin configuración adicional
- ✅ Las herramientas MCP están disponibles como:
  - `mcp__tts-notify__speak_text`
  - `mcp__tts-notify__list_voices`
  - `mcp__tts-notify__save_audio`
- ✅ Configuración centralizada y reutilizable

## 🔄 Para Otros Proyectos

Para implementar esta configuración en otros proyectos:

1. Copiar el comando de configuración con la ruta correcta del entorno virtual
2. Ejecutar los comandos en la secuencia mostrada
3. Verificar con las pruebas de funcionalidad

## 📝 Notas Importantes

- La configuración con `--scope user` es **persistente** entre sesiones
- No requiere configuración por proyecto
- Las variables de entorno se establecen una vez y se aplican globalmente
- El servidor debe estar accesible en la ruta especificada
- El entorno virtual debe contener el módulo `tts_notify` instalado