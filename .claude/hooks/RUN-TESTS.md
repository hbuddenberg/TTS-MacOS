# 🧪 Guía de Pruebas - Hooks TTS-macOS

## Tests Disponibles

Se crearon 4 scripts de prueba diferentes:

### 1. 🚀 Test Rápido (30 segundos)
**Archivo:** `test-quick.sh`
**Duración:** ~30 segundos
**Qué prueba:**
- Existencia de archivos
- Permisos de ejecución
- Comando `say` disponible
- Voces en español instaladas
- Prueba de audio básica

**Cómo ejecutar:**
```bash
./.claude/hooks/test-quick.sh
```

**Resultado esperado:**
```
⚡ TEST RÁPIDO DE HOOKS TTS-MACOS (30 segundos)
════════════════════════════════════════════════
1. Verificando archivos... ✅
2. Verificando permisos... ✅
3. Verificando comando 'say'... ✅
4. Verificando voces en español... ✅ (6 encontradas)
5. Prueba de audio (escucharás 'Prueba exitosa')...
¿Escuchaste el audio? (s/n): s

✅ TODOS LOS TESTS PASARON
```

---

### 2. 🧪 Test Completo (con audio)
**Archivo:** `test-hooks.sh`
**Duración:** ~5-10 minutos (con tests de audio)
**Qué prueba:**
- Todo lo del test rápido
- Verificación detallada de cada voz
- Hook post-response con diferentes configuraciones
- Hook user-prompt-submit
- Filtrado de código
- Truncado de texto
- Diferentes velocidades
- Cambio de voces

**Cómo ejecutar:**
```bash
./.claude/hooks/test-hooks.sh
```

**Incluye tests interactivos:**
- Te preguntará si quieres ejecutar tests de audio
- Validarás manualmente que escuchaste cada audio
- Tests de funcionalidad específica (filtrado, truncado, etc.)

**Resultado esperado:**
```
═══════════════════════════════════════════════════════════
  📊 RESUMEN DE TESTS
═══════════════════════════════════════════════════════════

Total de tests: 15
Tests exitosos: 15
Tests fallidos: 0

✅ TODOS LOS TESTS PASARON

🎉 Los hooks están funcionando correctamente!
```

---

### 3. 🔗 Test de Integración
**Archivo:** `test-integration.sh`
**Duración:** ~5 minutos
**Qué prueba:**
- Simulación de conversación real con Claude Code
- 7 escenarios diferentes:
  1. Pregunta simple
  2. Respuesta con código (filtrado)
  3. Cambio de voz dinámico
  4. Velocidad rápida
  5. Respuesta larga (truncado)
  6. Deshabilitar TTS
  7. Múltiples intercambios

**Cómo ejecutar:**
```bash
./.claude/hooks/test-integration.sh
```

**Resultado esperado:**
Simulación paso a paso de una conversación, con pausas entre cada escenario para validar el funcionamiento.

---

### 4. 🎤 Test de Voces
**Archivo:** `test-voices.sh`
**Duración:** ~2 minutos
**Qué prueba:**
- Lista todas las voces en español disponibles
- Reproduce cada voz con texto de ejemplo
- Ayuda a elegir la voz preferida

**Cómo ejecutar:**
```bash
./.claude/hooks/test-voices.sh
```

**Resultado esperado:**
```
🎤 TEST DE VOCES EN ESPAÑOL
═══════════════════════════════════════════════════

Encontradas 6 voces en español:

  • Monica es_MX  # español México
  • Paulina es_MX # español México
  • Jorge es_ES   # español España
  • Juan es_ES    # español España
  • Diego es_AR   # español Argentina
  • Angelica es_MX # español México

[1/6] Probando voz: Monica
[2/6] Probando voz: Paulina
...
```

---

## Recomendación de Ejecución

### Primera vez:
```bash
# 1. Test rápido para verificar instalación básica
./.claude/hooks/test-quick.sh

# 2. Si pasa, ejecutar test completo
./.claude/hooks/test-hooks.sh

# 3. Probar integración
./.claude/hooks/test-integration.sh
```

### Solo verificar voces:
```bash
./.claude/hooks/test-voices.sh
```

### Antes de usar con Claude Code:
```bash
# Test rápido para asegurar que todo funciona
./.claude/hooks/test-quick.sh
```

---

## Troubleshooting por Test

### test-quick.sh falla

**Error:** "Verificando archivos... ❌"
```bash
# Solución: Estás en el directorio incorrecto
cd /ruta/al/proyecto/TTS-MacOS
./.claude/hooks/test-quick.sh
```

**Error:** "Verificando permisos... ❌"
```bash
# Solución: Dar permisos de ejecución
chmod +x .claude/hooks/*
```

**Error:** "Verificando comando 'say'... ❌"
```
Causa: No estás en macOS o el comando no está disponible
No hay solución: Los hooks solo funcionan en macOS
```

**Error:** "Verificando voces en español... ❌"
```bash
# Solución: Instalar voces
# 1. Preferencias del Sistema → Accesibilidad
# 2. Contenido Hablado → Voces del Sistema
# 3. Descargar voces en español
```

