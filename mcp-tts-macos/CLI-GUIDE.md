# 🎤 Guía de Uso - TTS-macOS CLI

## 📖 Introducción

`tts-macos` es una herramienta de línea de comandos que convierte texto a voz usando el TTS nativo de macOS. Similar a cómo usarías `npx`, pero para texto a voz.

---

## 🚀 Instalación

### Opción 1: Instalación rápida (recomendado)

```bash
cd mcp-tts-macos
./install-cli.sh
```

Selecciona la opción 1 para instalación local.

### Opción 2: Instalación manual

```bash
# Copiar a ~/.local/bin
mkdir -p ~/.local/bin
cp tts-macos ~/.local/bin/
chmod +x ~/.local/bin/tts-macos

# Agregar a PATH (si no está)
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### Opción 3: Con pip (instalación como paquete)

```bash
cd mcp-tts-macos
pip install -e .
```

---

## 📚 Uso Básico

### Sintaxis

```bash
tts-macos "tu texto aquí" [opciones]
```

### Ejemplos Simples

```bash
# Reproducir texto simple
tts-macos "Hola mundo"

# Con voz específica
tts-macos "Buenos días" --voice jorge

# Con velocidad diferente
tts-macos "Esto es rápido" --rate 250

# Guardar como audio
tts-macos "Guardar esto" --save mi_audio.aiff

# Ver ayuda
tts-macos --help

# Listar voces disponibles
tts-macos --list
```

---

## 🎛️ Opciones Disponibles

### `-v, --voice <voz>`
Selecciona la voz a utilizar.

**Voces disponibles:**
- `monica` - Español México (Mujer) - **Por defecto**
- `paulina` - Español México (Mujer)
- `jorge` - Español España (Hombre)
- `juan` - Español España (Hombre)
- `diego` - Español Argentina (Hombre)
- `angelica` - Español México (Mujer)

**Ejemplo:**
```bash
tts-macos "Hola desde España" --voice jorge
```

### `-r, --rate <número>`
Velocidad de lectura en palabras por minuto (100-300).

**Valores comunes:**
- `125` - Muy lento
- `150` - Lento
- `175` - Normal (default)
- `200` - Rápido
- `250` - Muy rápido

**Ejemplo:**
```bash
tts-macos "Lee esto lento" --rate 125
tts-macos "Lee esto rápido" --rate 250
```

### `-s, --save <archivo>`
Guarda el audio en un archivo (formato .aiff).

**Ejemplo:**
```bash
tts-macos "Guardar este mensaje" --save mensaje.aiff
```

El archivo se guardará en el directorio actual.

### `-l, --list`
Lista todas las voces disponibles.

**Ejemplo:**
```bash
tts-macos --list
```

### `--version`
Muestra la versión de tts-macos.

**Ejemplo:**
```bash
tts-macos --version
```

### `--help`
Muestra la ayuda completa.

**Ejemplo:**
```bash
tts-macos --help
```

---

## 💡 Ejemplos Avanzados

### Combinar opciones

```bash
# Voz, velocidad y guardar
tts-macos "Mensaje completo" --voice paulina --rate 200 --save completo.aiff

# Texto largo
tts-macos "Este es un texto muy largo que será reproducido con la voz de Jorge a velocidad normal" --voice jorge
```

### Leer desde archivo

```bash
# Leer un archivo de texto
tts-macos "$(cat mi_texto.txt)"

# O con cat
cat mi_texto.txt | xargs tts-macos
```

### Usar en scripts

```bash
#!/bin/bash

# Notificación sonora
function notificar() {
    tts-macos "$1" --voice monica --rate 200
}

# Uso
notificar "Proceso completado"
notificar "Error en línea 42"
```

### Crear alias útiles

Agrega a tu `~/.zshrc` o `~/.bash_profile`:

```bash
# Alias para diferentes voces
alias hablar='tts-macos'
alias jorge='tts-macos --voice jorge'
alias monica='tts-macos --voice monica'

# Alias para velocidades
alias rapido='tts-macos --rate 250'
alias lento='tts-macos --rate 125'

# Función para leer archivos
function leer() {
    tts-macos "$(cat $1)"
}
```

Uso después de definir los alias:
```bash
hablar "Hola"
jorge "Desde España"
rapido "Muy rápido"
leer documento.txt
```

---

## 🔗 Uso Tipo "npx"

### Como comando directo (sin instalar)

```bash
# Ejecutar sin instalar
./tts-macos "Hola mundo"

# Desde cualquier lugar (usando ruta completa)
~/Documents/mcp-tts-macos/tts-macos "Hola mundo"
```

### Crear función en shell

Agrega a tu `~/.zshrc`:

```bash
function tts() {
    ~/Documents/mcp-tts-macos/tts-macos "$@"
}
```

Luego úsalo desde cualquier lugar:
```bash
tts "Hola mundo" --voice jorge
```

---

## 🎨 Casos de Uso Reales

### 1. Notificaciones de scripts

```bash
#!/bin/bash
# backup.sh

