from chatbot import Chat, register_call
import os
import warnings
warnings.filterwarnings("ignore")


@register_call("increment_count")
def memory_get_set_example(session, query):
    name=query.strip().lower()
    # Get memory
    old_count = session.memory.get(name, '0')
    new_count = int(old_count) + 1
    # Set memory
    session.memory[name]=str(new_count)
    return f"count  {new_count}"


chat = Chat(os.path.join(os.path.dirname(os.path.abspath(__file__)), "get_set_memory_example.template"))
chat.converse("""
Memory get and set example

Usage:
increment <name>
show <name>

example:
increment mango
show mango
""")
