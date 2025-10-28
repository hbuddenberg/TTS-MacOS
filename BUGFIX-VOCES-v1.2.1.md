# 🐛 Bug Fix: Voces no cambiaban - SOLUCIONADO

## 📋 Resumen

**Versión:** 1.2.1  
**Problema:** Las voces no cambiaban cuando se usaba `--voice`  
**Estado:** ✅ SOLUCIONADO

---

## 🔍 El Problema

Cuando ejecutabas:

```bash
uvx --from . tts-macos "Hola" --voice jorge
uvx --from . tts-macos "Hola" --voice monica
```

Todas las voces sonaban igual o no cambiaban.

### ¿Por qué pasaba?

El código tenía nombres de voces **fijos** que no necesariamente coincidían con las voces instaladas en tu sistema:

```python
# ❌ CÓDIGO ANTIGUO (v1.2.0)
VOCES = {
    "monica": "Monica",
    "paulina": "Paulina", 
    "jorge": "Jorge",
    ...
}
```

Si tu sistema tenía las voces con nombres ligeramente diferentes, o no las tenías instaladas, no funcionaba.

---

## ✅ La Solución

### Cambio Principal: Detección Automática

Ahora el código **detecta automáticamente** las voces disponibles en tu sistema:

```python
# ✅ CÓDIGO NUEVO (v1.2.1)
def obtener_voces_sistema():
    """Detecta automáticamente las voces en español disponibles"""
    result = subprocess.run(["say", "-v", "?"], capture_output=True, text=True)
    
    voces = {}
    for linea in result.stdout.split('\n'):
        if 'spanish' in linea.lower() or 'español' in linea.lower():
            nombre_voz = linea.strip().split()[0]
            voces[nombre_voz.lower()] = nombre_voz
    
    return voces

VOCES = obtener_voces_sistema()  # Se ejecuta al iniciar
```

### ¿Qué hace?

1. **Ejecuta** `say -v ?` para obtener todas las voces del sistema
2. **Filtra** solo las voces en español
3. **Crea** un diccionario con las voces realmente disponibles
4. **Usa** esos nombres cuando ejecutas el comando

---

## 🆕 Herramientas Nuevas

### 1. Script de Diagnóstico

**Archivo:** `diagnostico-voces.py`

```bash
cd mcp-tts-macos
python3 diagnostico-voces.py
```

**Qué hace:**
- ✅ Lista todas las voces en español instaladas
- ✅ Muestra cuáles faltan
- ✅ Prueba cada voz disponible
- ✅ Genera configuración sugerida

**Ejemplo de salida:**
```
🔍 Diagnóstico de Voces TTS para macOS
============================================================

✅ Se encontraron 4 voces en español:

🎤 Monica
   Monica               es_MX    # Monica, español (México)

🎤 Jorge  
   Jorge                es_ES    # Jorge, español (España)

🎤 Paulina
   Paulina              es_MX    # Paulina, español (México)

🎤 Juan
   Juan                 es_ES    # Juan, español (España)

🔍 Verificando voces esperadas:
   ✅ Monica     → disponible (usar: --voice monica)
   ✅ Jorge      → disponible (usar: --voice jorge)
   ✅ Paulina    → disponible (usar: --voice paulina)
   ✅ Juan       → disponible (usar: --voice juan)
   ❌ Diego      → NO instalada
   ❌ Angelica   → NO instalada
```

### 2. Guía de Solución

**Archivo:** `SOLUCION-VOCES.md`

Guía paso a paso para:
- Instalar voces faltantes
- Verificar instalación
- Probar cada voz
- Solucionar problemas comunes

---

## 🧪 Cómo Verificar que Funciona

### Paso 1: Actualizar el proyecto

```bash
# Descargar la nueva versión
cd ~/Downloads
tar -xzf mcp-tts-macos.tar.gz
cd mcp-tts-macos
```

### Paso 2: Ejecutar diagnóstico

```bash
python3 diagnostico-voces.py
```

Esto te dirá exactamente qué voces tienes y cuáles faltan.

### Paso 3: Ver voces disponibles

```bash
uvx --from . tts-macos --list
```

Ahora verás **solo las voces que tienes instaladas**, no una lista fija.

### Paso 4: Probar diferentes voces

```bash
# Cada una debería sonar diferente
uvx --from . tts-macos "Hola, soy Monica" --voice monica
uvx --from . tts-macos "Hola, soy Jorge" --voice jorge
uvx --from . tts-macos "Hola, soy Paulina" --voice paulina
```