echo "Iniciando backup..."
rsync -av /source /destination

if [ $? -eq 0 ]; then
    tts-macos "Backup completado exitosamente" --voice monica
else
    tts-macos "Error en el backup" --voice jorge --rate 150
fi
```

### 2. Timer/Alarma

```bash
# timer.sh
sleep 1800  # 30 minutos
tts-macos "Han pasado 30 minutos. Tiempo de descansar" --voice paulina
```

### 3. Lectura de noticias

```bash
# news.sh
curl -s "https://api.noticias.com/headlines" | \
jq -r '.articles[0].title' | \
tts-macos --voice jorge
```

### 4. Asistente de productividad

```bash
# pomodoro.sh
echo "Iniciando Pomodoro..."
tts-macos "Comienza a trabajar" --voice angelica

sleep 1500  # 25 minutos
tts-macos "Pomodoro completado. Toma un descanso" --voice angelica

sleep 300   # 5 minutos
tts-macos "Descanso terminado. Listo para otro pomodoro" --voice angelica
```

### 5. Traductor con voz

```bash
# translate-speak.sh
texto="Hello world"
traduccion=$(trans -b en:es "$texto")
tts-macos "$traduccion" --voice monica
```

---

## 🔧 Integración con Otros Comandos

### Con `jq` (procesar JSON)

```bash
cat data.json | jq -r '.message' | xargs tts-macos
```

### Con `grep` (buscar y leer)

```bash
grep "ERROR" logs.txt | head -1 | xargs tts-macos --voice jorge
```

### Con `awk` (procesar texto)

```bash
ps aux | awk 'NR==2 {print $11}' | xargs tts-macos
```

### Con `cron` (tareas programadas)

```bash
# Agregar a crontab
# Recordatorio diario a las 9 AM
0 9 * * * /Users/tu_usuario/.local/bin/tts-macos "Buenos días. Hora de trabajar"
```

---

## 🎯 Tips y Trucos

### Textos largos

Para textos muy largos, divídelos en párrafos:

```bash
# Leer archivo por párrafos
while IFS= read -r linea; do
    [ -n "$linea" ] && tts-macos "$linea" --voice monica
    sleep 1
done < documento.txt
```

### Control de audio

```bash
# Ajustar volumen del sistema antes de reproducir
osascript -e 'set volume output volume 50'
tts-macos "Volumen al 50%"
```

### Crear biblioteca de sonidos

```bash
# Crear múltiples audios
for frase in "Error" "Éxito" "Advertencia" "Completado"; do
    tts-macos "$frase" --voice jorge --save "${frase,,}.aiff"
done
```

---

## ❓ Preguntas Frecuentes

### ¿Funciona sin conexión a internet?
Sí, usa el TTS nativo de macOS, completamente offline.

### ¿Puedo usar otras voces?
Solo las voces instaladas en macOS. Para instalar más:
Preferencias del Sistema → Accesibilidad → Contenido Hablado → Voces del Sistema

### ¿Funciona en Linux o Windows?
No, solo macOS. Usa el comando `say` que es exclusivo de macOS.

### ¿Puedo cambiar el formato de audio?
Actualmente solo AIFF. Puedes convertir con:
```bash
tts-macos "Hola" --save temp.aiff
ffmpeg -i temp.aiff output.mp3
```

---

## 🆘 Solución de Problemas

### Comando no encontrado

```bash
# Verifica la instalación
which tts-macos

# Si no aparece, verifica el PATH
echo $PATH

# Reinstala
cd mcp-tts-macos
./install-cli.sh
```

### No se escucha audio

```bash
# Verifica volumen
osascript -e 'set volume output volume 50'

# Prueba el comando say directamente
say "Test"
```

### Voz no disponible

```bash
# Lista voces instaladas
say -v ?

# Instala voces faltantes desde Preferencias del Sistema
```

---

## 📦 Comparación con `npx`

| Característica | npx | tts-macos |
|----------------|-----|-----------|
| Instalación global | ✅ | ✅ |
| Uso sin instalar | ✅ | ✅ (con ./) |
| Argumentos | ✅ | ✅ |
| Pipeline | ✅ | ✅ |
| Multiplataforma | ✅ | ❌ (solo macOS) |

**Uso similar:**
```bash
# npx
npx some-package arg1 arg2

# tts-macos
tts-macos "texto" --voice jorge
```

---

## 🎉 ¡Listo para Usar!

Ahora tienes una herramienta CLI poderosa para texto a voz.

**Comandos para empezar:**
```bash
tts-macos "Hola mundo"
tts-macos --list
tts-macos --help
```

**¡Experimenta y diviértete! 🎤**
