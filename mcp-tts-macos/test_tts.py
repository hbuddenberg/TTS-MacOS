#!/usr/bin/env python3
"""
Script de prueba para verificar que el TTS de macOS funciona correctamente
"""
import subprocess
import sys

def test_voice(voice_name, text):
    """Prueba una voz específica"""
    print(f"\n🎤 Probando voz: {voice_name}")
    print(f"📝 Texto: {text}")
    try:
        subprocess.run(
            ["say", "-v", voice_name, text],
            check=True,
            capture_output=True
        )
        print(f"✅ {voice_name} funciona correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error con {voice_name}: {e}")
        return False
    except FileNotFoundError:
        print("❌ El comando 'say' no está disponible. ¿Estás en macOS?")
        return False

def main():
    print("=" * 60)
    print("🧪 TEST DE VOCES TTS PARA MACOS")
    print("=" * 60)
    
    # Verificar sistema
    import platform
    if platform.system() != "Darwin":
        print("\n❌ Este script solo funciona en macOS")
        sys.exit(1)
    
    print(f"\n✅ Sistema: macOS {platform.mac_ver()[0]}")
    
    # Voces a probar
    voces = {
        "Monica": "Hola, soy Mónica, voz de México",
        "Paulina": "Hola, soy Paulina, voz de México",
        "Jorge": "Hola, soy Jorge, voz de España",
        "Juan": "Hola, soy Juan, voz de España",
    }
    
    print(f"\n📋 Se probarán {len(voces)} voces en español")
    print("-" * 60)
    
    resultados = {}
    for voz, texto in voces.items():
        resultados[voz] = test_voice(voz, texto)
    
    # Resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 60)
    
    exitosas = sum(1 for v in resultados.values() if v)
    total = len(resultados)
    
    for voz, exitosa in resultados.items():
        estado = "✅" if exitosa else "❌"
        print(f"{estado} {voz}")
    
    print(f"\n📈 Resultado: {exitosas}/{total} voces funcionando correctamente")
    
    if exitosas == total:
        print("\n🎉 ¡Todas las voces funcionan perfectamente!")
        print("💡 Tip: Puedes usar cualquiera de estas voces en el servidor MCP")
    elif exitosas > 0:
        print("\n⚠️  Algunas voces no están disponibles")
        print("💡 Puedes instalar más voces en:")
        print("   Preferencias del Sistema → Accesibilidad → Contenido Hablado")
    else:
        print("\n❌ No se encontraron voces en español")
        print("📥 Instala voces en español desde:")
        print("   Preferencias del Sistema → Accesibilidad → Contenido Hablado")
    
    print("\n" + "=" * 60)
    
    # Prueba de velocidad
    print("\n🏃 Probando velocidades diferentes...")
    print("Velocidad normal (175 wpm):")
    subprocess.run(["say", "-v", "Monica", "-r", "175", "Esta es velocidad normal"])
    
    print("Velocidad rápida (250 wpm):")
    subprocess.run(["say", "-v", "Monica", "-r", "250", "Esta es velocidad rápida"])
    
    print("Velocidad lenta (125 wpm):")
    subprocess.run(["say", "-v", "Monica", "-r", "125", "Esta es velocidad lenta"])
    
    print("\n✅ Test completado!")

if __name__ == "__main__":
    main()
