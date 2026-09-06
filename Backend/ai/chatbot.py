"""
Backend wrapper for Practical 09 Local Farmer Chatbot
Zero external LLM API dependencies.
"""

import os
import sys

# Ensure local ai directory is in sys.path
_AI_DIR = os.path.dirname(os.path.abspath(__file__))
if _AI_DIR not in sys.path:
    sys.path.insert(0, _AI_DIR)

try:
    from nlp_chatbot import LocalFarmerChatbot
except ImportError:
    from Backend.ai.nlp_chatbot import LocalFarmerChatbot

# Global singleton instance
chatbot_instance = LocalFarmerChatbot()

def get_chatbot() -> LocalFarmerChatbot:
    return chatbot_instance
