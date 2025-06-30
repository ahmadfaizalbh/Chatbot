#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Enhanced Chatbot using Wikipedia and Template-based NLP
#
# 
# Enhanced by: Muhannad - github.com/muhannad-iz-a-tech-nerd
#
# Features:
# - Handles "who is" questions via Wikipedia.
# - Uses template-based conversation.
# - Improved error handling and logging.
# - Simple CLI interface.

import os
import warnings
import wikipedia
from chatbot import Chat, register_call

# Suppress unnecessary warnings
warnings.filterwarnings("ignore")

# Optional but setting the language to English.
wikipedia.set_lang("en")

@register_call("whoIs")
def who_is(session, query):
    """Fetches a Wikipedia summary for a given query."""
    try:
        return wikipedia.summary(query)
    except Exception as e:
        # Fallback: search for similar topics
        for new_query in wikipedia.search(query):
            try:
                return wikipedia.summary(new_query)
            except Exception:
                continue
        return f"Sorry, I couldn't find anything about '{query}'."

def main():
    # Initial question for the chatbot as a beginning 
    first_question = "Hi, how are you?"

    
    template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Example.template")

    if not os.path.exists(template_path):
        print(f"Error: Template file not found at {template_path}")
        return

    
    chat = Chat(template_path)
    chat.converse(first_question)

if __name__ == "__main__":
    main()
