"""
Backend wrapper for Practical 09 Local Farmer Chatbot
Zero external LLM API dependencies.
"""

import os
import sys

# Ensure practical directory is accessible
sys.path.append(os.path.abspath("Practical_09_NLP_App"))
try:
    from nlp_chatbot import LocalFarmerChatbot
except ImportError:
    from Practical_09_NLP_App.nlp_chatbot import LocalFarmerChatbot

# Global singleton instance
chatbot_instance = LocalFarmerChatbot()

def get_chatbot() -> LocalFarmerChatbot:
    return chatbot_instance
