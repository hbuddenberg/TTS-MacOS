# 🔧 Solución de Problemas con Voces

## 🎤 Las voces no cambian / todas suenan igual

Este es el problema más común. Aquí está la solución:

### 🔍 Paso 1: Diagnosticar

Ejecuta el script de diagnóstico:

```bash
cd mcp-tts-macos
python3 diagnostico-voces.py
```

Este script te dirá:
- ✅ Qué voces tienes instaladas
- ❌ Qué voces faltan
- 🔧 Cómo instalar las que faltan

### 📥 Paso 2: Instalar Voces en Español

1. **Abre Preferencias del Sistema** (o Ajustes del Sistema en macOS Ventura+)

2. **Navega a Accesibilidad**
   - En macOS Ventura o posterior: `Ajustes → Accesibilidad`
   - En macOS anteriores: `Preferencias → Accesibilidad`

3. **Ve a Contenido Hablado**
   - Busca la sección "Contenido Hablado" o "Spoken Content"

4. **Haz clic en "Voces del Sistema"**
   - Aparecerá una lista de voces

5. **Descarga voces en español:**

   **Para México:**
   - ✅ Monica (Mujer)
   - ✅ Paulina (Mujer)
   
   **Para España:**
   - ✅ Jorge (Hombre)
   - ✅ Juan (Hombre)
   
   **Para Argentina:**
   - ✅ Diego (Hombre)

6. **Espera a que se descarguen**
   - Pueden tardar unos minutos
   - Se descargarán en segundo plano

### ✅ Paso 3: Verificar Instalación

Después de instalar las voces, verifica:

```bash
cd mcp-tts-macos

# Opción 1: Con el diagnóstico
python3 diagnostico-voces.py

# Opción 2: Directamente con tts-macos
uvx --from . tts-macos --list
```

### 🧪 Paso 4: Probar Voces

Prueba cada voz:

```bash
# Con Monica (México - Mujer)
uvx --from . tts-macos "Hola, soy Monica" --voice monica

# Con Jorge (España - Hombre)
uvx --from . tts-macos "Hola, soy Jorge" --voice jorge

# Con Paulina (México - Mujer)
uvx --from . tts-macos "Hola, soy Paulina" --voice paulina

# Con Juan (España - Hombre)
uvx --from . tts-macos "Hola, soy Juan" --voice juan

# Con Diego (Argentina - Hombre)
uvx --from . tts-macos "Hola, soy Diego" --voice diego
```

---

## 🐛 Problemas Comunes

### Problema 1: "Voice not found"

**Causa:** La voz no está instalada

**Solución:**
```bash
# 1. Ver qué voces tienes
python3 diagnostico-voces.py

# 2. Instalar las voces faltantes (ver Paso 2 arriba)

# 3. Probar de nuevo
uvx --from . tts-macos "Test" --voice monica
```

### Problema 2: Todas las voces suenan igual

**Causa:** Solo tienes una voz instalada, o macOS está usando la voz por defecto

**Solución:**
```bash
# 1. Verificar voces instaladas
say -v ? | grep -i spanish

# 2. Si solo ves una voz, instala más (Paso 2 arriba)

# 3. Probar con nombres exactos
say -v Monica "Test Monica"
say -v Jorge "Test Jorge"
```

### Problema 3: La voz suena robótica o rara

**Causa:** Voces "compactas" vs "mejoradas"

**Solución:**
En Voces del Sistema, algunas voces tienen versiones:
- **Compacta** (~20 MB) - Calidad básica
- **Mejorada** (~100+ MB) - Alta calidad

Descarga la versión "Mejorada" para mejor calidad.

### Problema 4: Error "say: invalid voice"

**Causa:** Nombre de voz incorrecto o no instalada

**Solución:**
```bash
# Ver nombres exactos disponibles
say -v ?

# Usar nombre exacto (con mayúscula)
say -v Monica "Test"  # ✅ Correcto
say -v monica "Test"  # ❌ Puede fallar

# tts-macos maneja esto automáticamente
uvx --from . tts-macos "Test" --voice monica  # ✅ Funciona
```

---

## 🔍 Comandos de Diagnóstico Útiles

### Ver todas las voces en español:
```bash
say -v ? | grep -i spanish
```

### Ver todas las voces (cualquier idioma):
```bash
say -v ?
```

### Probar una voz específica:
```bash
say -v Monica "Hola, esta es una prueba"
```

### Ver información de una voz:
```bash
say -v ? | grep Monica
```

---

## 🎯 Configuración Recomendada

Para tener una buena variedad de voces:

**Mínimo (3 voces):**
- Monica (México - Mujer)
- Jorge (España - Hombre)
- Paulina (México - Mujer)

**Recomendado (5 voces):**
- Monica (México - Mujer)
- Paulina (México - Mujer)
- Jorge (España - Hombre)
- Juan (España - Hombre)
- Diego (Argentina - Hombre)

**Completo (todas):**
- Las 5 anteriores +
- Angelica (México - Mujer)
- Cualquier otra voz en español disponible

---

## 💡 Tips

### 1. Verificar antes de usar:
```bash
# Siempre puedes verificar qué voces tienes
uvx --from . tts-macos --list
```

### 2. Usar voces por país:
```bash
# México
uvx --from . tts-macos "Texto" --voice monica

# España
uvx --from . tts-macos "Texto" --voice jorge

# Argentina
uvx --from . tts-macos "Texto" --voice diego
```

### 3. Calidad de audio:
- Las voces "mejoradas" suenan más naturales
- Ocupan más espacio pero vale la pena
- Se descargan una sola vez

### 4. Versión de macOS:
- macOS 10.14+: Todas las voces disponibles
- Versiones más antiguas: Menos voces disponibles

---

## 🆘 Si Nada Funciona

1. **Reinicia tu Mac**
   - A veces las voces necesitan reinicio para activarse

2. **Verifica espacio en disco**
   - Las voces ocupan 100-300 MB cada una
   - Necesitas espacio suficiente

3. **Reinstala una voz**
   - Ve a Voces del Sistema
   - Elimina la voz problemática
   - Descárgala de nuevo

4. **Prueba con comando nativo:**
   ```bash
   say -v Monica "Test"
   ```
   Si esto no funciona, el problema es de macOS, no de tts-macos

5. **Actualiza macOS**
   - Versiones más nuevas tienen mejores voces
   - `Ajustes → General → Actualización de Software`

---

## ✅ Checklist de Verificación

- [ ] Ejecuté `python3 diagnostico-voces.py`
- [ ] Instalé al menos 3 voces en español
- [ ] Probé cada voz individualmente
- [ ] Las voces funcionan con `say -v` directamente
- [ ] Ejecuté `uvx --from . tts-macos --list`
- [ ] Descargué versiones "mejoradas" de las voces

---

## 📞 Soporte Adicional

Si después de seguir todos estos pasos las voces siguen sin cambiar:

1. Ejecuta y guarda la salida de:
   ```bash
   python3 diagnostico-voces.py > diagnostico.txt
   say -v ? | grep -i spanish >> diagnostico.txt
   ```

2. Revisa `diagnostico.txt` para ver qué voces tienes

3. Asegúrate de usar los nombres exactos que aparecen en el diagnóstico

---

**¡La v1.2.1 detecta automáticamente tus voces disponibles!** 🎉

Ya no necesitas que coincidan los nombres exactos - el sistema se adapta a lo que tienes instalado.
