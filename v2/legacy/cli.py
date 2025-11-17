"""
Legacy CLI - Preserves TTS-MacOS v1.4.4 CLI functionality

This module maintains the exact CLI implementation from v1.4.4
for complete backward compatibility.
"""

import argparse
import subprocess
import sys
import unicodedata
from pathlib import Path
from typing import Dict, List, Optional

from .voice_detector import LegacyVoiceDetector


class LegacyCLI:
    """
    Preserves v1.4.4 CLI functionality for backward compatibility
    """

    def __init__(self):
        self.version = "1.4.4"
        self.voice_detector = LegacyVoiceDetector()

    def normalize_text(self, text: str) -> str:
        """Normaliza texto removiendo acentos para comparación"""
        # Normalizar a NFD (separa caracteres base de acentos)
        nfd = unicodedata.normalize("NFD", text)
        # Filtrar los acentos (categoría Mn = Nonspacing Mark)
        without_accents = "".join(c for c in nfd if unicodedata.category(c) != "Mn")
        return without_accents.lower()

    def obtener_voces_sistema(self, solo_espanol=False):
        """Detecta automáticamente las voces disponibles en el sistema"""
        return self.voice_detector.obtener_voces_sistema(solo_espanol)

    def buscar_voz(self, voz_solicitada: str, voces: Dict[str, str]) -> Optional[str]:
        """Busca una voz usando el algoritmo flexible de v1.4.4"""
        return self.voice_detector.buscar_voz(voz_solicitada, voces)

    def listar_vocices_categorizadas(self):
        """Lista las voces categorizadas según la lógica v1.4.4"""
        categorias = self.voice_detector.categorizar_voces()

        print("\\n=== VOCES DISPONIBLES ===\\n")

        total_voces = 0
        for categoria, voces in categorias.items():
            if voces:
                print(f"🎭 {categoria} ({len(voces)} voces):")
                for voz in voces:
                    genero_icono = "👨" if voz["gender"] == "Masculino" else "👩"
                    idioma_flag = self._get_flag_idioma(voz["language"])
                    print(
                        f"  {genero_icono} {voz['name']} - {idioma_flag} {voz['description']}"
                    )
                    total_voces += 1
                print()

        print(f"📊 Total: {total_voces} voces detectadas")

    def _get_flag_idioma(self, language_code: str) -> str:
        """Retorna emoji de bandera para el idioma"""
        flags = {
            "es": "🇪🇸",
            "es-ES": "🇪🇸",
            "es-MX": "🇲🇽",
            "en": "🇺🇸",
            "en-US": "🇺🇸",
            "en-GB": "🇬🇧",
            "fr": "🇫🇷",
            "de": "🇩🇪",
            "it": "🇮🇹",
            "pt": "🇵🇹",
        }
        return flags.get(language_code, "🌍")

    def sintetizar_voz(
        self,
        texto: str,
        voz: Optional[str] = None,
        rate: int = 175,
        output_file: Optional[str] = None,
    ) -> bool:
        """Sintetiza texto usando el comando say de macOS"""
        try:
            cmd = ["say"]

            # Agregar voz si se especifica
            if voz:
                # Obtener voces del sistema para validación
                voces = self.obtener_voces_sistema()
                voz_valida = self.buscar_voz(voz, voces)

                if voz_valida:
                    cmd.extend(["-v", voz_valida])
                else:
                    print(f"⚠️  Voz '{voz}' no encontrada, usando voz por defecto")

            # Agregar rate si es diferente al default
            if rate != 175:
                cmd.extend(["-r", str(rate)])

            # Agregar archivo de salida si se especifica
            if output_file:
                cmd.extend(["-o", output_file])

            # Agregar texto
            cmd.append(texto)

            # Ejecutar comando
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode != 0:
                print(f"❌ Error en síntesis: {result.stderr}")
                return False

            if output_file:
                print(f"✅ Audio guardado en: {output_file}")

            return True

        except Exception as e:
            print(f"❌ Error sintetizando voz: {e}")
            return False

    def crear_parser(self) -> argparse.ArgumentParser:
        """Crea el parser de argumentos CLI según la lógica v1.4.4"""
        parser = argparse.ArgumentParser(
            description="TTS-MacOS v1.4.4 - Herramienta de Text-to-Speech para macOS",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Ejemplos de uso:
  %(prog)s "Hola mundo" --voice monica
  %(prog)s --list
  %(prog)s "Test" --voice jorge --rate 200 --output test.aiff
            """,
        )

        # Argumentos posicionales
        parser.add_argument("texto", nargs="?", help="Texto a convertir a voz")

        # Opciones principales
        parser.add_argument(
            "-v", "--voice", help="Voz a utilizar (ej: monica, jorge, angelica)"
        )

        parser.add_argument(
            "-r",
            "--rate",
            type=int,
            default=175,
            help="Velocidad de habla (palabras por minuto, default: 175)",
        )

        parser.add_argument(
            "-o", "--output", help="Archivo de salida para guardar audio (formato AIFF)"
        )

        parser.add_argument(
            "--list",
            action="store_true",
            help="Listar todas las voces disponibles categorizadas",
        )

        parser.add_argument(
            "--version", action="version", version=f"TTS-MacOS {self.version}"
        )

        return parser

    def run(self, args: List[str] = None) -> int:
        """Ejecuta el CLI con los argumentos proporcionados"""
        parser = self.crear_parser()
        parsed_args = parser.parse_args(args)

        # Si solo se quiere listar voces
        if parsed_args.list:
            self.listar_vocices_categorizadas()
            return 0

        # Validar que se proporcionó texto
        if not parsed_args.texto:
            print("❌ Error: Debes proporcionar un texto para convertir a voz")
            print("   Usa --list para ver voces disponibles")
            parser.print_help()
            return 1

        # Validar rate
        if not (100 <= parsed_args.rate <= 300):
            print("❌ Error: El rate debe estar entre 100 y 300 palabras por minuto")
            return 1

        # Realizar síntesis
        success = self.sintetizar_voz(
            texto=parsed_args.texto,
            voz=parsed_args.voice,
            rate=parsed_args.rate,
            output_file=parsed_args.output,
        )

        return 0 if success else 1


# Función principal para compatibilidad con v1.4.4
def main():
    """Función principal que mantiene compatibilidad con v1.4.4"""
    cli = LegacyCLI()
    sys.exit(cli.run())


if __name__ == "__main__":
    main()
