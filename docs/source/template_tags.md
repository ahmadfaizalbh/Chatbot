# Template Tags

> Template tags are used to generating the chat response. These are like web template system similar to JINJA template.
> Currently we have two type of tags Block tags and General tags. Each of them have different type of tags list.

> Block tags are block,learn,response,client,prev,group.

> General tags are if,endif,elif,else,chat,low,up,cap,call,topic

> Both tags have their own handler methods to process the template.
> Some tags are exceptional doesn't have endtag like call, low, up.

## syntax

Each tag must be inside this `{% %}` with single space before and after tagname.
It must have the endtag except some exceptional tags.

```
{% tagname %} ... {% endtagname %}
```

### Example

Sample block tag.

```
{% block %} ... {% endblock %}
```

## Group Tags

Group template tag keyword is `group`. 
It is a combination of multiple block tags or response tags into a single group.

Each group can have multiple sub-groups, client, response and learn tags. If we didn't
create block inside the group or group without topic name those will be a generic group.

Response of sub-groups order will be current block, parent block and generic block.
> Group tag must have at-least one of these tags block, group or response tag.

### Template Syntax

```
{% group topicname %}...{% endgroup %}
```

#### Generic Group sample Template

Below Template sample is a general group.
`{% group %}` group tag without the topicname.

```
{% group %}
{% block %}
    {% client %}show (?P<name>.*){% endclient %}
    {% response %}{ %name }{% endresponse %}
{% endblock %}
{% endgroup %}
```

### Named group sample Template

Below template is named group sample  `continent` is a group name.
It's also a nested group.

We have the name `{% group continent %}` after the group keyword.

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

Block template tag keyword is `block`. 
This used to separate the client query and response inside the particular group.

> Block tag must have at-least one of these tags client, learn, response or prev.

Example, Asia continent group we can have population and country query in different blocks.

```
{% group asia%}
  {% block %}
    {% client %}What is the population{% endclient %}
    {% response %}100000{% endresponse %}
  {% endblock %}
  {% block %}
    {% client %}How many countries?{% endclient %}
    {% response %}100{% endresponse %}
  {% endblock %}
{% endgroup %}
```

### Template Syntax

```
{% block %}.*{% endblock %}
```

### Template sample

Sample block tag with at-least single client tag.

```
{% block %}
    {% client %}(what is|(do you remember|tell me) about) (?P<name>.*){% endclient %}
{% endblock %}
```

## Client Tags

Client template tag keyword is `block`. 
This is used as a user input matcher. 
It can have static, dynamic and multiple user inputs matches inside this tag. 

Multiple user input we need to user `|`,`&` operator [regex](https://docs.python.org/3/howto/regex.html) 
used to find the user inputs matching. 

### Template Syntax

```
{% client %}...{% endclient %}
```

### Static input sample

Below sample, we are handing the static user input. Giving response 
to the client query.

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

### Multiple input sample

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
Response template tag keyword is `response`.
This is used for giving response to user queries.

It can have the static response, dynamic response or calling a function.

### Template Syntax

```
{% response %}...{% endresponse %}
```

### Dynamic response Template
Below sample have the random response for the single user input. 

Block tag have the single client tag and multiple response tags.
Response tag are chosen randomly.

``` 
    {% block %}
        {% client %}I need (.*){% endclient %}
        {% response %}Why do you need %1?{% endresponse %}
        {% response %}Would it really help you to get %1?{% endresponse %}
        {% response %}Are you sure you need %1?{% endresponse %}
    {% endblock %}
```

#### Chat Sample

When, user enter the sample query multiple times we get the random response from the current block.

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

## Previous Tags

Previous template tag keyword is `prev`. 
Previous tag used to match previous bot message.
A regex pattern is added between {% prev %} and {% endprev %}.

It must be inside the block tag also must have at-least one client tag inside this block.

### Syntax

```
{% block %}
     {% client %} ... {% endclient %}
     {% prev %}Regex Pattern{% endprev %}
{% endblock %}
```

### Sample Template

If Chatbot ask query `how are you` and user text can be `I feel/am feeling/ am absolutely good`.
We are matching the current user input with the previous text and returning the response.

```
{% block %}
    {% client %}(I (am|feel) )?(feeling )?(absolutely )?(.*){% endclient %}
    {% prev %}.*how are you{% endprev %}
    {% response %}{% if {%low %5 %} == fine | {%low %5 %} == good | {%low %5 %} == happy %}  Nice to know that you are %5. What else? {% else %} why you feel %5 {% endif %}{% endresponse %}
{% endblock %}
```

#### Chat Sample

Below Sample, we have the auto query from bot `Hi, how are you?`.  
If user enter `I feel good` or in the pattern inside the above sample template client tag.

It matched the response condition now we get the response `Nice to know that you are good`.

```
Hi, how are you?
> I feel good
  Nice to know that you are good. What else? 
 
```

## Learn Tags

Learn template tag keyword is `learn`.
It is used to give dynamic object and description without static object and response.

It must me inside the block tag also must have at-least one client tag 
either inside the learn tag block or on outer block tag.

### Syntax

It must have the group and block tag inside it. All the rules and features for group and block
tags applies for these inner tag as well.

```
{% block %}
    {% client %}...{% endclient %}
    {% learn %}
        {% group %}
            {% block %}
                ....
            {% endblock %}
        {% endgroup %}
    {% endlearn %}
{% endblock %}
```

### Learn tag template sample

Below example, we do not have the static variable and value
`(?P<object>.*) ` is variable take any input , their value must start with is/are `(?P<description>(is|are) .*)`.

Above mention object and description is added inside the learn tag with client query and response for the user next
response.

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

### Chat Sample to get the value from learn tag

Below sample `remember` is the client static input and `learn` is a variable startswith `is` and other description.
This will be added to memory.

```
> remember learn is tag give dynamic response
I will remember that learn is tag give dynamic response
```

We can return the description response when the query raised from user `tell me about learn`.

```
> tell me about learn
learn is tag give dynamic response
```

## Call tag

Call template tag keyword is `call`. 
It is used for calling custom function which is having the logic to handle the use inputs.

Function needs to be registered the before calling it. Each function name must be unique.
`register_call` decorator will check the unique function name 
and append the current function to the session

### Sample code to register a function:

```
from chatbot import register_call

@register_call("increment_count")
def memory_get_set_example(session, query):
    name=query.strip().lower()
    # Get memory
    old_count = session.memory.get(name, '0')
    new_count = int(old_count) + 1
    # Set memory
    session.memory[name]=str(new_count)
    return f"count  {new_count}"

```

### Syntax
```
{% call function_name %}
```

### Template Sample

Below is the sample of `increment_count` function.
This will take the variable and increase it count on memory

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