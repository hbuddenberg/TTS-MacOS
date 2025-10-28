#!/usr/bin/env python3
"""
TTS macOS - Herramienta de línea de comandos para Text-to-Speech
"""

import argparse
import subprocess
import sys
from pathlib import Path

__version__ = "1.2.1"

def obtener_voces_sistema():
    """Detecta automáticamente las voces en español disponibles en el sistema"""
    try:
        result = subprocess.run(
            ["say", "-v", "?"],
            capture_output=True,
            text=True,
            check=True
        )
        
        voces = {}
        for linea in result.stdout.split('\n'):
            # Buscar voces en español
            if 'spanish' in linea.lower() or 'español' in linea.lower():
                partes = linea.strip().split()
                if partes:
                    nombre_voz = partes[0]
                    # Crear alias en minúsculas
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

# Detectar voces disponibles en el sistema
VOCES = obtener_voces_sistema()

def hablar(texto, voz="monica", velocidad=175):
    """Reproduce texto usando TTS de macOS"""
    voz_capitalizada = VOCES.get(voz.lower(), "Monica")
    
    try:
        subprocess.run(
            ["say", "-v", voz_capitalizada, "-r", str(velocidad), texto],
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
    """Guarda texto como archivo de audio"""
    voz_capitalizada = VOCES.get(voz.lower(), "Monica")
    
    # Asegurar extensión .aiff
    if not archivo.endswith(".aiff"):
        archivo += ".aiff"
    
    try:
        subprocess.run(
            ["say", "-v", voz_capitalizada, "-o", archivo, texto],
            check=True
        )
        print(f"✅ Audio guardado en: {archivo}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al guardar: {e}", file=sys.stderr)
        return False

def listar_voces():
    """Lista las voces disponibles"""
    print("\n🎤 Voces en español disponibles en tu sistema:\n")
    
    if not VOCES:
        print("   ❌ No se encontraron voces en español instaladas")
        print("\n💡 Para instalar voces:")
        print("   1. Abre Preferencias del Sistema")
        print("   2. Ve a Accesibilidad → Contenido Hablado")
        print("   3. Haz clic en 'Voces del Sistema'")
        print("   4. Descarga voces en español (México, España, Argentina)")
        return
    
    # Obtener información completa de las voces
    try:
        result = subprocess.run(
            ["say", "-v", "?"],
            capture_output=True,
            text=True,
            check=True
        )
        
        voces_info = {}
        for linea in result.stdout.split('\n'):
            for voz_alias, voz_nombre in VOCES.items():
                if linea.strip().startswith(voz_nombre):
                    voces_info[voz_alias] = linea.strip()
                    break
    except:
        voces_info = {}
    
    # Mostrar voces
    for voz_alias in sorted(VOCES.keys()):
        voz_nombre = VOCES[voz_alias]
        if voz_alias in voces_info:
            print(f"  • {voz_alias:12} - {voces_info[voz_alias]}")
        else:
            print(f"  • {voz_alias:12} - {voz_nombre}")
    
    print(f"\n💡 Uso: tts-macos \"tu texto\" --voice {list(VOCES.keys())[0]}")
    print(f"   Total de voces disponibles: {len(VOCES)}\n")

def main():
    # Determinar voz por defecto (la primera disponible)
    voz_default = list(VOCES.keys())[0] if VOCES else "monica"
    
    parser = argparse.ArgumentParser(
        description="🎙️  TTS macOS - Convierte texto a voz usando el TTS nativo de macOS",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Ejemplos de uso:
  tts-macos "Hola mundo"
  tts-macos "Buenos días" --voice {voz_default}
  tts-macos "Texto rápido" --rate 250
  tts-macos "Mensaje" --save mi_audio.aiff
  tts-macos --list
  
  # Con uvx (sin instalar):
  uvx tts-macos "Hola mundo"
  uvx tts-macos "Buenos días" --voice {voz_default} --rate 200

Voces disponibles: {', '.join(sorted(VOCES.keys()))}
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
        choices=list(VOCES.keys()) if VOCES else ["monica"],
        help=f"Voz a utilizar (default: {voz_default})"
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
