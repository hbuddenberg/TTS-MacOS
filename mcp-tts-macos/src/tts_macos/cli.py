#!/usr/bin/env python3
"""
TTS macOS - Herramienta de línea de comandos para Text-to-Speech
"""

import argparse
import subprocess
import sys
import unicodedata
from pathlib import Path

__version__ = "1.3.0"

def normalize_text(text):
    """Normaliza texto removiendo acentos para comparación

    Args:
        text: Texto a normalizar

    Returns:
        Texto sin acentos en minúsculas
    """
    # Normalizar a NFD (separa caracteres base de acentos)
    nfd = unicodedata.normalize('NFD', text)
    # Filtrar los acentos (categoría Mn = Nonspacing Mark)
    without_accents = ''.join(c for c in nfd if unicodedata.category(c) != 'Mn')
    return without_accents.lower()

def obtener_voces_sistema(solo_espanol=False):
    """Detecta automáticamente las voces disponibles en el sistema

    Args:
        solo_espanol: Si es True, solo retorna voces en español
    """
    try:
        result = subprocess.run(
            ["say", "-v", "?"],
            capture_output=True,
            text=True,
            check=True
        )

        voces = {}
        for linea in result.stdout.split('\n'):
            partes = linea.strip().split()
            if not partes:
                continue

            nombre_voz = partes[0]
            linea_lower = linea.lower()

            # Si solo queremos español, filtrar
            if solo_espanol:
                if 'spanish' in linea_lower or 'español' in linea_lower:
                    voces[nombre_voz.lower()] = nombre_voz
            else:
                # Incluir TODAS las voces
                voces[nombre_voz.lower()] = nombre_voz

        return voces
    except:
        # Fallback a voces predeterminadas si hay error
        return {
            "monica": "Monica",
            "paulina": "Paulina",
            "jorge": "Jorge",
            "juan": "Juan",
            "diego": "Diego",
            "angelica": "Angelica"
        }

def categorizar_voces():
    """Categoriza las voces disponibles por tipo"""
    try:
        result = subprocess.run(
            ["say", "-v", "?"],
            capture_output=True,
            text=True,
            check=True
        )

        categorias = {
            'espanol': [],
            'siri': [],
            'enhanced': [],
            'premium': [],
            'otras': []
        }

        for linea in result.stdout.split('\n'):
            if not linea.strip():
                continue

            partes = linea.strip().split()
            if not partes:
                continue

            nombre_voz = partes[0]
            linea_lower = linea.lower()

            # Categorizar
            if 'spanish' in linea_lower or 'español' in linea_lower:
                categorias['espanol'].append((nombre_voz, linea.strip()))

            if 'siri' in linea_lower:
                categorias['siri'].append((nombre_voz, linea.strip()))

            if 'enhanced' in linea_lower:
                categorias['enhanced'].append((nombre_voz, linea.strip()))

            if 'premium' in linea_lower:
                categorias['premium'].append((nombre_voz, linea.strip()))

            # Si no está en ninguna categoría específica
            if not any([
                'spanish' in linea_lower,
                'español' in linea_lower,
                'siri' in linea_lower,
                'enhanced' in linea_lower,
                'premium' in linea_lower
            ]):
                categorias['otras'].append((nombre_voz, linea.strip()))

        return categorias
    except:
        return None

def buscar_voz_en_sistema(query):
    """Busca una voz en el sistema de forma flexible

    Args:
        query: Nombre de la voz a buscar

    Returns:
        Nombre correcto de la voz o None
    """
    try:
        result = subprocess.run(
            ["say", "-v", "?"],
            capture_output=True,
            text=True,
            check=True
        )

        query_normalized = normalize_text(query)

        # 1. Búsqueda exacta (case-insensitive y accent-insensitive)
        for linea in result.stdout.split('\n'):
            partes = linea.strip().split()
            if partes:
                nombre_voz = partes[0]
                if normalize_text(nombre_voz) == query_normalized:
                    return nombre_voz

        # 2. Búsqueda por inicio de nombre (prioridad)
        for linea in result.stdout.split('\n'):
            partes = linea.strip().split()
            if partes:
                nombre_voz = partes[0]
                if normalize_text(nombre_voz).startswith(query_normalized):
                    return nombre_voz

        # 3. Búsqueda parcial en toda la línea (accent-insensitive)
        for linea in result.stdout.split('\n'):
            if query_normalized in normalize_text(linea):
                partes = linea.strip().split()
                if partes:
                    return partes[0]

        return None
    except:
        return None

# Detectar voces disponibles en el sistema
VOCES = obtener_voces_sistema()

