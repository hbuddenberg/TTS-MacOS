# TTS Notify v3 — Plan de Desarrollo e Implementación

## 1. Resumen Ejecutivo
- **Objetivo**: Evolucionar TTS Notify a la versión 3 añadiendo soporte opcional para CoquiTTS, clonación de voces y pipelines de audio avanzados sin romper la compatibilidad existente.
- **Alcance clave**:
  - Selección dinámica de motor (`macos` vs `coqui`).
  - Perfiles de voz personalizados basados en samples de audio.
  - Pipeline modular de preprocesamiento y conversión.
  - Extensiones CLI, MCP y futura API REST.
  - Telemetría básica y fallback seguro.
- **Resultados esperados**: Plataforma TTS flexible, capaz de aprovechar modelos neuronales, manteniendo la facilidad de uso actual y una arquitectura escalable.

---

## 2. Alcance por Fases

| Fase | Objetivos | Hitos |
| ---- | --------- | ----- |
| A | Motor Coqui básico y selección de engine | Registro condicional, síntesis simple, CLI `--engine` |
| B | Perfiles de voz (clonación) y embeddings persistentes | Gestión de perfiles, CLI/MCP para creación y listado |
| C | Pipeline de audio + conversión formatos | Normalización, trimming, reducción de ruido opcional, `format_converter` |
| D | Extensiones MCP/API + telemetría | Nuevos tools MCP, endpoints API preliminares, métricas básicas |
| E | Fine-tuning experimental (flag) | Documentar y habilitar flags para investigación futura |

Las fases son incrementales; cada una puede desplegarse tras pruebas específicas sin bloquear las demás.

---

## 3. Cambios Arquitectónicos y Estructura de Directorios

```
tts_notify/
  core/
    coqui_engine.py
    voice_profile_manager.py
    audio_pipeline.py
    embeddings/
      coqui_embedding.py
      speaker_index.py
  plugins/
    preprocess/
      silence_trimmer.py
      noise_reducer.py
      normalizer.py
    conversion/
      format_converter.py
  data/
    voices/
      profiles/
      embeddings/
      samples/
  utils/
    telemetry.py
    resource_monitor.py
```

