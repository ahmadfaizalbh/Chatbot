# Chatbot
Python chatbot

```python
from chatbot import Chat,reflections,multiFunctionCall
import wikipedia

def whoIs(query,sessionID="general"):
    try:
        return wikipedia.summary(query)
    except:
        for newquery in wikipedia.search(query):
            try:
                return wikipedia.summary(newquery)
            except:
                pass
    return "I don't know about "+query
        
call = multiFunctionCall({"whoIs":whoIs})
firstQuestion="Hi, how are you?"
Chat("examples/Example.template", reflections,call=call).converse(firstQuestion)
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
7. [Execute shell script](#execute-shell-script)
8. [Topic based group](#topic-based-group)
9. [Learn](#learn)
10. [To upper case](#to-upper-case)
11. [To lower case](#to-lower-case)
12. [Capitalize](#capitalize)
13. [Previous](#previous)

---

## Memory
#### Set Memory
> ```
{ variable : value }
```
In think mode
```
{! variable : value }
```

#### Get Memory
> ```
{ variable }
```

## Get matched group
#### Get N<sup>th</sup> matched group of client pattern
> ```
%N
```
Example to get first matched
> ```
%1
```

#### Get N<sup>th</sup> matched group of bots pattern
> ```
%!N
```
Example to get first matched
> ```
%!1
```

## Recursion
> Get response as if client said this new statement
```
{% chat statement %}
```
It will do a pattern match for statement

## Condition
>``` 
{% if condition %} do this first {% elif condition %} do this next {% else %} do otherwise {% endif %}
```

## Change Topic
> ```
{% topic TopicName %}
```

## Interact with python function
> ```
{% call functionName: value %}
```

## Execute shell script
> ```
[ cmd ]
```
Execute command in think mode
> ```
[! cmd ]
```

## Topic based group 
>```
{% group topicName %}
  {% block %}
      {% client %}client says {% endclient %}
      {% response %}response test% endresponse %}
  {% endblock %}
  ...
{% endgroup %}
```

## Learn
> ```
{% learn %}
  {% group topicName %}
    {% block %}
        {% client %}client says {% endclient %}
        {% response %}response test% endresponse %}
    {% endblock %}
    ...
  {% endgroup %}
  ...
{% endlearn %}
```

# To upper case
>```
{% up string %}
```

# To lower case
>```
{% low string %}
```

# Capitalize
>```
{% cap string %}
```

# Previous
>```
{% block %}
    {% client %}client's statement pattern{% endclient %}
    {% prev %}previous bot's statement pattern{% endprev %}
    {% response %}response string{% endresponse %}
{% endblock %}
```
