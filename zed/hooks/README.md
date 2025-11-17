# Hooks de TTS para Zed

Este directorio contiene hooks de notificación con TTS (Text-to-Speech) específicamente diseñados para el editor de código Zed. Los hooks usan TTS-macOS para proporcionar retroalimentación auditiva durante el uso de Zed.

## 📋 Tabla de Contenidos

1. [Configuración](#configuración)
2. [Hooks Disponibles](#hooks-disponibles)
3. [Cómo Usar](#cómo-usar)
4. [Integración con Zed](#integración-con-zed)
5. [Troubleshooting](#troubleshooting)
6. [Variables de Entorno](#variables-de-entorno)

## Configuración

### Requisitos
- TTS-macOS instalado: [Ver documentación](https://github.com/anthropics/claude-code/mcp-tts-macos)
- macOS con voces en español instaladas

### Configuración Rápida
```bash
cd /Volumes/Resources/Develop/TTS-MacOS/zed/hooks
./enable-tts.sh
```

### Configuración Manual
```bash
# Habilitar TTS
export ZED_TTS_ENABLED=true

# Voz para notificaciones de guardado
export ZED_TTS_VOICE="monica"

# Velocidad de habla (palabras por minuto)
export ZED_TTS_RATE="175"

# Voz para tareas complejas
export ZED_TTS_TASK_VOICE="jorge"

# Velocidad para tareas complejas
export ZED_TTS_TASK_RATE="180"

# Longitud máxima de texto para TTS
export ZED_TTS_MAX_LENGTH="100"

# Anunciar inicio de Zed
export ZED_STARTUP_ANNOUNCE="true"
```

Para hacer permanente la configuración, añade estas líneas a tu `~/.zshrc` o `~/.bashrc`.

## Hooks Disponibles

### 1. `file-save-complete`
Notifica cuando un archivo se guarda correctamente.

**Uso:**
```bash
# Simular guardado de archivo
echo "test" | ./file-save-complete test.py

# Directamente con nombre de archivo
./file-save-complete mi-script.sh
```

**Mensajes de Ejemplo:**
- "Archivo Python guardado exitosamente: script.py"
- "Documento Markdown guardado: README.md"
- "Script guardado: build.sh"

### 2. `task-complete`
Notifica cuando tareas complejas se completan.

**Uso:**
```bash
# Simular tarea de compilación
echo "build success" | ./task-complete build

# Simular tarea de pruebas
echo "test completed with errors" | ./task-complete test

# Directamente con operación y resultado
./task-complete lint "lint completed with warnings"
```

**Mensajes de Ejemplo:**
- "Compilación completada exitosamente"
- "Pruebas con errores, revisa la consola"
- "Análisis de código completada"

### 3. `startup-complete`
Notifica cuando Zed se inicia correctamente.

**Uso:**
```bash
# Simular inicio de Zed
./startup-complete

# Con nombre de proyecto
./startup-complete mi-proyecto
```

**Mensajes de Ejemplo:**
- "Zed listo, empezamos a programar"
- "Zed listo, proyecto: mi-proyecto"

## Cómo Usar

### Paso 1: Instalar TTS-macOS
```bash
cd /Volumes/Resources/Develop/TTS-MacOS
./install-cli.sh
```

### Paso 2: Configurar Hooks
```bash
cd zed/hooks
./enable-tts.sh
```

### Paso 3: Probar Hooks
```bash
# Probar guardado de archivo
echo "test" | ./file-save-complete test.py

# Probar tareas complejas
echo "build success" | ./task-complete build

# Probar inicio
./startup-complete mi-proyecto
```

### Paso 4: Deshabilitar (Opcional)
```bash
./disable-tts.sh
```

## Integración con Zed

### Opción 1: Usar Scripts como Comandos Preguntados
Puedes usar estos scripts directamente en Zed:

1. Abre Zed
2. Usa el panel de comandos (`Cmd+Shift+P`)
3. Ejecuta comandos como:
   - `Run Command: shell ./Volumes/Resources/Develop/TTS-MacOS/zed/hooks/startup-complete mi-proyecto`

### Opción 2: Configurar como Acciones Personalizadas
Puedes configurar estos hooks como acciones personalizadas en Zed:

```json
{
  "actions": {
    "notify-save": {
      "command": "./Volumes/Resources/Develop/TTS-MacOS/zed/hooks/file-save-complete",
      "args": ["${file}"]
    },
    "notify-build": {
      "command": "./Volumes/Resources/Develop/TTS-MacOS/zed/hooks/task-complete",
      "args": ["build", "success"]
    }
  }
}
```

### Opción 3: Uso Manual en Terminal
```bash
# Guardar archivo y notificar
tts-macos "Archivo guardado exitosamente" --voice monica --rate 175

# Completar tarea
tts-macos "Compilación completada" --voice jorge --rate 180
```

## Troubleshooting

### Problemas Comunes

#### 1. "tts-macos command not found"
```bash
# Verifica instalación
which tts-macos

# Si no está instalado
cd /Volumes/Resources/Develop/TTS-MacOS
./install-cli.sh
```

#### 2. "Voz no encontrada"
```bash
# Lista voces disponibles
say -v ? | grep -iE "(spanish|español)"

# Lista todas las voces
say -v ? | head -20
```

#### 3. "Hook no funciona"
```bash
# Verifica permisos del script
chmod +x ./file-save-complete
chmod +x ./task-complete
chmod +x ./startup-complete

# Prueba manualmente
echo "test" | ./file-save-complete test.py
```

#### 4. "Configuración no persiste"
```bash
 # Verifica que las variables estén en tu .zshrc
tail -10 ~/.zshrc

 # Carga manualmente
source ~/.zed/tts-config
```

### Verificar Configuración
```bash
# Verificar variables de entorno
echo "ZED_TTS_ENABLED: $ZED_TTS_ENABLED"
echo "ZED_TTS_VOICE: $ZED_TTS_VOICE"
echo "ZED_TTS_RATE: $ZED_TTS_RATE"

# Probar TTS directamente
tts-macos "Prueba de configuración" --voice monica --rate 175
```

## Variables de Entorno

| Variable | Descripción | Valor por Defecto |
|----------|-------------|------------------|
| `ZED_TTS_ENABLED` | Habilitar TTS para Zed | `false` |
| `ZED_TTS_VOICE` | Voz para notificaciones | `monica` |
| `ZED_TTS_RATE` | Velocidad de notificaciones | `175` |
| `ZED_TTS_TASK_VOICE` | Voz para tareas complejas | `jorge` |
| `ZED_TTS_TASK_RATE` | Velocidad para tareas complejas | `180` |
| `ZED_TTS_MAX_LENGTH` | Longitud máxima de texto | `100` |
| `ZED_STARTUP_ANNOUNCE` | Anunciar inicio de Zed | `true` |

## Voz Disponibles

### Español (Recomendado)
- `monica` - Español (Mónica)
- `jorge` - Español (Jorge)
- `angelica` - Español (Angélica)
- `paulina` - Español (Paulina)
- `francisca` - Español (Francisca)

### Enhanced/Premium
- `juan` - Mejorado (Juan)
- `diego` - Premium (Diego)
- `carlos` - Premium (Carlos)

### Siri
- `siri female` - Siri femenino
- `siri male` - Siri masculino

## Ejemplos de Uso

### Desarrollo Python
```bash
# Guardar archivo Python
echo "import os" > test.py
echo "test" | ./file-save-complete test.py

# Completar pruebas
echo "test completed with 0 errors, 0 failures" | ./task-complete test
```

### Web Development
```bash
# Guardar archivo React
echo "function Component() { return <div>Hello</div>; }" > App.jsx
echo "test" | ./file-save-complete App.jsx

# Completar build
echo "build success" | ./task-complete build
```

### Proyectos de Scripting
```bash
# Guardar script
echo "#!/bin/bash\necho 'Hello World'" > deploy.sh
echo "test" | ./file-save-complete deploy.sh

# Completar instalación
echo "install success" | ./task-complete install
```

## Contribuir

Si quieres contribuir a estos hooks:

1. Haz un fork del proyecto
2. Crea una rama para tu feature
3. Haz un PR con tus cambios
4. Incluye pruebas para nuevas funcionalidades

## Licencia

Este proyecto es parte de TTS-macOS y sigue la misma licencia.