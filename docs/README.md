# Chatbot
Python chatbot AI that helps in creating a python based chatbot with
minimal coding. This provides both bots AI and chat handler and also
allows easy integration of REST API's and python function calls which
makes it unique and more powerful in functionality. This AI provides
numerous features like learn, memory, conditional switch, topic-based
conversation handling, etc.


![Demo](https://raw.githubusercontent.com/ahmadfaizalbh/Chatbot/master/images/demo.gif)
![Clothing assistance](https://raw.githubusercontent.com/ahmadfaizalbh/Chatbot/master/images/clothing.gif)
![Remainder](https://raw.githubusercontent.com/ahmadfaizalbh/Chatbot/master/images/reminder.gif)

## Installation

Install from PyPI:
```sh
pip install chatbotAI
```

install from github:
```sh
git clone https://github.com/ahmadfaizalbh/Chatbot.git
cd Chatbot
python setup.py install
```

## Demo
```python
>>> from chatbot import demo
>>> demo()
Hi, how are you?
> i'm fine
Nice to know that you are fine  
> quit
Thank you for talking with me.
>>> 
```

## Sample Code (with wikipedia search API integration)

```python
from chatbot import Chat,MultiFunctionCall
import wikipedia

def who_is(query,session_id="general"):
    try:
        return wikipedia.summary(query)
    except:
        for new_query in wikipedia.search(query):
            try:
                return wikipedia.summary(new_query)
            except:
                pass
    return "I don't know about "+query
        
call = MultiFunctionCall({"whoIs":who_is})
first_question="Hi, how are you?"
Chat("examples/Example.template",call=call).converse(first_question)
```

For Detail on how to build Facebook messenger bot checkout  [Facebook Integration.ipynb](https://github.com/ahmadfaizalbh/Meetup-Resources/blob/master/Facebook%20Integration.ipynb)

For Jupyter notebook Chatbot checkout [Infobot built using NLTK-Chatbot](https://github.com/ahmadfaizalbh/Meetup-Resources/blob/master/How%20to%20build%20a%20bot.ipynb)

#### Sample Apps
1. A sample facebook messenger bot built using [messengerbot](https://github.com/geeknam/messengerbot/pulls), [Django](https://github.com/django/django) and [NLTK-Chatbot](#chatbot) is available here [Facebook messenger bot](https://github.com/ahmadfaizalbh/FacebookMessengerBot/)
2. A sample microsoft bot built using [Microsoft Bot Connector Rest API - v3.0](https://docs.botframework.com/en-us/restapi/connector/#navtitle), [Django](https://github.com/django/django) and [NLTK-Chatbot](#chatbot) is available here [Micosoft Chatbot](https://github.com/ahmadfaizalbh/Microsoft-chatbot/)

## List of feature supported in bot template
1. [Memory](#memory)
2. [Get matched group](#get-matched-group)
3. [Recursion](#recursion)
4. [Condition](#condition)
5. [Change Topic](#change-topic)
6. [Interact with python function](#interact-with-python-function)
7. [REST API integration](#rest-api-integration)
8. [Topic based group](#topic-based-group)
9. [Learn](#learn)
10. [To upper case](#to-upper-case)
11. [To lower case](#to-lower-case)
12. [Capitalize](#capitalize)
13. [Previous](#previous)


![Chatbot AI flow Diagram](https://raw.githubusercontent.com/ahmadfaizalbh/Chatbot/master/images/ChatBot%20AI.png)


