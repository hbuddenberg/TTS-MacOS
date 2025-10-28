# 🔧 Guía de Solución de Problemas

## 🎯 Diagnóstico Rápido

Ejecuta el script de prueba para identificar problemas:

```bash
cd mcp-tts-macos
python3 test_tts.py
```

Este script verifica:
- ✅ Si estás en macOS
- ✅ Qué voces están instaladas
- ✅ Si el comando `say` funciona
- ✅ Diferentes velocidades de lectura

---

## 🐛 Problemas Comunes

### 1. El servidor no aparece en Claude Desktop

**Síntomas:**
- No ves el ícono del servidor MCP
- Claude no reconoce comandos de voz

**Soluciones:**

#### A. Verifica el archivo de configuración

```bash
# Abre el archivo de configuración
open ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

Debe contener:
```json
{
  "mcpServers": {
    "tts-macos": {
      "command": "/Users/TU_USUARIO/Documents/mcp-tts-macos/venv/bin/python",
      "args": [
        "/Users/TU_USUARIO/Documents/mcp-tts-macos/server.py"
      ]
    }
  }
}
```

#### B. Verifica las rutas

```bash
# Para saber tu usuario
whoami

# Verifica que el archivo server.py existe
ls -la ~/Documents/mcp-tts-macos/server.py

# Verifica que Python del venv existe
ls -la ~/Documents/mcp-tts-macos/venv/bin/python
```

#### C. Reinicia correctamente

1. Cierra Claude con **Cmd+Q** (no solo cierres la ventana)
2. Espera 5 segundos
3. Abre Claude Desktop nuevamente

---

### 2. No se escucha el audio

**Soluciones:**

#### A. Verifica el volumen del sistema
```bash
# Sube el volumen
osascript -e 'set volume output volume 50'
```

#### B. Prueba el comando `say` directamente
```bash
say -v Monica "Hola mundo"
```

Si esto no funciona, el problema es con macOS, no con el servidor.

#### C. Verifica el dispositivo de salida
1. Ve a **Preferencias del Sistema** → **Sonido**
2. Pestaña **Salida**
3. Selecciona tus altavoces o auriculares

---

### 3. Error: "Voice not found"

**Causa:** La voz solicitada no está instalada

**Solución:** Instalar voces en español

1. Abre **Preferencias del Sistema**
2. Ve a **Accesibilidad**
3. Haz clic en **Contenido Hablado**
4. Clic en **Voces del Sistema**
5. Busca y descarga voces en español:
   - Monica (Español México)
   - Paulina (Español México)
   - Jorge (Español España)
   - Juan (Español España)

#### Verificar voces instaladas:
```bash
# Lista todas las voces
say -v ?

# Filtrar solo español
say -v ? | grep -i spanish
say -v ? | grep -i español
```

---

### 4. Error: "command not found: python"

**Soluciones:**

#### A. Activa el entorno virtual
```bash
cd mcp-tts-macos
source venv/bin/activate
```

Deberías ver `(venv)` al inicio de tu línea de comando.

#### B. Verifica la instalación de Python
```bash
which python3
python3 --version
```

Debe mostrar Python 3.10 o superior.

#### C. Reinstala el entorno virtual
```bash
cd mcp-tts-macos
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

### 5. Error: "Permission denied"

**Causa:** Los scripts no son ejecutables

**Solución:**
```bash
cd mcp-tts-macos
chmod +x install.sh test_tts.py
```

---

### 6. El audio se corta o suena entrecortado

**Causas posibles:**
- CPU sobrecargado
- Problemas con el dispositivo de audio

**Soluciones:**

#### A. Reduce la velocidad
Usa una velocidad menor (ej: 150 palabras por minuto)

#### B. Cierra aplicaciones que usen mucho CPU
```bash
# Ver procesos que usan más CPU
top -o cpu
```

#### C. Prueba con otra voz
Algunas voces requieren más procesamiento que otras.

---

### 7. Claude Desktop se congela al usar TTS

**Soluciones:**

#### A. Reduce el texto
No envíes textos muy largos de una sola vez.

#### B. Verifica la memoria disponible
```bash
# Ver memoria disponible
top -l 1 | grep PhysMem
```

#### C. Reinicia Claude Desktop
```bash
killall "Claude"
open -a "Claude"
```

---

### 8. Error al guardar archivos de audio

**Síntomas:**
- "Permission denied" al guardar
- Archivo no aparece en el Escritorio

**Soluciones:**

#### A. Verifica permisos del Escritorio
```bash
# Da permisos de escritura
chmod +w ~/Desktop
```

#### B. Prueba guardar manualmente
```bash
say -v Monica -o ~/Desktop/test.aiff "Prueba"
```

Si esto funciona, el problema está en el servidor MCP.

---

## 🔍 Logs y Depuración

### Ver logs del servidor MCP

Los logs de Claude Desktop están en:
```bash
~/Library/Logs/Claude/
```

### Ejecutar el servidor manualmente para debug

```bash
cd mcp-tts-macos
source venv/bin/activate
python server.py
```

Esto te permitirá ver errores en tiempo real.

---

## 🆘 Obtener Ayuda

Si ninguna de estas soluciones funciona:

1. **Recopila información:**
   ```bash
   # Versión de macOS
   sw_vers
   
   # Versión de Python
   python3 --version
   
   # Voces instaladas
   say -v ? | grep -i spanish
   ```

2. **Ejecuta el diagnóstico:**
   ```bash
   python3 test_tts.py > diagnostico.txt 2>&1
   ```

3. **Revisa el README.md** para información adicional

---

## ✅ Checklist de Verificación

Antes de pedir ayuda, verifica:

- [ ] Estoy en macOS (no Linux ni Windows)
- [ ] Python 3.10+ está instalado
- [ ] El entorno virtual está activado
- [ ] Las dependencias están instaladas
- [ ] El archivo de configuración está correcto
- [ ] Las rutas en la configuración son absolutas
- [ ] He reiniciado Claude Desktop correctamente
- [ ] El comando `say` funciona en terminal
- [ ] Tengo voces en español instaladas
- [ ] El volumen del sistema está activado

---

## 💡 Tips de Rendimiento

1. **Usa voces compactas:** Monica y Paulina son más ligeras
2. **Textos cortos:** Divide textos largos en párrafos
3. **Velocidad óptima:** 175 palabras/minuto es el balance perfecto
4. **Cierra otras apps de audio:** Evita conflictos con Spotify, etc.

---

**¿Solucionaste tu problema?** ¡Genial! 🎉

**¿Aún tienes problemas?** Revisa el README.md o los logs de Claude.
