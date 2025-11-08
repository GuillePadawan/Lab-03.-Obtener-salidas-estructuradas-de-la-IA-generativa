"""
Clase principal del chatbot para generar posts de LinkedIn
"""
import sys
from typing import Optional
from core.api_client import OpenAIClient
from models.linkedin_post import LinkedinPost
from openai import OpenAIError


class LinkedinChatbot:
    """
    Chatbot interactivo por terminal para generar posts de LinkedIn
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-2024-08-06"):
        """
        Inicializa el chatbot
        
        Args:
            api_key: API key de OpenAI (opcional, se puede usar variable de entorno)
            model: Modelo de OpenAI a utilizar
        """
        self.api_client = None
        self.api_key = api_key
        self.model = model
        self.is_running = False
    
    def initialize(self) -> bool:
        """
        Inicializa el cliente de OpenAI y verifica la conexión
        
        Returns:
            bool: True si la inicialización fue exitosa
        """
        try:
            print("🔄 Inicializando cliente de OpenAI...")
            self.api_client = OpenAIClient(api_key=self.api_key, model=self.model)
            
            print("🔍 Verificando conexión con OpenAI...")
            self.api_client.test_connection()
            
            print("✅ Conexión establecida exitosamente")
            print(f"📱 Usando modelo: {self.model}\n")
            return True
            
        except ValueError as e:
            print(f"\n❌ Error de configuración: {e}")
            return False
        except Exception as e:
            print(f"\n❌ Error al inicializar: {e}")
            return False
    
    def show_welcome(self):
        """Muestra el mensaje de bienvenida"""
        welcome_text = """
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║           🚀 GENERADOR DE POSTS DE LINKEDIN 🚀                   ║
║                                                                  ║
║  Powered by OpenAI Structured Outputs + Pydantic                ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝

¡Bienvenido! Este chatbot te ayudará a crear posts profesionales 
para LinkedIn de forma rápida y sencilla.

📝 Características:
   • Contenido profesional y optimizado para engagement
   • Validación estricta de formato y estructura
   • Hashtags relevantes generados automáticamente
   • Categorización inteligente del contenido

💡 Instrucciones:
   • Describe la idea o tema del post que quieres crear
   • Sé lo más específico posible para mejores resultados
   • Escribe 'salir' o 'exit' para terminar el programa
   • Escribe 'ayuda' o 'help' para ver esta información de nuevo

"""
        print(welcome_text)
    
    def show_help(self):
        """Muestra el mensaje de ayuda"""
        help_text = """
═══════════════════════════════════════════════════════════════

📚 GUÍA DE USO

Comandos disponibles:
  • salir / exit / quit    → Termina el programa
  • ayuda / help           → Muestra esta ayuda
  • ejemplos               → Muestra ejemplos de ideas para posts

Cómo usar el generador:
  1. Describe tu idea de forma clara y concisa
  2. Puedes mencionar el público objetivo
  3. Indica el tono que prefieres (inspirador, educativo, etc.)
  4. El sistema generará automáticamente un post completo

Ejemplo de entrada:
  "Quiero crear un post sobre la importancia de la inteligencia 
   artificial en el desarrollo de software moderno, dirigido a 
   programadores que están empezando"

═══════════════════════════════════════════════════════════════
"""
        print(help_text)
    
    def show_examples(self):
        """Muestra ejemplos de ideas para posts"""
        examples_text = """
═══════════════════════════════════════════════════════════════

💡 EJEMPLOS DE IDEAS PARA POSTS

1. Tecnología:
   "Las 5 tendencias en IA que cambiarán el desarrollo de software en 2025"
   
2. Desarrollo Profesional:
   "Cómo superar el síndrome del impostor en tu carrera tech"
   
3. Liderazgo:
   "Lecciones aprendidas después de liderar equipos remotos durante 3 años"
   
4. Marketing:
   "Por qué el marketing de contenidos sigue siendo relevante en la era de la IA"
   
5. Innovación:
   "Cómo implementamos una cultura de innovación en nuestra startup"

