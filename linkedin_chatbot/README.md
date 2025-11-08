# 🚀 Generador de Posts de LinkedIn con OpenAI

Chatbot interactivo por terminal que genera posts profesionales de LinkedIn usando la API de OpenAI con **Structured Outputs** y **Pydantic** para garantizar respuestas estructuradas y validadas.

## ✨ Características

- ✅ **Structured Outputs**: Garantiza respuestas estructuradas usando `response_format` de OpenAI
- ✅ **Validación estricta**: Usa Pydantic para validar todos los campos del post
- ✅ **Interfaz interactiva**: Terminal amigable con comandos útiles
- ✅ **Manejo robusto de errores**: Gestión completa de excepciones y rechazos de la API
- ✅ **Generación inteligente**: Contenido profesional optimizado para LinkedIn
- ✅ **Hashtags automáticos**: Generación inteligente de hashtags relevantes
- ✅ **Categorización**: Clasificación automática del contenido

## 📋 Requisitos

- Python 3.9 o superior
- Cuenta de OpenAI con API key válida
- Créditos suficientes en tu cuenta de OpenAI

## 🔧 Instalación

### 1. Clonar o descargar el proyecto

```bash
cd linkedin_chatbot
```

### 2. Crear entorno virtual (recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar API key

Asegúrate de tener un archivo `.env` en el directorio raíz del proyecto con tu API key de OpenAI:

```
OPENAI_API_KEY=sk-tu-api-key-real-aqui
```

> 💡 **Obtén tu API key en**: https://platform.openai.com/api-keys
> 
> **Nota**: Si ya tienes tu archivo `.env` configurado, estás listo para usar el programa.

## 🚀 Uso

### Ejecutar el programa

```bash
python main.py
```

### Comandos disponibles

Durante la ejecución, puedes usar estos comandos:

- `ayuda` / `help` - Muestra la guía de uso
- `ejemplos` / `examples` - Muestra ejemplos de ideas para posts
- `salir` / `exit` / `quit` - Termina el programa

### Ejemplo de uso

```
💭 Describe tu idea para el post:
> Quiero crear un post sobre la importancia de la inteligencia artificial 
  en el desarrollo de software moderno

🤖 Generando post de LinkedIn...
⏳ Esto puede tomar unos segundos...

✨ ¡Post generado exitosamente! ✨

============================================================
📌 TÍTULO: La IA está transformando el desarrollo de software: 
          ¿Estás preparado?
============================================================

📝 CONTENIDO:
[Contenido generado automáticamente...]

============================================================
🏷️  HASHTAGS: #InteligenciaArtificial #DesarrolloSoftware #IA #Tech
📂 CATEGORÍA: Tecnología
============================================================
```

## 📁 Estructura del Proyecto

```
linkedin_chatbot/
├── main.py              # Punto de entrada principal
├── models/
│   ├── __init__.py
│   └── linkedin_post.py # Modelo Pydantic para posts
├── core/
│   ├── __init__.py
│   ├── api_client.py    # Cliente de OpenAI con Structured Outputs
│   └── chatbot.py       # Lógica principal del chatbot
├── requirements.txt     # Dependencias del proyecto
├── .env.example         # Plantilla para configuración
└── README.md           # Este archivo
```

## 🎯 Características Técnicas

### Modelo Pydantic

El modelo `LinkedinPost` incluye:

- **title**: Título del post (10-100 caracteres)
- **content**: Contenido principal (50-3000 caracteres)
- **hashtags**: Lista de 3-10 hashtags validados
- **category**: Categoría del post (validada contra lista permitida)

### Validaciones

- ✅ Longitudes mínimas y máximas
- ✅ Campos obligatorios
- ✅ Formato de hashtags
- ✅ Categorías válidas
- ✅ Contenido sin espacios vacíos
- ✅ Sin campos adicionales no definidos

### Manejo de Errores

El sistema gestiona:

- ❌ Errores de validación de Pydantic
- ❌ Rechazos (refusals) de la API
- ❌ Límites de tasa (rate limits)
- ❌ Cuota insuficiente
- ❌ API key inválida
- ❌ Errores de conexión
- ❌ Límites de tokens

## 🔍 Modelos Compatibles

El proyecto usa modelos compatibles con Structured Outputs:

- `gpt-4o-2024-08-06` (recomendado)
- `gpt-4o`
- `gpt-4o-mini`
- `gpt-4-turbo`

## 💡 Ejemplos de Ideas para Posts

### Tecnología
```
Las 5 tendencias en IA que cambiarán el desarrollo de software en 2025
```

### Desarrollo Profesional
```
Cómo superar el síndrome del impostor en tu carrera tech
```

### Liderazgo
```
Lecciones aprendidas después de liderar equipos remotos durante 3 años
```

### Marketing
```
Por qué el marketing de contenidos sigue siendo relevante en la era de la IA
```

## 🐛 Solución de Problemas

### Error: No se encontró la API key

**Solución**: Verifica que el archivo `.env` existe y contiene una API key válida:
```
OPENAI_API_KEY=sk-...
```

### Error: Cuota insuficiente

**Solución**: Verifica tu saldo en https://platform.openai.com/usage y recarga si es necesario.

### Error: Rate limit

**Solución**: Espera unos momentos antes de hacer otra solicitud. OpenAI tiene límites de tasa.

### Error: Modelo no compatible

**Solución**: Asegúrate de usar un modelo compatible con Structured Outputs. Edita el modelo en `main.py`.

## 📚 Documentación Adicional

- [OpenAI Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [OpenAI Python SDK](https://github.com/openai/openai-python)

## 🤝 Contribuciones

Este proyecto es educativo. Siéntete libre de mejorarlo y adaptarlo a tus necesidades.

## 📄 Licencia

Proyecto educativo para el Bootcamp de IA.

## 👨‍💻 Autor

Desarrollado como parte del Sprint 4 - Plataformas de IA Generativa para Desarrollo

---

**¡Disfruta generando contenido de calidad para LinkedIn! 🚀**
