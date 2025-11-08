"""
Módulo core con la lógica principal del chatbot
"""
from .chatbot import LinkedinChatbot
from .api_client import OpenAIClient

__all__ = ['LinkedinChatbot', 'OpenAIClient']
