from chatbot import Chat, MultiFunctionCall
import wikipedia
import os
import warnings
warnings.filterwarnings("ignore")


def who_is(query, session_id="general"):
    try:
        return wikipedia.summary(query)
    except Exception:
        for new_query in wikipedia.search(query):
            try:
                return wikipedia.summary(new_query)
            except Exception:
                pass
    return "I don't know about "+query


call = MultiFunctionCall({"whoIs": who_is})
first_question = "Hi, how are you?"
chat = Chat(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Example.template"), call=call)
chat.converse(first_question)
