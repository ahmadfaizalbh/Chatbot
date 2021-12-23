[![Downloads](https://pepy.tech/badge/chatbotai)](https://pepy.tech/project/chatbotai)
[![PyPI version](https://badge.fury.io/py/chatbotAI.svg)](https://badge.fury.io/py/chatbotAI)
![Upload Python Package](https://github.com/ahmadfaizalbh/Chatbot/workflows/Upload%20Python%20Package/badge.svg)
[![CodeQL](https://github.com/ahmadfaizalbh/Chatbot/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/ahmadfaizalbh/Chatbot/actions/workflows/codeql-analysis.yml)

# ChatBotAI
Python chatbot AI that helps in creating a python based chatbot with
minimal coding. This provides both bots AI and chat handler and also
allows easy integration of REST API's and python function calls which
makes it unique and more powerful in functionality. This AI provides
numerous features like learn, memory, conditional switch, topic-based
conversation handling, etc.


![Demo GUI](https://raw.githubusercontent.com/ahmadfaizalbh/Chatbot/master/images/demo_gui.gif)

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
```shell
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
from chatbot import Chat, register_call
import wikipedia


@register_call("whoIs")
def who_is(session, query):
    try:
        return wikipedia.summary(query)
    except Exception:
        for new_query in wikipedia.search(query):
            try:
                return wikipedia.summary(new_query)
            except Exception:
                pass
    return "I don't know about "+query

first_question="Hi, how are you?"
Chat("examples/Example.template").converse(first_question)
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

---

## Memory

#### Set Memory
```
{ variable : value }
```
In think mode
```
{! variable : value }
```

#### Get Memory
```
{ variable }
```

## Get matched group
for grouping in regex refer [Python regular expression docs](https://docs.python.org/3/howto/regex.html#non-capturing-and-named-groups)
#### Get N<sup>th</sup> matched group of client pattern
```
%N
```
Example to get first matched
```
%1
```
#### Get matching named group of client pattern
```
%Client_pattern_group_name
```
Example to get matching named group `person`
```
%person
```

#### Get N<sup>th</sup> matched group of bots message pattern
```
%!N
```
Example to get first matched
```
%!1
```

#### Get matching named group of bots message pattern
```
%!Bot_pattern_group_name
```
Example to get matching named group `region`
```
%!region
```

## Recursion
Get response as if client said this new statement
```
{% chat statement %}
```
It will do a pattern match for statement

## Condition
``` 
{% if condition %} do this first {% elif condition %} do this next {% else %} do otherwise {% endif %}
```

## Change Topic
```
{% topic TopicName %}
```

## Interact with python function
##### In python 
```python
@register_call("functionName")
def function_name(session, query):
    return "response string"
```
##### In template 
```
{% call functionName: value %}
```

## REST API integration
 
### In API.json file
 ```
{
    "APIName":{
        "auth" : {
            "url":"https://your_rest_api_url/login.json",
            "method":"POST",
            "data":{
                "user":"Your_Username",
                "password":"Your_Password"
            }
        },
        "MethodName" : {
            "url":"https://your_rest_api_url/GET_method_Example.json",
            "method":"GET",
            "params":{
                "key1":"value1",
                "key2":"value2",
                ...
            },
            "value_getter":[order in which data has to be picked from json response]
        },
        "MethodName1" : {
            "url":"https://your_rest_api_url/GET_method_Example.json",
            "method":"POST",
            "data":{
                "key1":"value1",
                "key2":"value2",
                ...
            },
            "value_getter":[order in which data has to be picked from json response]
        },
        "MethodName2" : {
            ...
        },
        ...
    },
    "APIName2":{
        ...
    },
    ...
}
```
*If authentication is required only then `auth` method is needed.The `data` and `params` defined in pi.json file acts as defult values and all key value pair defined in template file overrides the default value.`value_getter` consistes of list of keys in order using which info from json will be collected.*

### In Template file
```
[ APIName:MethodName,Key1:value1 (,Key*:value*) ]
```
you can have any number of key value pair and all key value pair will override data or params depending on `method`, if `method` is `POST` then it overrides data and if method is `GET` then it overrides `params`.

## Topic based group 
```
{% group topicName %}
  {% block %}
      {% client %}client says {% endclient %}
      {% response %}response text{% endresponse %}
  {% endblock %}
  ...
{% endgroup %}
```

## Learn
```
{% learn %}
  {% group topicName %}
    {% block %}
        {% client %}client says {% endclient %}
        {% response %}response text{% endresponse %}
    {% endblock %}
    ...
  {% endgroup %}
  ...
{% endlearn %}
```

## To upper case
```
{% up string %}
```

## To lower case
```
{% low string %}
```

## Capitalize
```
{% cap string %}
```

## Previous
```
{% block %}
    {% client %}client's statement pattern{% endclient %}
    {% prev %}previous bot's statement pattern{% endprev %}
    {% response %}response string{% endresponse %}
{% endblock %}
```


![Chatbot AI flow Diagram](https://raw.githubusercontent.com/ahmadfaizalbh/Chatbot/master/images/ChatBot%20AI.png)

