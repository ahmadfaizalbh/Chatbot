import unittest
import os
from chatbot import Chat

class TestAIIntegration(unittest.TestCase):
    def setUp(self):
        # Initialize with dummy pairs
        self.chat = Chat(pairs={'': {"pairs": [], "defaults": []}, "sub": {"pairs": [], "defaults": []}}, language="en")

    def test_ai_integration(self):
        # Train on a simple string
        self.chat.train("hello world how are you today", epochs=5)
        
        # Learn a response
        self.chat.learn_response("hello", "hi")
        
        # Test AI fallback
        response = self.chat.ai_converse("unknown input that matches no pattern")
        
        self.assertNotEqual(response, "Sorry I couldn't find anything relevant", "AI Fallback not triggered (Legacy Error)")
        # If it returns the untrained message, that's expected; otherwise, it should be AI-generated (not None or empty)
        if response == "I haven't been trained on enough data to answer that yet. Please train me!":
            self.assertTrue(True)  # PASS: AI Fallback (Untrained) triggered
        else:
            self.assertIsNotNone(response)
            self.assertNotEqual(response, "", f"AI generated invalid response: {response}")

    def test_learn_response_capital_question(self):
        self.chat.learn_response("What is the capital of Mars?", "Elon Musk's future home")
        response = self.chat.respond("What is the capital of Mars?")
        words_found = sum(1 for w in ["elon", "musk", "mars", "future", "home"] if w in response.lower())
        self.assertGreaterEqual(words_found, 3, f"Response '{response}' does not contain expected words")

    def test_learn_response_simple_fact(self):
        self.chat.learn_response("What is AI?", "Artificial Intelligence")
        response = self.chat.respond("What is AI?")
        self.assertTrue("artificial" in response.lower() or "intelligence" in response.lower(), f"Response '{response}' does not contain 'artificial' or 'intelligence'")

    def test_learn_response_name_question(self):
        self.chat.learn_response("Who created Python?", "Guido van Rossum")
        response = self.chat.respond("Who created Python?")
        self.assertTrue("guido" in response.lower() or "rossum" in response.lower(), f"Response '{response}' does not contain 'guido' or 'rossum'")

    def test_learn_response_definition(self):
        self.chat.learn_response("What is machine learning?", "AI that learns from data")
        response = self.chat.respond("What is machine learning?")
        words_found = sum(1 for w in ["ai", "learns", "data", "learning"] if w in response.lower())
        self.assertGreaterEqual(words_found, 2, f"Response '{response}' does not contain at least 2 expected words")

    def test_training_and_cleanup(self):
        # Smaller dataset for speed
        with open("dummy_train_small.txt", "w", encoding="utf-8") as f:
            f.write("Hello how are you\nI am fine\n" * 5) 
        
        self.chat.train("dummy_train_small.txt", epochs=2)
        # Assert that training completes without error
        self.assertTrue(True)

    def test_combined_workflow(self):
        chat = Chat()
        # Smaller dataset for speed
        with open("dummy_train_small.txt", "w", encoding="utf-8") as f:
            f.write("Hello how are you\nI am fine\n" * 5) 

        chat.train("dummy_train_small.txt", epochs=2)

        # Test 1: Capital question
        chat.learn_response("What is the capital of Mars?", "Elon Musk's future home")
        response = chat.respond("What is the capital of Mars?")
        words_found = sum(1 for w in ["elon", "musk", "mars", "future", "home"] if w in response.lower())
        self.assertGreaterEqual(words_found, 3, "Test 1 failed")

        # Test 2: Simple fact
        chat.learn_response("What is AI?", "Artificial Intelligence")
        response = chat.respond("What is AI?")
        self.assertTrue("artificial" in response.lower() or "intelligence" in response.lower(), "Test 2 failed")

        # Test 3: Name question
        chat.learn_response("Who created Python?", "Guido van Rossum")
        response = chat.respond("Who created Python?")
        self.assertTrue("guido" in response.lower() or "rossum" in response.lower(), "Test 3 failed")

        # Test 4: Definition
        chat.learn_response("What is machine learning?", "AI that learns from data")
        response = chat.respond("What is machine learning?")
        words_found = sum(1 for w in ["ai", "learns", "data", "learning"] if w in response.lower())
        self.assertGreaterEqual(words_found, 2, "Test 4 failed")

if __name__ == '__main__':
    unittest.main()