═══════════════════════════════════════════════════════════════
"""
        print(examples_text)
    
    def get_user_input(self) -> Optional[str]:
        """
        Solicita y procesa la entrada del usuario
        
        Returns:
            str: Entrada del usuario procesada, o None si quiere salir
        """
        try:
            print("\n" + "─" * 70)
            user_input = input("\n💭 Describe tu idea para el post:\n> ").strip()
            
            if not user_input:
                print("⚠️  No puedes dejar la entrada vacía. Intenta de nuevo.")
                return ""
            
            # Comandos especiales
            if user_input.lower() in ['salir', 'exit', 'quit']:
                return None
            
            if user_input.lower() in ['ayuda', 'help']:
                self.show_help()
                return ""
            
            if user_input.lower() in ['ejemplos', 'examples']:
                self.show_examples()
                return ""
            
            return user_input
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrupción detectada. Saliendo...")
            return None
        except EOFError:
            return None
    
    def generate_and_display_post(self, user_idea: str) -> bool:
        """
        Genera y muestra un post de LinkedIn basado en la idea del usuario
        
        Args:
            user_idea: Idea proporcionada por el usuario
        
        Returns:
            bool: True si la generación fue exitosa
        """
        try:
            print("\n🤖 Generando post de LinkedIn...")
            print("⏳ Esto puede tomar unos segundos...\n")
            
            # Generar el post usando la API
            post = self.api_client.generate_linkedin_post(user_idea)
            
            # Mostrar el resultado
            print("\n✨ ¡Post generado exitosamente! ✨")
            print(post.format_for_display())
            
            # Preguntar si quiere guardar el post
            self.offer_save_option(post)
            
            return True
            
        except ValueError as e:
            print(f"\n❌ Error de validación: {e}")
            print("\n💡 Sugerencias:")
            print("   • Intenta ser más específico en tu idea")
            print("   • Asegúrate de que el tema sea apropiado")
            print("   • Revisa que tu descripción tenga suficiente detalle")
            return False
            
        except OpenAIError as e:
            print(f"\n❌ Error de la API de OpenAI: {e}")
            print("\n💡 Posibles soluciones:")
            print("   • Verifica tu conexión a internet")
            print("   • Comprueba que tu API key sea válida")
            print("   • Revisa tu cuota en platform.openai.com")
            return False
            
        except Exception as e:
            print(f"\n❌ Error inesperado: {e}")
            print("\n💡 Por favor, intenta de nuevo o contacta al soporte")
            return False
    
    def offer_save_option(self, post: LinkedinPost):
        """
        Ofrece la opción de guardar el post en un archivo
        
        Args:
            post: Post de LinkedIn generado
        """
        try:
            save_input = input("\n💾 ¿Deseas guardar este post en un archivo? (s/n): ").strip().lower()
            
            if save_input in ['s', 'si', 'sí', 'y', 'yes']:
                filename = input("📁 Nombre del archivo (sin extensión): ").strip()
                if not filename:
                    filename = "linkedin_post"
                
                filename = f"{filename}.txt"
                
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(post.format_for_display())
                
                print(f"✅ Post guardado exitosamente en: {filename}")
        
        except Exception as e:
            print(f"⚠️  No se pudo guardar el archivo: {e}")
    
    def run(self):
        """
        Ejecuta el bucle principal del chatbot
        """
        # Mostrar bienvenida
        self.show_welcome()
        
        # Inicializar cliente de OpenAI
        if not self.initialize():
            print("\n❌ No se pudo inicializar el chatbot. Verifica tu configuración.")
            print("💡 Asegúrate de tener configurada la variable de entorno OPENAI_API_KEY")
            return
        
        print("🎯 ¡Listo para generar posts! Escribe tu primera idea.\n")
        
        # Bucle principal
        self.is_running = True
        while self.is_running:
            try:
                # Obtener entrada del usuario
                user_input = self.get_user_input()
                
                # Verificar si quiere salir
                if user_input is None:
                    self.is_running = False
                    break
                
                # Saltar si la entrada está vacía (comando de ayuda/ejemplos)
                if not user_input:
                    continue
                
                # Generar y mostrar el post
                self.generate_and_display_post(user_input)
                
            except KeyboardInterrupt:
                print("\n\n⚠️  Interrupción detectada.")
                self.is_running = False
                break
            
            except Exception as e:
                print(f"\n❌ Error inesperado en el bucle principal: {e}")
                print("💡 El programa continuará ejecutándose...\n")
        
        # Mensaje de despedida
        self.show_goodbye()
    
    def show_goodbye(self):
        """Muestra el mensaje de despedida"""
        goodbye_text = """
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║                    👋 ¡Hasta pronto!                             ║
║                                                                  ║
║  Gracias por usar el Generador de Posts de LinkedIn             ║
║                                                                  ║
║  💡 Comparte contenido de calidad en LinkedIn                    ║
║  🚀 Sigue creciendo profesionalmente                             ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
"""
        print(goodbye_text)
