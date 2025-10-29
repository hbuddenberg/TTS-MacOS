# 🎙️ Actualización: Detección Automática de Voces

## ✨ Novedades

Los hooks ahora detectan **automáticamente** todas las voces disponibles en tu sistema, incluyendo:

- ✅ Voces en español (Monica, Jorge, Paulina, etc.)
- ✅ Voces Enhanced/Premium (Angélica, Francisca, etc.)
- ✅ Voces de Siri (cuando estén instaladas)
- ✅ Todas las demás voces del sistema

## 🔍 Voces Detectadas en Tu Sistema

Según el escaneo actual:

### 📍 Voces en Español Estándar (16)
- Eddy (España y México)
- Flo (España y México)
- Grandma (España y México)
- Grandpa (España y México)
- Reed (España y México)
- Rocko (España y México)
- Sandy (España y México)
- Shelley (España y México)

### ⭐ Voces Enhanced/Premium (13)
- **Angélica** (Enhanced) - México
- **Carlos** (Enhanced) - Colombia
- **Diego** (Enhanced) - Argentina
- **Francisca** (Enhanced) - Chile
- **Isabela** (Enhanced) - Argentina
- **Jorge** (Enhanced) - España
- **Juan** (Enhanced) - México
- **Marisol** (Enhanced + Premium) - España
- **Mónica** (Enhanced) - España
- **Paulina** (Enhanced) - México
- **Soledad** (Enhanced) - Colombia
- **Jimena** (Enhanced) - Colombia

### 🤖 Voces de Siri
- Actualmente no instaladas
- El sistema las detectará automáticamente cuando se instalen

## 🚀 Cómo Usar

### Método 1: Nombre Exacto
```bash
export TTS_VOICE=Angélica    # Con tilde
export TTS_VOICE=Angelica    # Sin tilde (también funciona)
export TTS_VOICE=Francisca
export TTS_VOICE=Jorge
```

### Método 2: Búsqueda Automática (Case-Insensitive)
```bash
export TTS_VOICE=angelica    # Minúsculas
export TTS_VOICE=MONICA      # Mayúsculas
export TTS_VOICE=jorge       # Cualquier combinación
```

### Método 3: Búsqueda Parcial
```bash
export TTS_VOICE=angel       # Encontrará "Angélica"
export TTS_VOICE=franc       # Encontrará "Francisca"
export TTS_VOICE=siri        # Encontrará voz Siri (si está instalada)
```

## 📊 Archivos Actualizados

1. **post-response** - Hook principal con detección automática
2. **user-prompt-submit** - Hook de confirmación con detección automática
3. **enable-tts.sh** - Muestra todas las voces disponibles categorizadas
4. **list-all-voices.sh** - Lista completa de voces del sistema
5. **test-siri-voices.sh** - Tests de detección automática

## 🧪 Probar la Detección Automática

### Ver Todas las Voces
```bash
./.claude/hooks/list-all-voices.sh
```

### Configuración Interactiva
```bash
source .claude/hooks/enable-tts.sh
```
- Mostrará todas las voces disponibles categorizadas
- Permite seleccionar por nombre o número
- Detecta automáticamente voces Enhanced y Siri

### Test de Detección
```bash
./.claude/hooks/test-siri-voices.sh
```

## 💡 Ejemplos de Uso

### Usar Voz Enhanced
```bash
export TTS_ENABLED=true
export TTS_VOICE=Angélica    # Voz Enhanced de México
export TTS_RATE=175
```

### Usar Voz Premium
```bash
export TTS_ENABLED=true
export TTS_VOICE=Marisol     # Voz Premium de España
export TTS_RATE=165
```

### Combinar Voces Diferentes
```bash
# Respuestas con voz femenina México
export TTS_VOICE=Angélica

# Confirmaciones con voz masculina España
export TTS_PROMPT_ENABLED=true
export TTS_PROMPT_VOICE=Jorge
```

### Usar Voces por País

**México:**
```bash
export TTS_VOICE=Angélica  # o Paulina, Juan
```

**España:**
```bash
export TTS_VOICE=Jorge     # o Mónica, Marisol
```

**Argentina:**
```bash
export TTS_VOICE=Diego     # o Isabela
```

**Chile:**
```bash
export TTS_VOICE=Francisca
```

**Colombia:**
```bash
export TTS_VOICE=Carlos    # o Soledad, Jimena
```

## 🔧 Funcionalidades de Detección

El sistema de detección automática sigue este orden:

