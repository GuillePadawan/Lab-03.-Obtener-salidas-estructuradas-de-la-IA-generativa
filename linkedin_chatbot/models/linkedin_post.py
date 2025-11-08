"""
Modelo Pydantic para posts de LinkedIn con validación estricta
"""
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import List


class LinkedinPost(BaseModel):
    """
    Modelo que representa un post de LinkedIn estructurado.
    
    Campos obligatorios:
    - title: Título del post (máximo 100 caracteres)
    - content: Contenido principal del post (máximo 3000 caracteres)
    - hashtags: Lista de hashtags (mínimo 3, máximo 10)
    - category: Categoría del post (debe ser una de las categorías válidas)
    """
    
    # Configuración estricta del modelo
    model_config = ConfigDict(
        str_strip_whitespace=True,  # Elimina espacios en blanco al inicio y final
        extra='forbid'  # No permite campos adicionales no definidos
    )
    
    title: str = Field(
        ...,  # Campo obligatorio
        min_length=10,
        max_length=100,
        description="Título llamativo y descriptivo para el post de LinkedIn"
    )
    
    content: str = Field(
        ...,  # Campo obligatorio
        min_length=50,
        max_length=3000,
        description="Contenido principal del post con información valiosa y profesional"
    )
    
    hashtags: List[str] = Field(
        ...,  # Campo obligatorio
        min_length=3,
        max_length=10,
        description="Lista de hashtags relevantes para el post (entre 3 y 10)"
    )
    
    category: str = Field(
        ...,  # Campo obligatorio
        description="Categoría del post: tecnología, negocios, marketing, liderazgo, desarrollo profesional, industria, innovación, recursos humanos"
    )
    
    @field_validator('title')
    @classmethod
    def validate_title(cls, v: str) -> str:
        """Valida que el título no esté vacío después de limpiar espacios"""
        if not v or not v.strip():
            raise ValueError("El título no puede estar vacío")
        return v.strip()
    
    @field_validator('content')
    @classmethod
    def validate_content(cls, v: str) -> str:
        """Valida que el contenido sea sustancial"""
        cleaned = v.strip()
        if not cleaned:
            raise ValueError("El contenido no puede estar vacío")
        
        # Verificar que tenga contenido real (no solo espacios o saltos de línea)
        if len(cleaned.replace('\n', '').replace('\r', '').strip()) < 50:
            raise ValueError("El contenido debe tener al menos 50 caracteres de texto real")
        
        return cleaned
    
    @field_validator('hashtags')
    @classmethod
    def validate_hashtags(cls, v: List[str]) -> List[str]:
        """Valida que los hashtags sean válidos"""
        if not v:
            raise ValueError("Debe proporcionar al menos 3 hashtags")
        
        # Limpiar y validar cada hashtag
        cleaned_hashtags = []
        for tag in v:
            # Eliminar espacios y el símbolo # si está presente
            cleaned_tag = tag.strip().lstrip('#')
            
            if not cleaned_tag:
                raise ValueError("Los hashtags no pueden estar vacíos")
            
            if ' ' in cleaned_tag:
                raise ValueError(f"Los hashtags no pueden contener espacios: '{cleaned_tag}'")
            
            if len(cleaned_tag) < 2:
                raise ValueError(f"Los hashtags deben tener al menos 2 caracteres: '{cleaned_tag}'")
            
            # Agregar el hashtag sin el símbolo # (se agregará al mostrar)
            cleaned_hashtags.append(cleaned_tag)
        
        # Verificar duplicados (case insensitive)
        lowercase_tags = [tag.lower() for tag in cleaned_hashtags]
        if len(lowercase_tags) != len(set(lowercase_tags)):
            raise ValueError("No puede haber hashtags duplicados")
        
        return cleaned_hashtags
    
    @field_validator('category')
    @classmethod
    def validate_category(cls, v: str) -> str:
        """Valida que la categoría sea una de las permitidas"""
        valid_categories = {
            'tecnología', 'tecnologia',
            'negocios',
            'marketing',
            'liderazgo',
            'desarrollo profesional', 'desarrollo_profesional',
            'industria',
            'innovación', 'innovacion',
            'recursos humanos', 'recursos_humanos', 'rrhh'
        }
        
        category_lower = v.lower().strip()
        
        # Normalizar categorías con espacios o guiones bajos
        category_normalized = category_lower.replace('_', ' ')
        
        if category_normalized not in valid_categories:
            raise ValueError(
                f"Categoría inválida: '{v}'. Debe ser una de: "
                "tecnología, negocios, marketing, liderazgo, desarrollo profesional, "
                "industria, innovación, recursos humanos"
            )
        
        # Devolver en formato normalizado con mayúscula inicial
        return category_normalized.title()
    
    def format_for_display(self) -> str:
        """
        Formatea el post para mostrar en terminal de forma legible
        """
        hashtags_formatted = ' '.join([f'#{tag}' for tag in self.hashtags])
        
        output = f"""
{'='*60}
📌 TÍTULO: {self.title}
{'='*60}

📝 CONTENIDO:
{self.content}

{'='*60}
🏷️  HASHTAGS: {hashtags_formatted}
📂 CATEGORÍA: {self.category}
{'='*60}
"""
        return output