def hablar(texto, voz="monica", velocidad=175):
    """Reproduce texto usando TTS de macOS con búsqueda flexible de voces"""
    # Primero intentar con las voces conocidas
    voz_encontrada = VOCES.get(voz.lower())

    # Si no está en VOCES, buscar en el sistema
    if not voz_encontrada:
        voz_encontrada = buscar_voz_en_sistema(voz)

    # Fallback final
    if not voz_encontrada:
        voz_encontrada = "Monica"

    try:
        subprocess.run(
            ["say", "-v", voz_encontrada, "-r", str(velocidad), texto],
            check=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al reproducir: {e}", file=sys.stderr)
        return False
    except FileNotFoundError:
        print("❌ Comando 'say' no encontrado. ¿Estás en macOS?", file=sys.stderr)
        return False

def guardar(texto, archivo, voz="monica"):
    """Guarda texto como archivo de audio con búsqueda flexible de voces"""
    # Primero intentar con las voces conocidas
    voz_encontrada = VOCES.get(voz.lower())

    # Si no está en VOCES, buscar en el sistema
    if not voz_encontrada:
        voz_encontrada = buscar_voz_en_sistema(voz)

    # Fallback final
    if not voz_encontrada:
        voz_encontrada = "Monica"

    # Asegurar extensión .aiff
    if not archivo.endswith(".aiff"):
        archivo += ".aiff"

    try:
        subprocess.run(
            ["say", "-v", voz_encontrada, "-o", archivo, texto],
            check=True
        )
        print(f"✅ Audio guardado en: {archivo}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al guardar: {e}", file=sys.stderr)
        return False

def listar_voces():
    """Lista todas las voces disponibles categorizadas"""
    categorias = categorizar_voces()

    if not categorias:
        print("❌ No se pudo obtener la lista de voces del sistema")
        return

    print("\n🎙️  VOCES DISPONIBLES EN EL SISTEMA")
    print("═══════════════════════════════════════════════════════════")
    print("")

    # Voces en Español
    if categorias['espanol']:
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"📍 VOCES EN ESPAÑOL ({len(categorias['espanol'])})")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        for nombre, info in sorted(categorias['espanol']):
            print(f"  {nombre:15} {info[len(nombre):].strip()}")
        print("")

    # Voces Enhanced/Premium
    enhanced_premium = categorias['enhanced'] + categorias['premium']
    if enhanced_premium:
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"⭐ VOCES ENHANCED/PREMIUM ({len(set([v[0] for v in enhanced_premium]))})")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        # Eliminar duplicados manteniendo orden
        seen = set()
        for nombre, info in enhanced_premium:
            if nombre not in seen:
                seen.add(nombre)
                print(f"  {nombre:15} {info[len(nombre):].strip()}")
        print("")

    # Voces de Siri
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("🤖 VOCES DE SIRI")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    if categorias['siri']:
        for nombre, info in sorted(categorias['siri']):
            print(f"  {nombre:15} {info[len(nombre):].strip()}")
        print("")
        print("  ⚠️  Nota: Las voces de Siri pueden estar instaladas pero")
        print("     NO son accesibles con 'say -v' por limitaciones de Apple")
    else:
        print("  ⚠️  LIMITACIÓN TÉCNICA:")
        print("  Las voces de Siri NO son accesibles con este comando")
        print("  por restricciones de Apple en el sistema TTS.")
        print("")
        print("  ✅ ALTERNATIVA RECOMENDADA:")
        print("  Usa voces Enhanced/Premium que ofrecen calidad similar:")
        print("  • Mónica (Enhanced)   - España, calidad profesional")
        print("  • Jorge (Enhanced)    - España, voz masculina natural")
        print("  • Angélica (Enhanced) - México, voz femenina clara")
        print("")
        print("  📖 Más información: ver archivo SIRI-VOICES-GUIDE.md")
    print("")

    # Total
    total_voces = len(VOCES)
    print("═══════════════════════════════════════════════════════════")
    print(f"  Total de voces: {total_voces}")
    print("═══════════════════════════════════════════════════════════")
    print("")
    print("💡 Uso:")
    print("  tts-macos \"Hola mundo\" --voice Monica")
    print("  tts-macos \"Hola mundo\" --voice Siri")
    print("  tts-macos \"Hola mundo\" --voice Angélica")
    print("")