- **core/** aloja los motores y lógicas de negocio principales.
- **plugins/** permite agregar/activar transformaciones sin modificar núcleo.
- **data/** conserva artefactos generados por usuarios (perfiles, audios, embeddings) con estructura clara.
- **utils/** incorpora monitorización y métricas.

---

## 4. Extensión de Configuración (TTSConfig)

### Campos nuevos propuestos
- `TTS_NOTIFY_ENGINE` (macos|coqui)
- `TTS_NOTIFY_COQUI_MODEL`, `TTS_NOTIFY_COQUI_MODEL_TYPE`
- `TTS_NOTIFY_COQUI_USE_GPU`, `TTS_NOTIFY_COQUI_AUTOINIT`
- `TTS_NOTIFY_COQUI_SPEAKER`, `TTS_NOTIFY_COQUI_STYLE`
- `TTS_NOTIFY_COQUI_PROFILE_DIR`, `TTS_NOTIFY_COQUI_EMBEDDING_DIR`
- `TTS_NOTIFY_COQUI_ENABLE_CLONING`
- `TTS_NOTIFY_COQUI_MIN_SAMPLE_SECONDS`, `TTS_NOTIFY_COQUI_MAX_SAMPLE_SECONDS`
- `TTS_NOTIFY_COQUI_AUTO_CLEAN_AUDIO`, `TTS_NOTIFY_COQUI_AUTO_TRIM_SILENCE`
- `TTS_NOTIFY_COQUI_NOISE_REDUCTION`, `TTS_NOTIFY_COQUI_DIARIZATION`
- `TTS_NOTIFY_COQUI_CONVERSION_ENABLED`, `TTS_NOTIFY_COQUI_TARGET_FORMATS`
- `TTS_NOTIFY_COQUI_EMBEDDING_CACHE`, `TTS_NOTIFY_COQUI_EMBEDDING_FORMAT`
- `TTS_NOTIFY_EXPERIMENTAL_FINE_TUNING`

### Validaciones
- Si `ENGINE=coqui` y no hay modelo ⇒ error.
- Auto-creación de directorios si no se definen.
- GPU solicitada sin soporte ⇒ se fuerza CPU y se registra advertencia.

---

## 5. Motor CoquiTTSEngine (Fase A)

### Requisitos
- Dependencias opcionales (`pip install .[coqui]`).
- Inicialización lazy (`asyncio.to_thread` para evitar bloquear event loop).
- Métodos mínimos: `initialize`, `cleanup`, `is_available`, `get_supported_voices`, `speak`, `synthesize`, `save`.
- Compatibilidad con respuestas `TTSResponse` y control de formatos (WAV por defecto, conversión posterior).
- Logging claro para diagnósticos.

### Pasos
1. Crear `coqui_engine.py` en `core/`.
2. Actualizar bootstrap en `tts_engine.py` para registrar Coqui solo si config/entorno lo solicitan y la dependencia está disponible.
3. Extender CLI (`--engine`, `--model`) para seleccionar motor y modelo.
4. Validar fallback a `macos` si Coqui no está disponible.

---

## 6. Voice Cloning & Voice Profiles (Fase B)

### Componentes
- `voice_profile_manager.py`: creación, lectura, eliminación de perfiles.
- Directorio `data/voices/profiles` (metadatos JSON/YAML).
- Directorio `data/voices/embeddings` (archivos `.npy` o `.pt`).
- Directorio `data/voices/samples` (audios fuente).

### Flujo de creación de perfil
1. Validar audios (formato, duración, nivel).
2. Pipeline de audio (limpieza, normalización, trimming, opcional diarización).
3. Extracción de embeddings (depende del modelo; preferir XTTS o similares).
4. Agregado de embeddings (media ponderada, normalización).
5. Guardado de metadata (idioma, género estimado, estadísticas).
6. Registro de voz en `VoiceManager` como `Voice` con `metadata.embedding_path`.

### Nuevos comandos/flags CLI
- `--clone --name <id> --files <lista>`: crear perfil personalizado.
- `--list-profiles`: enumerar perfiles disponibles.
- `--speaker <id>` / `--style <id>`: seleccionar speaker/estilo nativo de modelo.
- `--voice <profile_id>`: usar perfil clonando (mapeado por `VoiceManager`).

### Nuevos tools MCP
- `create_voice_profile`
- `list_voice_profiles`
- `describe_voice_profile`
- Integración segura: validar existencia, retornar mensajes claros y rutas relativas.

---

## 7. Pipeline de Audio (Fase C)

### Objetivos
- Preprocesar audios de entrada para mejorar calidad de embeddings y voz resultante.
- Operaciones configurables:
  - Resample y normalización (RMS o LUFS simple).
  - Eliminación de silencios extremos.
  - Reducción de ruido (spectral gating).
  - Diarización segmentada (cuando se habilite).

### Diseño
- `audio_pipeline.py` con clase `AudioPipeline` que reciba `config` y devuelva lista de segmentos procesados (`Path`).
- `plugins/preprocess/` para cada etapa, desacopladas y activables según config.
- Uso de librerías como `librosa`, `soundfile`, `pydub`.
- Flags para activar/desactivar (`TTS_NOTIFY_COQUI_NOISE_REDUCTION`, etc.).

---

## 8. Conversión de Formatos (Fase C)

- Plugin `plugins/conversion/format_converter.py`.
- Entrada: WAV (generado por Coqui).
- Salida: MP3, FLAC, OGG (según `TTS_NOTIFY_COQUI_TARGET_FORMATS`).
- Dependencias opcionales: `pydub`, `ffmpeg`.
- Integrado en `CoquiTTSEngine.save()` y `synthesize()`:
  - Si formato deseado ≠ WAV ⇒ ejecutar conversión (con logs y manejo de errores).
  - Mantener AIFF como default para macOS.

---

## 9. Extensiones CLI y UX

### Flags clave
- `--engine`, `--model`, `--speaker`, `--style`.
- `--clone`, `--files`, `--name`, `--list-profiles`.
- `--convert <archivo> --to <formato>`.
- `--diagnose-engine <engine>` (verificar disponibilidad, dependencias, tiempo de init).

### Flujos
- Al iniciar CLI:
  1. Cargar config según perfil/env.
  2. `bootstrap_engines(config)`.
  3. Si se solicitan operaciones de gestión (clonación/listado) ⇒ ejecutarlas y salir.
  4. Para síntesis/guardado ⇒ seleccionar motor, voice (nativo o perfil), ejecutar.

  Para el comando `--list`, se listará el motor activo: por defecto el configurado (generalmente macOS) y, si se especifica `--engine`, se mostrará el inventario correspondiente (por ejemplo `--engine coqui --list`).

---

## 10. Extensiones MCP (Fase D)

### Nuevas herramientas
1. `create_voice_profile` (argumentos: nombre, lista de archivos, metadata opcional).
2. `list_voice_profiles`.
3. `describe_voice_profile`.
4. `engine_info` (devuelve capacidades, formatos y estado de inicialización).
5. `convert_audio` (archivo + formato destino, cuando conversión habilitada).

### Consideraciones
- Validar rutas relativas y asegurar que MCP no bloquee el proceso (usar `asyncio.to_thread` para tareas pesadas).
- Documentar esquemas de respuesta JSON.

---

## 11. API REST (Opcional v3 / v3.1)

Endpoints sugeridos:
- `POST /profiles` (multipart) — crea perfil.
- `GET /profiles` — lista.
- `GET /profiles/{id}` — metadata.
- `DELETE /profiles/{id}` — eliminación.
- `POST /tts` — síntesis (motor, perfil, speaker).
- `GET /voices` — voces disponibles.
- `GET /engines` — resumen.
- `POST /convert` — conversión de formatos.

Requiere FastAPI/Starlette en extras específicos. Puede planificarse para v3.1 si el tiempo es limitado.

---

## 12. Telemetría y Monitorización (Fase D)

- `utils/telemetry.py`: registrar duración de síntesis, tamaño de audio, uso de memoria (psutil) y almacenar JSON (`data/telemetry/metrics.json`).
- `utils/resource_monitor.py`: comprobar GPU, memoria, threads activos.
- Exponer información vía CLI (`--diagnose-engine`) y MCP (`engine_info`).

---

## 13. Seguridad y Privacidad

- Guardar datos de usuario localmente (no subir a servicios externos).
- Proveer comando `--purge-profile <id>` para eliminar perfiles sensibles.
- Almacenar checksums en metadata para detectar corrupción.
- Validar tipo de archivo y duración antes de aceptar la clonación.
- Documentar prácticas recomendadas (audios limpios, sin ruido).

---

## 14. Rendimiento y Optimización

### Targets iniciales
- Latencia de síntesis Coqui (texto corto) ≤ 2.5 × latencia de `say`.
- Creación de perfil con 2 muestras ≤ 30 segundos.
- Uso de memoria estable (sin growth tras 50 peticiones).

### Estrategias
- Cachear instancia de modelo Coqui mientras no cambie el nombre del modelo.
- Cache de embeddings (`TTS_NOTIFY_COQUI_EMBEDDING_CACHE`).
- Limitar concurrencia (`TTS_NOTIFY_MAX_CONCURRENT`).
- Reutilizar threads en conversions/preprocesamiento si es necesario.

---

## 15. Fallback y Manejo de Errores

- Si Coqui no está disponible ⇒ log WARN, fallback a macOS.
- Si embedding inválido ⇒ mensaje y fallback a speaker/model default.
- Si modelo no soporta estilo ⇒ ignorar estilo y registrar aviso.
- Si GPU no disponible ⇒ fallback CPU automático.

---

## 16. Feature Flags

| Flag | Función |
| ---- | ------- |
| `TTS_NOTIFY_COQUI_ENABLE_CLONING` | Activar/desactivar clonación. |
| `TTS_NOTIFY_COQUI_NOISE_REDUCTION` | Habilitar reducción de ruido. |
| `TTS_NOTIFY_COQUI_DIARIZATION` | Activar diarización de audio. |
| `TTS_NOTIFY_EXPERIMENTAL_FINE_TUNING` | Permitir rutas experimentales de fine-tuning. |

---

## 17. Plan de Pruebas

### Casos esenciales
1. CLI con `macos` (sin extras) ⇒ sin cambios en flujo base.
2. CLI con Coqui instalado ⇒ síntesis simple (`--engine coqui`).
3. Clonación con 1 sample muy corto ⇒ rechazo esperado.
4. Clonación con 2 samples válidos ⇒ creación, listado y uso del perfil.
5. Conversión WAV→MP3 ⇒ archivo generado y reproducible.
6. MCP `create_voice_profile` ⇒ confirmación JSON.
7. Estrés: 10 peticiones concurrentes (evaluar latencia y memoria).
8. Fallback GPU solicitado sin soporte.

### Scripts sugeridos
- `scripts/tests/test_coqui_engine.py`: pruebas unitarias/mocked.
- `scripts/tests/test_voice_profiles.py`: creación/listado.
- `scripts/tests/test_pipeline.py`: validar preprocesamiento.
- `scripts/benchmarks/benchmark_tts.py`: medir tiempos.

---

## 18. Checklist Técnico

- [ ] Extender `TTSConfig` con nuevos campos y validaciones.
- [ ] Añadir extras opcionales en `pyproject.toml`.
- [ ] Implementar `coqui_engine.py` (fase A).
- [ ] Modificar bootstrap en `tts_engine.py`.
- [ ] Actualizar CLI con flags `--engine`, `--model`, etc.
- [ ] Implementar clonación (`voice_profile_manager.py`, embeddings, pipeline básico).
- [ ] Integrar perfiles en `VoiceManager`.
- [ ] Crear plugins de preprocesamiento y conversión (stubs funcionales).
- [ ] Extender MCP con nuevos tools.
- [ ] (Opcional) Añadir endpoints API REST.
- [ ] Añadir telemetría (duración, memoria).
- [ ] Actualizar documentación (README-v3, VOICE_CLONING.md, MIGRATION-GUIDE-v3.md).
- [ ] Ejecutar pruebas y documentar resultados.

---

## 19. Migración de v2 a v3

- Crear `MIGRATION-GUIDE-v3.md` con pasos:
  - Para seguir usando macOS nativo: sin cambios.
  - Para Coqui: `pip install .[coqui]`.
  - Para clonación con diarización: `pip install .[coqui,diarization]`.
  - Nuevos comandos CLI/MCP y ejemplos.
- Mantener compatibilidad de argumentos existentes; nuevos flags son opt-in.

---

## 20. Roadmap Posterior

| Versión | Mejora |
| ------- | ------ |
| v3.1 | API REST formal y conversión avanzada (bitrate, sample rate). |
| v3.2 | Soporte para fine-tuning incremental (LoRA/adapter) bajo flag experimental. |
| v3.3 | Combinación de perfiles (voz + estilo). |
| v3.4 | Diarización robusta y detección automática de idioma. |
| v3.5 | Exportación/importación de perfiles y backups cifrados. |

---

## 21. Métricas de Éxito

- Latencia aceptable en síntesis Coqui (texto corto) ≤ 2.5× macOS.
- Perfiles clonados reutilizables sin errores en 95% de casos.
- Fallback seguro y documentado.
- Reporte de telemetría accesible y útil para diagnósticos.
- Usuarios pueden crear su perfil en < 5 minutos con audios adecuados.

---

## 22. Próximos Pasos Inmediatos (Fase A)

1. Añadir campos a `TTSConfig` y actualizar `config_manager`.
2. Crear `coqui_engine.py` y ajustar bootstrap de motores.
3. Añadir flag `--engine` y `--model` en CLI.
4. Verificar fallback cuando Coqui no está disponible.
5. Documentar las instrucciones de instalación de extras.

Una vez completado, avanzar a la Fase B (clonación) siguiendo los artefactos y módulos definidos.

---

**Plan creado por:** Equipo de Ingeniería TTS Notify  
**Versión del documento:** 1.0  
**Fecha:** *(actualizar al momento de guardar)*
