# Recursion
Chat tag `{% chat %}` is used to handle the recursion.
It must be inside the response tag.

## Syntax

Chat tag can be added along with other responses.

```
{% response %}... {% chat ... %} ... {% endresponse %}
```

## Some UseCases
Recursion is useful in scenarios like handling user input implicitly.

i)  Removing or ignoring repeated words in the Inputs
ii) sending multiple response

### Remove repeated inputs
Sometimes user accidentally enter the same text multiple times. 
This is unwanted chat need only regex pattern matched text. 
Here chat remove the unwanted text recursively ( number of the times text appears ).

#### Template Example
Below sample, `{% chat %1 %}` tag is added. 
This the regex pattern `%1` matches the first value in the client tag that's `Please`.
Now this text will be ignored recursively and final response will be based on user entered text.

```
{% block %}
    {% client %}Please (.*){% endclient %}
    {% response %}{% chat %1 %}{% endresponse %}
{% endblock %}
```


#### Chat Example

Multiple **please** word is entered in the chat those are removed implicitly and user input 
will be taken for response. These responses are based on `default.template`.

1. 

Below sample `check` is taken as user input and matched with template and return the response.

```
> please please check
>  why you feel check this  
```

2. 
Below sample `note this` is taken as user input and matched with template and return the response.

```
> please please note this
> note this  .
```

### Send the Multiple chat response to user
If user enter multiple queries in a chat, they need answers for both.

Instance like **tell me about apples and mango?** 
we need to give answer for both apple and mango.

#### Template Sample
```
{% block %}
    {% client %}(Do you know about|what is|who is|tell me about) (?P<query1>.*)(,| and | \& )(?P<query2>.*){% endclient %}
    {% response %}
           {% chat %1 %query1 %}
           ------------------------------------
           {% chat %1 %query2 %}
    {% endresponse %}
{% endblock %}
{% endblock %}
```

Above sample, we have regex pattern match `(?P<query1>.*)(,| and | \& )(?P<query2>.*)`.
This will match the user input in two variable *query1* , *query2* and then create two different
chat queries. `, and &` these will separate the two inputs `(,| and | \& )`.

If user enter below query
> `Do you know about Python and C`

This will be converted to two chat responses by template itself.

```
{% chat Do you know about Python %}
-----------------------------------
{% chat Do you know about c %}
```

Now this query will be matched with other template and get the response.

#### Chat Sample

Below chat get the response from wikipedia after converting to two different chat each of them will be matched in other template
that will call the wikipedia and return the response. 

This operation occurs recursively and get the response from wiki. Both query responses return after fetching the information.

```
> Do you know about Python and C

> Python is an interpreted high-level general-purpose programming language. 
  Its design philosophy emphasizes code readability with its use of significant indentation..... 
> -----------------------------------------
> C  is a general-purpose, procedural computer programming language supporting structured programming, 
   lexical variable scope, and recursion, with a static type system......
