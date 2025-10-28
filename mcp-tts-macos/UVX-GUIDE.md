# 🚀 Guía de Uso con UVX

## 📖 ¿Qué es uvx?

`uvx` es parte del ecosistema [uv](https://github.com/astral-sh/uv) - una herramienta ultrarrápida de gestión de paquetes Python. Similar a `npx` para Node.js, `uvx` te permite ejecutar herramientas Python sin instalarlas globalmente.

**Ventajas:**
- ⚡ Extremadamente rápido
- 📦 No requiere instalación global
- 🔄 Siempre usa la última versión
- 🧹 No contamina tu sistema

---

## 🛠️ Instalación de uv/uvx

### macOS (Homebrew)

```bash
brew install uv
```

### macOS/Linux (Script oficial)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Verificar instalación

```bash
uvx --version
```

---

## 🎤 Uso Básico con uvx

### Sin instalar nada

```bash
# Desde el directorio del proyecto
cd mcp-tts-macos
uvx --from . tts-macos "Hola mundo"
```

### Desde PyPI (cuando esté publicado)

```bash
uvx tts-macos "Hola mundo"
uvx tts-macos "Buenos días" --voice jorge
uvx tts-macos "Rápido" --rate 250
```

---

## 💡 Ejemplos con uvx

### Ejemplos Básicos

```bash
# Reproducir texto
uvx --from . tts-macos "Hola mundo"

# Con voz específica
uvx --from . tts-macos "Desde España" --voice jorge

# Con velocidad ajustada
uvx --from . tts-macos "Muy rápido" --rate 250
uvx --from . tts-macos "Muy lento" --rate 125

# Guardar como audio
uvx --from . tts-macos "Guardar mensaje" --save audio.aiff

# Ver voces disponibles
uvx --from . tts-macos --list

# Ver ayuda
uvx --from . tts-macos --help
```

### Combinar Opciones

```bash
# Todo junto
uvx --from . tts-macos "Mensaje completo" \
    --voice paulina \
    --rate 200 \
    --save completo.aiff
```

---

## 🔧 Uso en Scripts

### Script Bash

```bash
#!/bin/bash
# notify.sh

function notificar() {
    uvx --from /ruta/a/mcp-tts-macos tts-macos "$1" --voice monica
}

# Uso
notificar "Proceso completado"
notificar "Error detectado"
```

### Con Variables de Entorno

```bash
# Definir ruta del proyecto
export TTS_MACOS_PATH="/Users/tu_usuario/mcp-tts-macos"

# Usar en scripts
uvx --from "$TTS_MACOS_PATH" tts-macos "Mensaje"
```

### Alias para Facilitar Uso

Agrega a tu `~/.zshrc` o `~/.bash_profile`:

```bash
# Alias simple
alias tts='uvx --from ~/mcp-tts-macos tts-macos'

# Alias con voces
alias monica='uvx --from ~/mcp-tts-macos tts-macos --voice monica'
alias jorge='uvx --from ~/mcp-tts-macos tts-macos --voice jorge'
alias rapido='uvx --from ~/mcp-tts-macos tts-macos --rate 250'

# Función más compleja
function hablar() {
    uvx --from ~/mcp-tts-macos tts-macos "$@"
}
```

Después de definir los alias:

```bash
tts "Hola mundo"
jorge "Desde España"
rapido "Muy rápido"
hablar "Con función" --voice paulina
```

---

## 📦 Uso Local vs Instalado

### Local (con --from)

```bash
# Usa el código local del proyecto
cd mcp-tts-macos
uvx --from . tts-macos "texto"
```

**Ventajas:**
- ✅ No requiere instalación
- ✅ Usa versión local
- ✅ Perfecto para desarrollo
- ✅ Cambios inmediatos

### Instalado (cuando esté en PyPI)

```bash
# Descarga e instala automáticamente
uvx tts-macos "texto"
```

**Ventajas:**
- ✅ Más corto
- ✅ Funciona desde cualquier lugar
- ✅ Siempre la última versión

---

## 🎯 Casos de Uso Reales

### 1. Notificaciones de Backup

```bash
#!/bin/bash
# backup.sh

rsync -av /source /destination

if [ $? -eq 0 ]; then
    uvx --from ~/mcp-tts-macos tts-macos "Backup completado" --voice monica
else
    uvx --from ~/mcp-tts-macos tts-macos "Error en backup" --voice jorge
fi
```

### 2. Timer Pomodoro

```bash
#!/bin/bash
# pomodoro.sh

echo "Iniciando Pomodoro..."
uvx --from ~/mcp-tts-macos tts-macos "Comienza a trabajar" --voice angelica

sleep 1500  # 25 minutos
uvx --from ~/mcp-tts-macos tts-macos "Toma un descanso" --voice angelica

sleep 300   # 5 minutos
uvx --from ~/mcp-tts-macos tts-macos "De vuelta al trabajo" --voice angelica
```

### 3. Monitor de Sistema

```bash
#!/bin/bash
# monitor.sh

while true; do
    cpu=$(top -l 1 | grep "CPU usage" | awk '{print $3}' | cut -d'%' -f1)
    
    if (( $(echo "$cpu > 80" | bc -l) )); then
        uvx --from ~/mcp-tts-macos tts-macos "Alerta: CPU al $cpu porciento"
    fi
    
    sleep 300  # Revisar cada 5 minutos
done
```

### 4. Recordatorios con Cron

```bash
# Editar crontab
crontab -e

# Agregar recordatorios
0 9 * * * uvx --from /Users/tu_usuario/mcp-tts-macos tts-macos "Buenos días"
0 12 * * * uvx --from /Users/tu_usuario/mcp-tts-macos tts-macos "Hora de almorzar"
0 18 * * * uvx --from /Users/tu_usuario/mcp-tts-macos tts-macos "Fin del día"
```

### 5. Integración con CI/CD

```yaml
# .github/workflows/notify.yml
name: Build Notification

on: [push]

jobs:
  build:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install uv
        run: brew install uv
      - name: Notify
        run: |
          uvx --from . tts-macos "Build completado" --save build-done.aiff
```

---

## 🔗 Integración con Otros Comandos

### Con jq (procesar JSON)

```bash
# Leer y hablar un campo JSON
echo '{"message":"Hola mundo"}' | \
    jq -r '.message' | \
    xargs uvx --from ~/mcp-tts-macos tts-macos
```

### Con curl (APIs)

```bash
# Obtener y leer una cita del día
curl -s https://api.quotable.io/random | \
    jq -r '.content' | \
    xargs uvx --from ~/mcp-tts-macos tts-macos --voice jorge
```

### Con grep (buscar en archivos)

```bash
# Buscar errores y notificar
if grep -q "ERROR" logs.txt; then
    uvx --from ~/mcp-tts-macos tts-macos "Se encontraron errores en el log"
fi
```

### Pipeline complejo

```bash
# Leer titulares de noticias (ejemplo ficticio)
curl -s https://api.news.com/headlines | \
    jq -r '.articles[0].title' | \
    xargs uvx --from ~/mcp-tts-macos tts-macos --voice jorge --rate 180
```

---

## 🆚 Comparación: uvx vs pip install

| Característica | uvx | pip install |
|----------------|-----|-------------|
| Instalación global | ❌ | ✅ |
| Velocidad | ⚡⚡⚡ | ⚡ |
| Aislamiento | ✅ | ❌ (sin venv) |
| Actualizaciones | Automáticas | Manual |
| Espacio disco | Mínimo | Más |
| Múltiples versiones | ✅ | ❌ |

---

## 🎓 Tips y Trucos

### 1. Crear wrapper script

```bash
#!/bin/bash
# ~/bin/tts

uvx --from ~/mcp-tts-macos tts-macos "$@"
```

```bash
chmod +x ~/bin/tts
tts "Ahora es más corto"
```

### 2. Usar con watch

```bash
# Monitorear archivo y notificar cambios
watch -n 60 "tail -1 monitor.log | xargs uvx --from ~/mcp-tts-macos tts-macos"
```

### 3. Pre-cargar con --with

```bash
# Si necesitas dependencias extras
uvx --with mcp --from . tts-macos "texto"
```

### 4. Especificar versión de Python

```bash
uvx --python 3.12 --from . tts-macos "texto"
```

---

## 🐛 Solución de Problemas

### Error: "command not found: uvx"

```bash
# Instalar uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# O con Homebrew
brew install uv

# Verificar
which uvx
```

### Error: "No module named tts_macos"

```bash
# Asegúrate de estar en el directorio correcto
cd mcp-tts-macos
uvx --from . tts-macos "test"

# O usa ruta absoluta
uvx --from /ruta/completa/a/mcp-tts-macos tts-macos "test"
```

### Muy lento en primera ejecución

```bash
# uvx cachea el paquete, la primera vez es más lenta
# Subsecuentes ejecuciones son instantáneas

# Pre-cachear
uvx --from . tts-macos --help
```

### Limpiar cache

```bash
# Si necesitas limpiar el cache de uvx
rm -rf ~/.cache/uv
```

---

## 📊 Benchmark: uvx vs pip

```bash
# Tiempo de ejecución (después de caché)

# Con uvx
time uvx --from . tts-macos "test"
# real: ~0.1s

# Con pip install + ejecución
time tts-macos "test"
# real: ~0.05s

# Conclusión: uvx es casi instantáneo después del primer uso
```

---

## 🎉 Ventajas de usar uvx

1. **No contamina tu sistema**
   - No instala nada globalmente
   - Perfecto para probar herramientas

2. **Siempre actualizado**
   - Usa la última versión del código
   - Ideal para desarrollo

3. **Múltiples versiones**
   - Puedes tener diferentes versiones
   - Sin conflictos

4. **Portabilidad**
   - Funciona igual en diferentes máquinas
   - Solo necesitas uv instalado

5. **Desarrollo rápido**
   - Cambios en código = efecto inmediato
   - No necesitas reinstalar

---

## 📚 Recursos Adicionales

- [Documentación oficial de uv](https://github.com/astral-sh/uv)
- [Guía de uvx](https://docs.astral.sh/uv/guides/tools/)
- CLI-GUIDE.md para más ejemplos generales

---

## ✅ Checklist de Uso

- [ ] Instalé uv/uvx
- [ ] Estoy en el directorio del proyecto
- [ ] Probé: `uvx --from . tts-macos "test"`
- [ ] Creé alias para uso frecuente
- [ ] Entendí la diferencia entre --from local y PyPI

---

## 🎤 Ejemplos Rápidos para Copiar

```bash
# Básico
uvx --from . tts-macos "Hola mundo"

# Con opciones
uvx --from . tts-macos "Buenos días" --voice jorge --rate 200

# Guardar
uvx --from . tts-macos "Mi mensaje" --save audio.aiff

# Leer archivo
uvx --from . tts-macos "$(cat documento.txt)" --voice paulina

# En script
if ./deploy.sh; then
    uvx --from ~/mcp-tts-macos tts-macos "Deploy exitoso"
fi
```

---

**¡Disfruta de TTS-macOS con uvx! Es la forma más moderna de usarlo. 🚀**
