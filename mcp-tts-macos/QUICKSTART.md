# 🚀 Guía Rápida de Inicio

¿Quieres empezar YA? Sigue estos 4 pasos:

## 1️⃣ Instalación Express (2 minutos)

```bash
# Navega a la carpeta del proyecto
cd mcp-tts-macos

# Ejecuta el instalador automático
./install.sh
```

¡Eso es todo! El script hace todo por ti:
- ✅ Crea el entorno virtual
- ✅ Instala dependencias
- ✅ Configura Claude Desktop
- ✅ Prueba que todo funciona

## 2️⃣ Reinicia Claude Desktop

- Cierra Claude Desktop completamente (Cmd+Q)
- Ábrelo nuevamente

## 3️⃣ Prueba que funciona

Escribe en Claude:

```
"Lee en voz alta: Hola, este es mi primer mensaje de texto a voz"
```

## 4️⃣ ¡Disfruta! 🎉

Ya está todo listo. Ahora puedes:

### Comandos útiles:

**Reproducir con voz específica:**
```
"Lee esto con la voz de Jorge: Buenos días"
```

**Más rápido o más lento:**
```
"Lee esto rápido: [tu texto]"
"Lee esto despacio: [tu texto]"
```

**Guardar como audio:**
```
"Guarda este mensaje como audio: [tu texto]"
```

**Ver voces disponibles:**
```
"¿Qué voces tienes disponibles?"
```

---

## ⚠️ ¿Problemas?

### No se escucha nada
1. Verifica el volumen de tu Mac
2. Prueba en terminal: `say "Hola mundo"`

### Claude no reconoce los comandos
1. Verifica que el servidor aparezca conectado en Claude
2. Revisa el archivo de configuración en:
   `~/Library/Application Support/Claude/claude_desktop_config.json`

### Voces no disponibles
Instala más voces en:
**Preferencias del Sistema → Accesibilidad → Contenido Hablado**

---

## 📚 Más información

Para documentación completa, lee el [README.md](README.md)

**¡Ahora a disfrutar de tu asistente con voz! 🎤**
