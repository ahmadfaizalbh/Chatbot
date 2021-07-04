# Template Tags
> Template tags are generating the chat response. 
> These are like web template system similar to JINJA template with following tags Group, Block, Client, Response and Learn Tags

## Group Tags
Group tag are used to group the response to particular topic. Each group can have multiple subgroups group.
If we didn't create block inside the group or group without topic name those will be a generic group.

Sub-group response will be checked and return from the current block, parent block and generic block.

### Template Syntax
```
{% group topicname %}
    ...
{% endgroup %}
```

#### Generic Group sample Template
Below Template sample we have the general group.
`{% group %}` group tag doesn't have the name 

```
{% group %}
{% block %}
    {% client %}show (?P<name>.*){% endclient %}
    {% response %}{ %name }{% endresponse %}
{% endblock %}
{% endgroup %}
```

### Named group sample Template
Below template is sample for named group and nested group.

We have the name `{% group continent %}` inside the group tag. So this will be under the continent group.

```
{% group continent %}
    {%  group asia %}
        {% client %}Regex{% endclient %}
        {% response %} Response{% endresponse %}
    {% endgroup %}
    {% group europe %}
        {% client %}Regex{% endclient %}
        {% response %} Response{% endresponse %}
    {% endgroup %}
    ...
{% endgroup %}
```



## Block Tags 
Block holds each client query and response details. Every block must have the at-least one client block.

### Template Syntax
```
{% block %}
...
{% endblock %}
```
### Template sample
Sample block tag with at-least single client tag.
```
{% block %}
    {% client %}(what is|(do you remember|tell me) about) (?P<name>.*){% endclient %}
{% endblock %}
```

## Client Tags
Client tag is user input handler. We can have static, dynamic and multiple user input inside this tag.
Dynamic text we are handling with python [regex](https://docs.python.org/3/howto/regex.html). 
Multiple user input we need to user `|` operator.

### Template Syntax
```
{% client %}
{% endclient %}
```

### Static input sample
Below sample, we are handing the static user input.

```
{% block %}
    {% client %}What is your name{% endclient %}
    {% response %}My name is ChatBot{% endresponse %}
{% endblock %}
```

#### Chat sample
```
> What is your name
My name is ChatBot
```

### Dynamic input sample
`(?P<name>.*)` is the regex based input and stores the input in the variable `name`.
Later we have display this to user or store in memory
```
{% block %}
    {% client %} show (?P<name>.*){% endclient %}
    {% response %}%name{% endresponse%}
{% endblock %}
```
#### Chat sample
Below example takes the random input from user.

```
> show Age
Age
```
### Multiple input Template
Using the `|` we can take multiple inputs
```
{% block %}
    {% client %}(what is|(do you remember|tell me) about) (?P<name>.*){% endclient %}
    {% response %} %name {% endresponse %}
{% endblock %}
```

#### Chat Sample
Below sample, we can return same response to multiple user queries
1. 
```
> What is about sun
 sun
```
2. 
```
> do you remember about sun
sun
```

## Response Tags
Response tag used for give response to user queries.
we can have the static response, dynamic response or calling a function.

### Template Syntax
```
{% response %}
...
{% endresponse %}
```

### Dynamic response Template
Below sample have the random response for the single client

``` 
    {% block %}
    {% client %}I need (.*){% endclient %}
    {% response %}Why do you need %1?{% endresponse %}
    {% response %}Would it really help you to get %1?{% endresponse %}
    {% response %}Are you sure you need %1?{% endresponse %}
    {% endblock %}
```
#### Chat Sample

When, user enter the sample query multiple times we get the random response.
1.  
```
>I Need something
Why do you need  something
```

2. 
```
>I Need something
Are you sure you need something
```

### Function call sample Template

`call` is used for calling custom function which is having the logic to handle the use inputs.

Below is the sample of increment_count function. This will take the variable and increase it count on memory

```
{% block %}
    {% client %}increment (?P<name>.*){% endclient %}
    {% response %}{% call increment_count: %name %}{% endresponse %}
{% endblock %}
```

#### Chat Sample
Below sample Age variable value is increased in the memory.

1.
```
> increment Age
Age 1
```
2. 
```
increment Age
Age 2
```



## Previous Tags
Previous tag helps to give the proper response or save some input for future response 

### Template Syntax
```
{% prev %}
{% endprev %}
```

### Sample previous Template
```
{% block %}
    {% client %}(I (am|feel) )?(feeling )?(absolutely )?(.*){% endclient %}
    {% prev %}.*how are you{% endprev %}
    {% response %}{% if {%low %5 %} == fine | {%low %5 %} == good | {%low %5 %} == happy %}  Nice to know that you are %5. What else? {% else %} why you feel %5 {% endif %}{% endresponse %}
{% endblock %}
```
#### Chat Sample
```
> I am feeling good
 Nice to know that you are good. What else? 
```

## Learn Tags
Learn tag is dynamic object and description without static object and response.

### Syntax
```
{% learn %}
{% endlearn %}
```
### Learn tag template sample
Below example, we do not have the static variable and value
`(?P<object>.*) ` is variable take any input , their value must start with is/are `(?P<description>(is|are) .*)`.

Above mention object and description is added inside the learn tag with client query and response for the user next response.

```
{% block %}
    {% client %}Remember (?P<object>.*) (?P<description>(is|are) .*){% endclient %}
    {% response %}I will remember that %object %description {% endresponse %}
    {% learn %}
      {% group %}
        {% block %}
            {% client %}(Do you know|tell me) about %object{% endclient %}
            {% response %}%object %description{% endresponse %}
        {% endblock %}
      {% endgroup %}
    {% endlearn %}
{% endblock %}
```

###Chat Sample to get the value from learn tag

remember is the client static input and `learn` is a variable startswith `is` and other description.
This will be added to memory.
```
> remember learn is tag give dynamic response
I will remember that learn is tag give dynamic response
```

We can return the description response when the query raised from user `tell me about learn`/
```
> tell me about learn
learn is tag give dynamic response
```
