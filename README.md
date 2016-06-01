# Chatbot
Python chatbot

```python
# should contain topic '*'
from chatbot import *
pair = {  topicName1: 
                  (
                    ( "Pattern to match what clent said",
                      "Pattern to match what bot said",#Optional
                      ( "Bots response 1", # bot makes a rangom choice of one from this
                        "Bots response 2",
                        "Bots response 3",
                        ...
                      )
                    ),
                    ...
                  ),
          topicName2: 
                  (
                    ( "Pattern to match what clent said",
                      "Pattern to match what bot said",#Optional
                      ( "Bots response 1",
                        "Bots response 2",
                        "Bots response 3",
                        ...
                      )
                    ),
                    ...
                  ),
          ...
        }
firstQuetion =`first thing that bot would say`
Chat(pairs, reflections).converse(firstQuetion)
```
The Pattern is python regex pattern.


## List of feature supported in bot response
1. [Memory](#memory)
2. [Get matched group](#get-matched-group)
3. [Recursion](#recursion)
4. [Condition](#condition)
5. [Change Topic](#change-topic)
6. [Interact with python function](#interact-with-python-function)
6. [Execute shell script](#execute-shell-script)

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
