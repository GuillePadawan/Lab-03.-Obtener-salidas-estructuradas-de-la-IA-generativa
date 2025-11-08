"""
Cliente para interactuar con la API de OpenAI usando Structured Outputs
"""
import os
from typing import Optional
from openai import OpenAI, OpenAIError
from pydantic import ValidationError
from models.linkedin_post import LinkedinPost


class OpenAIClient:
    """
    Cliente para generar posts de LinkedIn usando OpenAI con Structured Outputs
    """
    
    # Modelos compatibles con Structured Outputs
    COMPATIBLE_MODELS = [
        "gpt-4o-2024-08-06",
        "gpt-4o",
        "gpt-4o-mini",
        "gpt-4-turbo"
    ]
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-2024-08-06"):
        """
        Inicializa el cliente de OpenAI
        
        Args:
            api_key: API key de OpenAI. Si no se proporciona, se busca en variable de entorno
            model: Modelo a utilizar (debe ser compatible con Structured Outputs)
        
        Raises:
            ValueError: Si no se proporciona API key o el modelo no es compatible
        """
        # Obtener API key
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        
        if not self.api_key:
            raise ValueError(
                "No se encontró la API key de OpenAI. "
                "Proporciona api_key como parámetro o configura la variable de entorno OPENAI_API_KEY"
            )
        
        # Validar modelo
        if model not in self.COMPATIBLE_MODELS:
            print(f"⚠️  Advertencia: El modelo '{model}' puede no ser compatible con Structured Outputs.")
            print(f"   Modelos recomendados: {', '.join(self.COMPATIBLE_MODELS)}")
        
        self.model = model
        
        # Inicializar cliente de OpenAI
        try:
            self.client = OpenAI(api_key=self.api_key)
        except Exception as e:
            raise ValueError(f"Error inicializando cliente de OpenAI: {str(e)}")
        
        # Prompt del sistema optimizado para LinkedIn
        self.system_prompt = """Eres un experto en crear contenido profesional para LinkedIn.
        
Tu tarea es generar posts atractivos, profesionales y de alta calidad que generen engagement.

Directrices para crear el contenido:
1. TÍTULO: Debe ser llamativo, conciso y captar la atención (máximo 100 caracteres)
2. CONTENIDO: 
   - Escribe entre 200-500 palabras
   - Usa un tono profesional pero cercano
   - Incluye valor real para el lector
   - Estructura el texto con párrafos cortos y fáciles de leer
   - Usa emojis estratégicamente para mejorar la legibilidad (máximo 3-5)
   - Incluye una llamada a la acción al final
3. HASHTAGS:
   - Proporciona entre 3 y 10 hashtags relevantes
   - Mezcla hashtags populares y específicos
   - No incluyas el símbolo # (se agregará automáticamente)
4. CATEGORÍA:
   - Elige la categoría más apropiada: tecnología, negocios, marketing, liderazgo, 
     desarrollo profesional, industria, innovación, recursos humanos

Adapta el tono y contenido según la idea proporcionada por el usuario."""
    
    def generate_linkedin_post(self, user_idea: str) -> LinkedinPost:
        """
        Genera un post de LinkedIn estructurado usando Structured Outputs
        
        Args:
            user_idea: Idea o tema del post proporcionado por el usuario
        
        Returns:
            LinkedinPost: Objeto validado con el post generado
        
        Raises:
            ValueError: Si hay error en la validación o generación del contenido
            OpenAIError: Si hay error en la comunicación con la API
        """
        if not user_idea or not user_idea.strip():
            raise ValueError("Debes proporcionar una idea para el post")
        
        try:
            # Crear el mensaje del usuario
            user_message = f"""Genera un post profesional de LinkedIn sobre el siguiente tema:

"{user_idea.strip()}"

Asegúrate de crear contenido valioso, relevante y que genere engagement."""
            
            # Llamada a la API usando chat.completions.parse con response_format
            response = self.client.chat.completions.parse(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_message}
                ],
                response_format=LinkedinPost,  # Structured Output con Pydantic
                temperature=0.7,  # Balance entre creatividad y coherencia
                max_tokens=2000
            )
            
            # Verificar si hay refusal (rechazo del modelo)
            if response.choices[0].message.refusal:
                refusal_message = response.choices[0].message.refusal
                raise ValueError(
                    f"La API rechazó generar el contenido: {refusal_message}\n"
                    "Esto puede deberse a que el tema viola las políticas de uso de OpenAI."
                )
            
            # Obtener el objeto parseado automáticamente
            linkedin_post = response.choices[0].message.parsed
            
            if not linkedin_post:
                raise ValueError(
                    "La API no devolvió un post válido. "
                    "Esto puede ocurrir si el modelo no pudo generar contenido estructurado."
                )
            
            return linkedin_post
        
        except ValidationError as e:
            # Error de validación de Pydantic
            error_messages = []
            for error in e.errors():
                field = ' -> '.join(str(loc) for loc in error['loc'])
                message = error['msg']
                error_messages.append(f"  - {field}: {message}")
            
            raise ValueError(
                "Error en la validación del post generado:\n" + 
                '\n'.join(error_messages) +
                "\n\nPor favor, intenta con una idea diferente o más específica."
            )
        
        except OpenAIError as e:
            # Errores específicos de la API de OpenAI
            error_msg = str(e)
            
            if "rate_limit" in error_msg.lower():
                raise OpenAIError(
                    "Se alcanzó el límite de tasa de la API. "
                    "Por favor, espera unos momentos antes de intentar de nuevo."
                )
            elif "insufficient_quota" in error_msg.lower():
                raise OpenAIError(
                    "Cuota insuficiente en tu cuenta de OpenAI. "
                    "Verifica tu saldo en https://platform.openai.com/usage"
                )
            elif "invalid_api_key" in error_msg.lower():
                raise OpenAIError(
                    "API key inválida. Verifica que tu OPENAI_API_KEY sea correcta."
                )
            else:
                raise OpenAIError(f"Error de la API de OpenAI: {error_msg}")
        
        except Exception as e:
            # Cualquier otro error inesperado
            raise ValueError(
                f"Error inesperado al generar el post: {str(e)}\n"
                "Por favor, intenta de nuevo o contacta al soporte."
            )
    
    def test_connection(self) -> bool:
        """
        Verifica que la conexión con OpenAI funcione correctamente
        
        Returns:
            bool: True si la conexión es exitosa
        
        Raises:
            Exception: Si hay algún problema con la conexión
        """
        try:
            # Hacer una llamada simple para verificar la conexión
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "test"}],
                max_tokens=5
            )
            return True
        except Exception as e:
            raise Exception(f"Error al probar la conexión con OpenAI: {str(e)}")
