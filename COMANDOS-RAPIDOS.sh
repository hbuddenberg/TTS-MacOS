#!/bin/bash
# ============================================
# COMANDOS DE INSTALACIÓN RÁPIDA
# ============================================
# Copia y pega estos comandos en tu terminal
# ============================================

# 1. Navegar a la carpeta de Descargas (o donde esté el archivo)
cd ~/Downloads

# 2. Descomprimir el proyecto
tar -xzf mcp-tts-macos.tar.gz

# 3. Entrar a la carpeta del proyecto
cd mcp-tts-macos

# 4. Ejecutar el instalador automático
./install.sh

# ============================================
# ¡Eso es todo! Ahora:
# ============================================
# 1. Cierra Claude Desktop (Cmd+Q)
# 2. Abre Claude Desktop nuevamente
# 3. Escribe: "Lee en voz alta: Hola mundo"
# ============================================

# ============================================
# COMANDOS ADICIONALES ÚTILES
# ============================================

# Para probar las voces disponibles:
# python3 test_tts.py

# Para verificar que el servidor está corriendo:
# cat ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Para probar una voz manualmente:
# say -v Monica "Hola mundo"

# Para ver todas las voces instaladas:
# say -v ? | grep -i spanish

# Para instalar más voces:
# 1. Ve a: Preferencias del Sistema
# 2. Accesibilidad → Contenido Hablado
# 3. Voces del Sistema
# 4. Descarga las voces en español que quieras

# ============================================
# UBICACIÓN DE ARCHIVOS IMPORTANTES
# ============================================

# Configuración de Claude Desktop:
# ~/Library/Application Support/Claude/claude_desktop_config.json

# Logs de Claude Desktop:
# ~/Library/Logs/Claude/

# Proyecto instalado:
# ~/Documents/mcp-tts-macos/

# Audios guardados (por defecto):
# ~/Desktop/*.aiff

# ============================================
# SI ALGO NO FUNCIONA
# ============================================

# 1. Lee el archivo TROUBLESHOOTING.md:
# cat TROUBLESHOOTING.md

# 2. Ejecuta el diagnóstico:
# python3 test_tts.py

# 3. Verifica el volumen:
# osascript -e 'set volume output volume 50'

# 4. Prueba el comando say:
# say "Hola mundo"

# 5. Reinstala si es necesario:
# rm -rf venv
# ./install.sh

# ============================================
# COMANDOS DE DESINSTALACIÓN
# ============================================

# Para desinstalar completamente:
# cd ~/Documents
# rm -rf mcp-tts-macos

# Eliminar configuración de Claude:
# Edita ~/Library/Application Support/Claude/claude_desktop_config.json
# y elimina la sección "tts-macos"

# ============================================
# ¡DISFRUTA DE TU SERVIDOR TTS! 🎉
# ============================================
