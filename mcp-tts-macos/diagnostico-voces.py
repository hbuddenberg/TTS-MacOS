#!/usr/bin/env python3
"""
Script de diagnóstico para verificar voces disponibles en macOS
"""
import subprocess
import sys

def obtener_voces_disponibles():
    """Obtiene todas las voces disponibles en el sistema"""
    try:
        result = subprocess.run(
            ["say", "-v", "?"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError:
        print("❌ Error al obtener voces del sistema")
        return None
    except FileNotFoundError:
        print("❌ Comando 'say' no encontrado. ¿Estás en macOS?")
        return None

def filtrar_voces_espanol(voces_output):
    """Filtra solo voces en español"""
    if not voces_output:
        return []
    
    voces_espanol = []
    for linea in voces_output.split('\n'):
        if 'spanish' in linea.lower() or 'español' in linea.lower():
            # Extraer nombre de la voz (primera palabra)
            partes = linea.strip().split()
            if partes:
                nombre_voz = partes[0]
                voces_espanol.append((nombre_voz, linea.strip()))
    
    return voces_espanol

def probar_voz(nombre_voz, texto="Hola, esta es una prueba"):
    """Prueba una voz específica"""
    try:
        subprocess.run(
            ["say", "-v", nombre_voz, texto],
            check=True,
            capture_output=True
        )
        return True
    except:
        return False

def main():
    print("🔍 Diagnóstico de Voces TTS para macOS")
    print("=" * 60)
    print()
    
    # Obtener todas las voces
    print("📋 Obteniendo voces del sistema...")
    voces_output = obtener_voces_disponibles()
    
    if not voces_output:
        sys.exit(1)
    
    # Filtrar voces en español
    voces_espanol = filtrar_voces_espanol(voces_output)
    
    if not voces_espanol:
        print("\n⚠️  No se encontraron voces en español instaladas")
        print("\n💡 Para instalar voces:")
        print("   1. Abre Preferencias del Sistema")
        print("   2. Ve a Accesibilidad → Contenido Hablado")
        print("   3. Haz clic en 'Voces del Sistema'")
        print("   4. Descarga voces en español")
        sys.exit(1)
    
    print(f"\n✅ Se encontraron {len(voces_espanol)} voces en español:\n")
    print("-" * 60)
    
    # Mostrar voces disponibles
    for nombre, info_completa in voces_espanol:
        print(f"🎤 {nombre}")
        print(f"   {info_completa}")
        print()
    
    print("-" * 60)
    print()
    
    # Verificar voces esperadas
    voces_esperadas = {
        "Monica": "monica",
        "Paulina": "paulina",
        "Jorge": "jorge", 
        "Juan": "juan",
        "Diego": "diego",
        "Angelica": "angelica"
    }
    
    voces_disponibles_nombres = [nombre for nombre, _ in voces_espanol]
    
    print("🔍 Verificando voces esperadas por tts-macos:")
    print()
    
    voces_encontradas = {}
    voces_faltantes = []
    
    for voz_sistema, voz_cli in voces_esperadas.items():
        if voz_sistema in voces_disponibles_nombres:
            print(f"   ✅ {voz_sistema:12} → disponible (usar: --voice {voz_cli})")
            voces_encontradas[voz_cli] = voz_sistema
        else:
            print(f"   ❌ {voz_sistema:12} → NO instalada")
            voces_faltantes.append(voz_sistema)
    
    print()
    print("=" * 60)
    
    if voces_faltantes:
        print(f"\n⚠️  Faltan {len(voces_faltantes)} voces:")
        for voz in voces_faltantes:
            print(f"   • {voz}")
        print("\n💡 Para instalarlas:")
        print("   Preferencias → Accesibilidad → Contenido Hablado → Voces del Sistema")
    
    if voces_encontradas:
        print(f"\n✅ Voces disponibles: {', '.join(voces_encontradas.keys())}")
        print()
        
        # Probar voces
        print("🧪 ¿Quieres probar las voces disponibles? (s/n): ", end="")
        respuesta = input().strip().lower()
        
        if respuesta == 's':
            print()
            for voz_cli, voz_sistema in voces_encontradas.items():
                print(f"🎤 Probando {voz_sistema} ({voz_cli})...")
                texto = f"Hola, soy {voz_sistema}"
                if probar_voz(voz_sistema, texto):
                    print(f"   ✅ {voz_sistema} funciona correctamente")
                else:
                    print(f"   ❌ Error al probar {voz_sistema}")
                print()
    
    # Generar configuración corregida
    print()
    print("=" * 60)
    print("📝 Configuración sugerida para cli.py:")
    print("=" * 60)
    print()
    print("VOCES = {")
    for voz_cli, voz_sistema in voces_encontradas.items():
        print(f'    "{voz_cli}": "{voz_sistema}",')
    print("}")
    print()
    
    # Sugerir voces alternativas si hay otras disponibles
    voces_alternativas = [
        nombre for nombre in voces_disponibles_nombres 
        if nombre not in voces_esperadas.keys()
    ]
    
    if voces_alternativas:
        print("\n💡 Otras voces en español disponibles:")
        for voz in voces_alternativas:
            # Crear nombre de comando (en minúsculas)
            nombre_comando = voz.lower()
            print(f"   • {voz} (agregar como: \"{nombre_comando}\")")
        print()

if __name__ == "__main__":
    main()
