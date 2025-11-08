# 🚀 GUÍA DE INSTALACIÓN RÁPIDA

## Pasos para ejecutar el proyecto

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Configurar API key

Asegúrate de tener un archivo `.env` en el directorio del proyecto con tu API key:

```
OPENAI_API_KEY=sk-tu-api-key-aqui
```

**Nota**: Si ya tienes tu archivo `.env` configurado con las API keys necesarias, puedes omitir este paso.

### 3. Ejecutar el programa
```bash
python main.py
```

## 💡 Obtener tu API key

1. Ve a https://platform.openai.com/api-keys
2. Inicia sesión o crea una cuenta
3. Crea una nueva API key
4. Copia la key (empieza con sk-...)
5. Úsala en tu archivo .env

## ✅ Verificar instalación

Si todo está correcto, verás:
```
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║           🚀 GENERADOR DE POSTS DE LINKEDIN 🚀                   ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

## ❌ Problemas comunes

### "No module named 'openai'"
**Solución**: `pip install -r requirements.txt`

### "No se encontró la API key"
**Solución**: Verifica que el archivo .env existe y tiene el formato correcto

### "API key inválida"
**Solución**: Verifica que copiaste la API key completa sin espacios

## 📞 Necesitas ayuda?

Consulta el README.md completo para más información.
