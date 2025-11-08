"""
Punto de entrada principal del Generador de Posts de LinkedIn
"""
import sys
import os
from dotenv import load_dotenv

# Agregar el directorio actual al path para imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.chatbot import LinkedinChatbot


def main():
    """
    Función principal que inicializa y ejecuta el chatbot
    """
    # Cargar variables de entorno desde archivo .env
    load_dotenv()
    
    # Verificar que existe la API key
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("\n" + "="*70)
        print("❌ ERROR: No se encontró la API key de OpenAI")
        print("="*70)
        print("\n📋 Para usar este programa necesitas configurar tu API key:\n")
        print("1️⃣  Crea un archivo llamado '.env' en este directorio")
        print("2️⃣  Agrega la siguiente línea al archivo:")
        print("    OPENAI_API_KEY=tu_api_key_aqui")
        print("\n💡 Puedes obtener tu API key en: https://platform.openai.com/api-keys")
        print("\n" + "="*70 + "\n")
        sys.exit(1)
    
    try:
        # Crear instancia del chatbot
        # Puedes cambiar el modelo aquí si lo deseas
        chatbot = LinkedinChatbot(
            api_key=api_key,
            model="gpt-4o-2024-08-06"  # Modelo compatible con Structured Outputs
        )
        
        # Ejecutar el chatbot
        chatbot.run()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Programa interrumpido por el usuario.")
        sys.exit(0)
    
    except Exception as e:
        print(f"\n❌ Error crítico: {e}")
        print("💡 Si el problema persiste, contacta al soporte.")
        sys.exit(1)


if __name__ == "__main__":
    main()