def main():
    # Determinar voz por defecto (la primera disponible)
    voz_default = list(VOCES.keys())[0] if VOCES else "monica"

    # Detectar ruta del proyecto REAL para el ejemplo de MCP
    import os
    import sys

    # Estrategia 1: Buscar en la ruta del script actual
    script_path = Path(__file__).resolve()
    project_dir = None

    # Si el script está en mcp-tts-macos/src/tts_macos/cli.py
    if 'mcp-tts-macos' in str(script_path):
        # Extraer la ruta hasta mcp-tts-macos
        parts = str(script_path).split('mcp-tts-macos')
        potential_dir = Path(parts[0] + 'mcp-tts-macos')
        if (potential_dir / 'server.py').exists():
            project_dir = potential_dir

    # Estrategia 2: Buscar server.py en el directorio actual o sus padres
    if project_dir is None:
        current_dir = Path.cwd()
        for _ in range(5):
            if (current_dir / 'server.py').exists():
                project_dir = current_dir
                break
            if (current_dir / 'mcp-tts-macos' / 'server.py').exists():
                project_dir = current_dir / 'mcp-tts-macos'
                break
            current_dir = current_dir.parent
            if str(current_dir) == '/':
                break

    # Estrategia 3: Buscar 'mcp-tts-macos' en el cwd
    if project_dir is None:
        cwd = Path.cwd()
        if 'mcp-tts-macos' in str(cwd):
            parts = str(cwd).split('mcp-tts-macos')
            project_dir = Path(parts[0] + 'mcp-tts-macos')
        else:
            # Última opción: usar cwd con nota
            project_dir = cwd

    ejemplo_venv = f"{project_dir}/venv/bin/python"
    ejemplo_server = f"{project_dir}/server.py"

    # Verificar si detectamos el proyecto correctamente
    if (Path(ejemplo_server).exists()):
        nota_rutas = "✅ Rutas detectadas automáticamente del proyecto actual"
    else:
        nota_rutas = "⚠️  Ejecuta este comando desde el directorio del proyecto para ver rutas correctas"

    parser = argparse.ArgumentParser(
        description="🎙️  TTS macOS - Convierte texto a voz usando el TTS nativo de macOS",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EJEMPLOS DE USO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 Instalado globalmente:
  tts-macos "Hola mundo"
  tts-macos "Buenos días" --voice Monica
  tts-macos "Texto rápido" --rate 250
  tts-macos "Mensaje" --save mi_audio.aiff
  tts-macos --list

🚀 Con uvx (sin instalar):
  uvx --from /ruta/al/proyecto tts-macos "Hola mundo"
  uvx --from . tts-macos "Buenos días" --voice Jorge --rate 200
  uvx --from . tts-macos --list

  # Crear alias para uso frecuente:
  alias tts='uvx --from ~/ruta/al/proyecto tts-macos'
  tts "Ahora es más fácil"
  tts --list

🎭 Voces Enhanced/Premium:
  tts-macos "Calidad superior" --voice "Angélica (Enhanced)"
  tts-macos "Voz premium" --voice "Marisol (Premium)"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BÚSQUEDA FLEXIBLE DE VOCES

Puedes usar nombres parciales o sin acentos:
  --voice monica       → Mónica
  --voice angelica     → Angélica
  --voice siri         → Siri Female (si está instalada)
  --voice "jorge enh"  → Jorge (Enhanced)

Total de voces detectadas: {len(VOCES)}
Usa --list para ver todas las voces disponibles organizadas por categoría
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🤖 CONFIGURACIÓN DEL SERVIDOR MCP (para Claude Desktop)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{nota_rutas}

Archivo: ~/Library/Application Support/Claude/claude_desktop_config.json

{{
  "mcpServers": {{
    "tts-macos": {{
      "command": "{ejemplo_venv}",
      "args": ["{ejemplo_server}"]
    }}
  }}
}}

⚠️  Importante:
  • Usa rutas ABSOLUTAS (ajusta las rutas según tu instalación)
  • Asegúrate de crear el venv primero: python3 -m venv venv
  • Instala dependencias: pip install -r requirements.txt

💡 Instalación automática: ./install.sh
📖 Documentación completa: README.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        """
    )
    
    parser.add_argument(
        "texto",
        nargs="?",
        help="Texto a convertir en voz"
    )
    
    parser.add_argument(
        "-v", "--voice",
        default=voz_default,
        help=f"Voz a utilizar - cualquier voz del sistema (default: {voz_default}). Usa --list para ver todas las opciones"
    )
    
    parser.add_argument(
        "-r", "--rate",
        type=int,
        default=175,
        help="Velocidad en palabras por minuto (100-300, default: 175)"
    )
    
    parser.add_argument(
        "-s", "--save",
        metavar="ARCHIVO",
        help="Guardar audio en archivo (formato .aiff)"
    )
    
    parser.add_argument(
        "-l", "--list",
        action="store_true",
        help="Listar voces disponibles"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"tts-macos {__version__}"
    )
    
    args = parser.parse_args()
    
    # Listar voces
    if args.list:
        listar_voces()
        return 0
    
    # Validar que hay texto
    if not args.texto:
        parser.print_help()
        return 1
    
    # Validar velocidad
    if not 100 <= args.rate <= 300:
        print("⚠️  Velocidad debe estar entre 100 y 300 palabras por minuto", file=sys.stderr)
        return 1
    
    # Guardar archivo
    if args.save:
        success = guardar(args.texto, args.save, args.voice)
        if not success:
            return 1
    
    # Reproducir audio
    success = hablar(args.texto, args.voice, args.rate)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
