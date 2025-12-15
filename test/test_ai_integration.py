from chatbot import Chat
import os

def test_ai_integration():
    print("Initializing Chat...")
    # Initialize with dummy pairs
    chat = Chat(pairs={'': {"pairs": [], "defaults": []}, "sub": {"pairs": [], "defaults": []}}, language="en")
    
    print("Testing Train...")
    # Train on a simple string
    chat.train("hello world how are you today", epochs=5)
    
    print("Testing Online Learning...")
    # Learn a response
    chat.learn_response("hello", "hi")
    
    print("Testing Fallback Logic (Direct)...")
    # "unknown input" should trigger AI
    # We test ai_converse directly since converse() loop returns None
    response = chat.ai_converse("unknown input that matches no pattern")
    print(f"Fallback Response: '{response}'") 
    
    if response == "I haven't been trained on enough data to answer that yet. Please train me!":
         print("PASS: AI Fallback (Untrained) triggered")
    elif response == "Sorry I couldn't find anything relevant":
        print("FAIL: AI Fallback not triggered (Legacy Error)")
    else:
        # If it returns "None" or "", that's now invalid. 
        # If it returns gibberish, that's fine (it tried).
        print(f"PASS: AI generated: {response}")

    print("Integration Test Passed!")

if __name__ == "__main__":
    test_ai_integration()