---

## 📥 Si No Tienes Voces Instaladas

El diagnóstico te dirá cómo instalarlas:

1. **Abre Preferencias del Sistema**
2. **Ve a Accesibilidad → Contenido Hablado**
3. **Haz clic en "Voces del Sistema"**
4. **Descarga voces en español:**
   - Monica (México)
   - Jorge (España)
   - Paulina (México)
   - Juan (España)
   - Diego (Argentina)

---

## 🆚 Comparación Antes/Después

### Antes (v1.2.0):
```bash
# ❌ Si "Jorge" no estaba instalado → Error o voz por defecto
uvx --from . tts-macos "Test" --voice jorge

# ❌ Lista fija de voces (aunque no las tuvieras)
uvx --from . tts-macos --list
# Mostraba: monica, paulina, jorge, juan, diego, angelica
```

### Después (v1.2.1):
```bash
# ✅ Detecta automáticamente qué voces tienes
uvx --from . tts-macos "Test" --voice jorge

# ✅ Lista solo voces realmente disponibles
uvx --from . tts-macos --list
# Muestra solo: monica, jorge, paulina (las que tienes)
```

---

## 🎯 Beneficios

1. **Sin configuración manual**: Se adapta automáticamente a tu sistema
2. **Mensajes más claros**: Te dice exactamente qué voces faltan
3. **Fácil diagnóstico**: Script incluido para verificar
4. **Sin errores**: No intenta usar voces que no existen
5. **Flexible**: Funciona con cualquier voz en español que instales

---

## 📊 Archivos Modificados

```
src/tts_macos/cli.py          [Detección automática de voces]
src/tts_macos/__init__.py     [Actualizado a v1.2.1]
pyproject.toml                [Actualizado a v1.2.1]
CHANGELOG.md                  [Documentado el cambio]

Archivos nuevos:
diagnostico-voces.py          [Script de diagnóstico]
SOLUCION-VOCES.md             [Guía de solución]
```

---

## 🚀 Instrucciones de Actualización

### Si ya tienes el proyecto:

```bash
cd ~/Downloads
rm -rf mcp-tts-macos  # Eliminar versión antigua
tar -xzf mcp-tts-macos.tar.gz  # Nueva versión
cd mcp-tts-macos

# Verificar versión
uvx --from . tts-macos --version
# Debería mostrar: tts-macos 1.2.1
```

### Primera vez:

```bash
cd ~/Downloads
tar -xzf mcp-tts-macos.tar.gz
cd mcp-tts-macos

# Diagnosticar voces
python3 diagnostico-voces.py

# Instalar voces si es necesario (siguiendo las instrucciones)

# Probar
uvx --from . tts-macos "Hola mundo" --voice monica
```

---

## ✅ Checklist Post-Actualización

- [ ] Descargué mcp-tts-macos.tar.gz v1.2.1
- [ ] Ejecuté `python3 diagnostico-voces.py`
- [ ] Instalé las voces faltantes (si era necesario)
- [ ] Probé `uvx --from . tts-macos --list`
- [ ] Las voces ahora cambian correctamente
- [ ] Leí SOLUCION-VOCES.md por si tengo problemas

---

## 🎉 Resultado

**Ahora las voces funcionan perfectamente y se adaptan automáticamente a tu sistema.**

Si tienes 3 voces instaladas, verás 3.  
Si instalas 2 más, aparecerán automáticamente.  
Sin configuración, sin complicaciones.

---

## 📞 ¿Siguen sin cambiar las voces?

Si después de actualizar a v1.2.1 las voces siguen sin cambiar:

1. **Ejecuta el diagnóstico:**
   ```bash
   python3 diagnostico-voces.py
   ```

2. **Verifica que tienes múltiples voces instaladas**
   - Si solo tienes 1 voz, todas sonarán igual
   - Instala al menos 3 voces diferentes

3. **Prueba con `say` directamente:**
   ```bash
   say -v Monica "Test Monica"
   say -v Jorge "Test Jorge"
   ```
   
   Si esto funciona pero tts-macos no, reporta el problema.

4. **Lee la guía completa:**
   - Abre SOLUCION-VOCES.md
   - Sigue todos los pasos

---

**¡Disfruta de las voces funcionando! 🎤**

*Bug reportado y solucionado en el mismo día - v1.2.1*
