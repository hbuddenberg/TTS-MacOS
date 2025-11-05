# PRIMERA VEZ después de cambios o instalación
uvx --from . --refresh tts-macos --list --gen female

# Después del refresh, usa normal
uvx --from . tts-macos --list --gen female
uvx --from . tts-macos --list --gen male --lang es_ES
uvx --from . tts-macos "Hola mundo" --voice Monica
```

## 🎯 ¿Cuándo usar `--refresh`?

- **Después de instalar** el proyecto por primera vez
- **Después de modificar** el código fuente del CLI
- **Después de actualizar** las opciones o argumentos
- **Cuando veas errores** como "unrecognized arguments"

## 📝 Ejemplos Prácticos

```bash
# Instalación inicial con refresh
uvx --from . --refresh tts-macos --help

# Probar nuevas opciones (si ya hiciste refresh antes)
uvx --from . tts-macos --list --gen female --lang es_ES
uvx --from . tts-macos --list --gen male
uvx --from . tts-macos --list --lang es_MX

# Síntesis de voz
uvx --from . tts-macos "Hola mundo" --voice Mónica --rate 200
```

## 🚀 Para el Uso Diario

Una vez que hayas hecho `--refresh` al menos una vez después de cada cambio, puedes usar `uvx` normal sin problemas.

```bash
# Crear alias conveniente en ~/.zshrc o ~/.bash_profile
alias tts='uvx --from ~/ruta/a/tu/proyecto tts-macos'

# Usar directamente
tts --list --gen female
tts "Hola mundo" --voice Jorge
```

## ⚠️ Recordatorio Importante

- **Sin `--refresh`**: uvx usa caché anterior → posibles errores
- **Con `--refresh`**: uvx reinstala con código actualizado → funciona correctamente

Este comportamiento es normal de uvx y asegura que siempre uses la versión más reciente del código durante el desarrollo.