"""
Legacy Voice Detector - Preserves v1.4.4 voice detection functionality

This module maintains the exact voice detection and categorization logic
from TTS-MacOS v1.4.4 for backward compatibility.
"""

import subprocess
import unicodedata
from typing import Dict, List, Optional, Tuple


class LegacyVoiceDetector:
    """
    Preserves v1.4.4 voice detection and categorization functionality
    """

    def __init__(self):
        self.voices_cache = None
        self.spanish_voices_cache = None

    def normalize_text(self, text: str) -> str:
        """Normaliza texto removiendo acentos para comparación

        Args:
            text: Texto a normalizar

        Returns:
            Texto sin acentos en minúsculas
        """
        # Normalizar a NFD (separa caracteres base de acentos)
        nfd = unicodedata.normalize("NFD", text)
        # Filtrar los acentos (categoría Mn = Nonspacing Mark)
        without_accents = "".join(c for c in nfd if unicodedata.category(c) != "Mn")
        return without_accents.lower()

    def get_system_voices(self) -> Dict[str, str]:
        """Obtiene todas las voces disponibles en el sistema (v1.4.4 logic)"""
        try:
            result = subprocess.run(
                ["say", "-v", "?"], capture_output=True, text=True, check=True
            )

            voces = {}
            for linea in result.stdout.split("\\n"):
                partes = linea.strip().split()
                if not partes:
                    continue

                nombre_voz = partes[0]
                resto = " ".join(partes[1:])

                # Crear alias sin acentos para búsqueda flexible
                nombre_normalizado = self.normalize_text(nombre_voz)
                desc_normalizada = self.normalize_text(resto)

                # Guardar con diferentes claves para búsqueda flexible
                voces[nombre_voz] = resto
                voces[nombre_normalizado] = resto

                # Agregar aliases comunes
                if "monica" in nombre_normalizado:
                    voces["monica"] = resto
                voces["jorge"] = resto
                voces["angelica"] = resto
                voces["francisca"] = resto
                voces["paulina"] = resto

                # Agregar alias para búsqueda sin acentos
                if "á" in nombre_voz:
                    voces[nombre_voz.replace("á", "a")] = resto
                if "é" in nombre_voz:
                    voces[nombre_voz.replace("é", "e")] = resto
                if "í" in nombre_voz:
                    voces[nombre_voz.replace("í", "i")] = resto
                if "ó" in nombre_voz:
                    voces[nombre_voz.replace("ó", "o")] = resto
                if "ú" in nombre_voz:
                    voces[nombre_voz.replace("ú", "u")] = resto

            return voces

        except subprocess.CalledProcessError as e:
            print(f"Error al obtener voces del sistema: {e}")
            return {}

    def obtener_voces_sistema(self, solo_espanol=False) -> Dict[str, str]:
        """Detecta automáticamente las voces disponibles en el sistema (v1.4.4 logic)

        Args:
            solo_espanol: Si es True, solo retorna voces en español
        """
        try:
            result = subprocess.run(
                ["say", "-v", "?"], capture_output=True, text=True, check=True
            )

            voces = {}
            for linea in result.stdout.split("\\n"):
                partes = linea.strip().split()
                if not partes:
                    continue

                nombre_voz = partes[0]
                linea_lower = linea.lower()

                # Filtrar por español si se solicita
                if solo_espanol and not any(
                    palabra in linea_lower
                    for palabra in ["spanish", "español", "spain", "mexico", "mexico"]
                ):
                    continue

                # Guardar voz normalizada y sin acentos
                voz_normalizada = self.normalize_text(nombre_voz)
                voces[nombre_voz] = " ".join(partes[1:])
                voces[voz_normalizada] = " ".join(partes[1:])

                # Agregar aliases específicos para español
                if any(palabra in linea_lower for palabra in ["monica", "españa"]):
                    voces["monica"] = " ".join(partes[1:])
                if any(palabra in linea_lower for palabra in ["jorge", "españa"]):
                    voces["jorge"] = " ".join(partes[1:])
                if any(palabra in linea_lower for palabra in ["angelica", "mexico"]):
                    voces["angelica"] = " ".join(partes[1:])
                if any(palabra in linea_lower for palabra in ["paulina", "mexico"]):
                    voces["paulina"] = " ".join(partes[1:])

            return voces

        except subprocess.CalledProcessError as e:
            print(f"Error detectando voces: {e}")
            return {}

    def buscar_voz(self, voz_solicitada: str, voces: Dict[str, str]) -> Optional[str]:
        """Busca una voz usando el algoritmo flexible de v1.4.4"""
        if not voz_solicitada or not voces:
            return None

        # Normalizar voz solicitada
        voz_normalizada = self.normalize_text(voz_solicitada)

        # Estrategia 1: Búsqueda exacta (case sensitive)
        if voz_solicitada in voces:
            return voz_solicitada

        # Estrategia 2: Búsqueda exacta (case insensitive)
        voz_upper = voz_solicitada.upper()
        for clave in voces:
            if clave.upper() == voz_upper:
                return clave

        # Estrategia 3: Búsqueda normalizada (sin acentos, minúsculas)
        if voz_normalizada in voces:
            return voz_normalizada

        # Estrategia 4: Búsqueda parcial
        for clave in voces:
            if voz_normalizada in clave or clave in voz_normalizada:
                return clave

        # Estrategia 5: Búsqueda por primera letra
        primera_letra = voz_normalizada[0] if voz_normalizada else ""
        for clave in voces:
            if clave and clave[0] == primera_letra:
                return clave

        return None

    def categorizar_voces(self) -> Dict[str, List[Dict[str, str]]]:
        """Categoriza voces usando la lógica de v1.4.4"""
        try:
            result = subprocess.run(
                ["say", "-v", "?"], capture_output=True, text=True, check=True
            )

            categorias = {
                "Español": [],
                "Enhanced": [],
                "Premium": [],
                "Siri": [],
                "Otras": [],
            }

            for linea in result.stdout.split("\\n"):
                if not linea.strip():
                    continue

                partes = linea.strip().split()
                if not partes:
                    continue

                nombre = partes[0]
                descripcion = " ".join(partes[1:])
                linea_lower = linea.lower()

                voice_info = {
                    "name": nombre,
                    "description": descripcion,
                    "language": self._extraer_idioma(descripcion),
                    "type": self._determinar_tipo(linea_lower),
                    "gender": self._extraer_genero(descripcion),
                }

                # Categorizar según la lógica v1.4.4
                if any(palabra in linea_lower for palabra in ["spanish", "español"]):
                    categorias["Español"].append(voice_info)
                elif "premium" in linea_lower:
                    categorias["Premium"].append(voice_info)
                elif "enhanced" in linea_lower:
                    categorias["Enhanced"].append(voice_info)
                elif "siri" in linea_lower:
                    categorias["Siri"].append(voice_info)
                else:
                    categorias["Otras"].append(voice_info)

            return categorias

        except subprocess.CalledProcessError:
            return {
                "Español": [],
                "Enhanced": [],
                "Premium": [],
                "Siri": [],
                "Otras": [],
            }

    def _extraer_idioma(self, descripcion: str) -> str:
        """Extrae el idioma de la descripción de la voz"""
        desc_lower = descripcion.lower()
        if "spanish" in desc_lower or "español" in desc_lower:
            if "mexico" in desc_lower:
                return "es-MX"
            elif "spain" in desc_lower:
                return "es-ES"
            return "es"
        elif "english" in desc_lower:
            return "en"
        return "unknown"

    def _determinar_tipo(self, linea_lower: str) -> str:
        """Determina el tipo de voz basado en la descripción"""
        if "premium" in linea_lower:
            return "Premium"
        elif "enhanced" in linea_lower:
            return "Enhanced"
        elif "siri" in linea_lower:
            return "Siri"
        return "Standard"

    def _extraer_genero(self, descripcion: str) -> str:
        """Extrae el género de la voz"""
        desc_lower = descripcion.lower()
        if any(palabra in desc_lower for palabra in ["female", "woman"]):
            return "Femenino"
        elif any(palabra in desc_lower for palabra in ["male", "man"]):
            return "Masculino"
        return "Desconocido"

    def get_voz_defecto(self, categoria: str = "Español") -> str:
        """Retorna una voz por defecto para la categoría especificada"""
        fallback_voices = {
            "Español": "Monica",
            "Enhanced": "Alex",
            "Premium": "Samantha",
            "Siri": "Siri",
            "Otras": "Alex",
        }

        return fallback_voices.get(categoria, "Monica")
