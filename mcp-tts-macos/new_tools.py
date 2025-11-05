
@app.list_tools()
async def list_tools() -> list[Tool]:
    """
    Lista las herramientas disponibles en el servidor MCP
    """
    return [
        Tool(
            name="speak_text",
            description="Convierte texto a voz y lo reproduce usando el TTS nativo de macOS. Soporta TODAS las voces del sistema incluyendo español, Siri, Enhanced y Premium. Puede forzar variante específica con el parámetro 'type'.",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "El texto que deseas convertir a audio",
                    },
                    "voice": {
                        "type": "string",
                        "description": "Nombre de la voz a utilizar (ej: Monica, Jorge, Siri, Angélica). Acepta cualquier voz instalada en el sistema. Usa list_voices para ver opciones.",
                        "default": "monica",
                    },
                    "rate": {
                        "type": "integer",
                        "description": "Velocidad de lectura en palabras por minuto (100-300). Default: 175",
                        "default": 175,
                        "minimum": 100,
                        "maximum": 300,
                    },
                    "type": {
                        "type": "string",
                        "description": "Forzar variante específica de voz (normal/enhanced/premium/siri). Útil para voces con múltiples variantes como Marisol (Enhanced + Premium).",
                        "enum": ["normal", "enhanced", "premium", "siri"],
                    },
                },
                "required": ["text"],
            },
        ),
        Tool(
            name="list_voices",
            description="Lista TODAS las voces disponibles en el sistema macOS categorizadas por tipo: Español, Siri, Enhanced/Premium y otras",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="save_audio",
            description="Convierte texto a voz y lo guarda como archivo de audio (AIFF). Soporta todas las voces del sistema. Puede forzar variante específica con el parámetro 'type'.",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "El texto a convertir"},
                    "filename": {"type": "string", "description": "Nombre del archivo (sin extensión)"},
                    "voice": {
                        "type": "string",
                        "description": "Nombre de la voz a utilizar (ej: Monica, Jorge, Siri, Angélica)",
                        "default": "monica",
                    },
                    "type": {
                        "type": "string",
                        "description": "Forzar variante específica de voz (normal/enhanced/premium/siri). Útil para voces con múltiples variantes como Marisol (Enhanced + Premium).",
                        "enum": ["normal", "enhanced", "premium", "siri"],
                    },
                },
                "required": ["text", "filename"],
            },
        ),
    ]
