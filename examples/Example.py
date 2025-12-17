from chatbot import Chat, register_call
import os


@register_call("whoIs")
def who_is(session, query):
    # Simple knowledge base instead of wikipedia
    knowledge = {
        "python": "Python is a high-level programming language created by Guido van Rossum.",
        "ai": "Artificial Intelligence is the simulation of human intelligence in machines.",
        "chatbot": "A chatbot is a computer program designed to simulate conversation with human users."
    }
    
    query_lower = query.lower().strip()
    for key, value in knowledge.items():
        if key in query_lower:
            return value
    
    return f"I don't know about {query}"


first_question = "Hi, how are you?"
chat = Chat(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Example.template"))
chat.converse(first_question)