**Error:** "¿Escuchaste el audio? (s/n): n"
```bash
# Verificar volumen
osascript -e 'set volume output volume 50'

# Probar manualmente
say -v Monica "test"

# Si funciona manualmente pero no con el hook, revisar permisos
ls -la .claude/hooks/post-response
```

---

### test-hooks.sh falla

**Muchos tests fallan al inicio:**
- Revisa primero con `test-quick.sh`
- Asegura que test-quick.sh pase al 100%

**Tests de audio fallan:**
```bash
# Verificar que tts-macos esté instalado (opcional)
which tts-macos

# Si no está, los hooks usarán 'say' directamente
# Esto es normal y debería funcionar igual
```

**Filtrado de código falla:**
- El hook debe eliminar bloques ```code```
- Verifica que sed funcione:
```bash
echo -e "texto\n\`\`\`python\ncode\n\`\`\`\nmás texto" | sed '/```/,/```/d'
# Debería mostrar solo "texto" y "más texto"
```

---

### test-integration.sh falla

**No se escucha nada:**
```bash
# Verificar variables de entorno
echo $TTS_ENABLED  # Debe ser "true"
echo $TTS_VOICE    # Debe ser una voz válida

# Exportar manualmente
export TTS_ENABLED=true
export TTS_VOICE=monica
```

**Escenarios específicos fallan:**
- Cada escenario es independiente
- Si uno falla, continúa con los demás
- Anota cuál falló para debug específico

---

### test-voices.sh falla

**"No se encontraron voces en español":**
```bash
# Verificar voces disponibles
say -v ? | grep -i spanish

# Si no muestra nada, instalar voces:
# System Preferences → Accessibility → Spoken Content → System Voices
```

---

## Tests Manuales Adicionales

### Test Manual 1: Hook Individual
```bash
# Probar post-response directamente
export TTS_ENABLED=true
export TTS_VOICE=monica
echo "Texto de prueba" | ./.claude/hooks/post-response
```

### Test Manual 2: Con tts-macos CLI
```bash
# Si tienes tts-macos instalado
tts-macos "Prueba con CLI" --voice monica --rate 175
```

### Test Manual 3: Con say directamente
```bash
# Fallback nativo de macOS
say -v Monica -r 175 "Prueba directa con say"
```

### Test Manual 4: Filtrado
```bash
# Crear archivo de prueba
cat > /tmp/test-response.txt << 'EOF'
Este es texto normal.

```python
print("esto es código")
```

Más texto después del código.
EOF

# Probar filtrado
cat /tmp/test-response.txt | ./.claude/hooks/post-response
# Debe leer solo el texto, no el código
```

---

## Validación de Resultados

### ✅ Test Exitoso
- Todos los tests pasan (contador de PASS)
- El audio se reproduce correctamente
- Las voces se escuchan claras
- El filtrado de código funciona
- El truncado funciona según configuración

### ⚠️ Test Parcial
- Algunos tests fallan pero los críticos pasan
- Audio funciona pero algunas voces no están disponibles
- Hooks funcionan pero tts-macos CLI no instalado (usa say como fallback)

### ❌ Test Fallido
- No se escucha ningún audio
- Archivos no existen o no tienen permisos
- Comando say no disponible (no estás en macOS)
- No hay voces en español instaladas

---

## Después de los Tests

### Si todos pasan:
```bash
# Activar TTS para Claude Code
export TTS_ENABLED=true
export TTS_VOICE=monica
export TTS_RATE=175

# Iniciar Claude Code
claude-code
```

### Si algunos fallan:
1. Revisa la sección de troubleshooting
2. Ejecuta tests manuales específicos
3. Verifica configuración del sistema
4. Consulta `.claude/hooks/README.md`

---

## Automatización de Tests

### Ejecutar todos los tests en secuencia:
```bash
#!/bin/bash
# run-all-tests.sh

echo "Ejecutando todos los tests..."
echo ""

./.claude/hooks/test-quick.sh
if [ $? -ne 0 ]; then
    echo "❌ Test rápido falló. Deteniéndose."
    exit 1
fi

echo ""
read -p "Test rápido pasó. ¿Ejecutar test completo? (s/n): " continuar
if [[ "$continuar" == "s" ]]; then
    ./.claude/hooks/test-hooks.sh
fi
```

---

## Información de Debug

### Habilitar modo verbose:
```bash
# Agregar al inicio de cualquier hook
set -x  # Mostrar todos los comandos ejecutados

# O ejecutar con bash -x
bash -x ./.claude/hooks/post-response <<< "test"
```

### Ver logs en tiempo real:
```bash
# Crear archivo de log en el hook
echo "DEBUG: $VARIABLE" >> /tmp/tts-debug.log

# Ver logs
tail -f /tmp/tts-debug.log
```

---

## Resumen Rápido

| Test | Duración | Cuándo usar |
|------|----------|-------------|
| `test-quick.sh` | 30 seg | Primera vez, antes de usar |
| `test-hooks.sh` | 5-10 min | Instalación completa, debugging |
| `test-integration.sh` | 5 min | Validar flujo completo |
| `test-voices.sh` | 2 min | Elegir voz preferida |

**Recomendación:** Empieza con `test-quick.sh`. Si pasa, los hooks funcionan.