1. **Búsqueda exacta** (case-insensitive)
   - `export TTS_VOICE=Monica` → Encuentra "Monica" o "Mónica"

2. **Búsqueda parcial**
   - `export TTS_VOICE=angel` → Encuentra "Angélica"
   - `export TTS_VOICE=siri` → Encuentra "Siri Female/Male"

3. **Fallback a español**
   - Si no encuentra la voz, busca primera voz en español

4. **Fallback final**
   - Usa "Monica" o primera voz disponible

## 📖 Documentación Adicional

- **Voces de Siri**: `.claude/hooks/VOCES-SIRI.md`
- **Ejemplos**: `.claude/hooks/EJEMPLOS.md`
- **README**: `.claude/hooks/README.md`
- **Inicio Rápido**: `.claude/hooks/INICIO-RAPIDO.md`

## ✅ Tests Disponibles

```bash
# Test rápido (30 segundos)
./.claude/hooks/test-quick.sh

# Test completo de hooks
./.claude/hooks/test-hooks.sh

# Test de detección de voces
./.claude/hooks/test-siri-voices.sh

# Test de integración
./.claude/hooks/test-integration.sh

# Listar todas las voces
./.claude/hooks/list-all-voices.sh
```

## 🎯 Configuraciones Recomendadas

### Para Trabajo Diario
```bash
export TTS_ENABLED=true
export TTS_VOICE=Paulina      # Voz clara y profesional
export TTS_RATE=175
```

### Para Presentaciones
```bash
export TTS_ENABLED=true
export TTS_VOICE=Jorge        # Voz masculina autoridad
export TTS_RATE=165
```

### Para Aprendizaje
```bash
export TTS_ENABLED=true
export TTS_VOICE=Mónica       # Voz clara de España
export TTS_RATE=150           # Velocidad lenta
```

### Para Desarrollo Rápido
```bash
export TTS_ENABLED=true
export TTS_VOICE=Angélica
export TTS_RATE=220           # Velocidad rápida
export TTS_MAX_LENGTH=300     # Solo mensajes cortos
```

## 🌟 Ventajas de las Voces Enhanced

Las voces Enhanced (mejoradas) ofrecen:

- ✨ Mayor naturalidad
- 🎵 Mejor entonación
- 🗣️ Pronunciación más clara
- 💬 Sonido menos robótico
- 🌍 Mejor manejo de acentos regionales

**Voces Enhanced disponibles en tu sistema:**
- Angélica, Carlos, Diego, Francisca, Isabela
- Jorge, Juan, Marisol, Mónica, Paulina
- Soledad, Jimena

**Voz Premium:**
- Marisol (la mejor calidad disponible)

## 🚀 Próximos Pasos

1. **Probar voces Enhanced:**
   ```bash
   source .claude/hooks/enable-tts.sh
   ```

2. **Elegir tu favorita:**
   - Prueba varias voces Enhanced
   - Selecciona la que mejor suene para ti

3. **Configurar permanentemente:**
   ```bash
   echo 'export TTS_ENABLED=true' >> ~/.zshrc
   echo 'export TTS_VOICE=Angélica' >> ~/.zshrc
   echo 'export TTS_RATE=175' >> ~/.zshrc
   source ~/.zshrc
   ```

4. **Usar con Claude Code:**
   ```bash
   claude-code
   ```

## ❓ FAQ

**P: ¿Cómo instalo voces de Siri?**
R: System Preferences → Accessibility → Spoken Content → System Voices → Buscar "Siri"

**P: ¿Qué diferencia hay entre Enhanced y Premium?**
R: Premium es la calidad más alta, Enhanced es muy buena calidad. Ambas son superiores a las voces estándar.

**P: ¿Puedo usar tildes en los nombres?**
R: Sí, el sistema detecta "Angelica" y "Angélica" automáticamente.

**P: ¿Funcionan las voces en Claude Code?**
R: Sí, solo configura las variables de entorno y los hooks harán el resto.

## 🎉 Resumen

Los hooks ahora son **inteligentes** y detectan automáticamente:
- ✅ **13 voces Enhanced** (incluida 1 Premium)
- ✅ **16 voces estándar en español**
- ✅ **Búsqueda flexible** (exacta, parcial, case-insensitive)
- ✅ **Soporte para Siri** (cuando se instalen)
- ✅ **200+ voces totales** en tu sistema

**¡Disfruta de las voces mejoradas con Claude Code! 🎙️**
