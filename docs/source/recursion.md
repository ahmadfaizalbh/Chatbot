# Recursion
> Recursion gives the recursive multiple response to the user query.
> It picks the particular block matches with the user query and return the response on that block
> Whichever block or prev tag matched to user input will be picked for the response.

## Syntax
```
{% chat statement %}
```

### Template Sample
`Please (.*)` is the user query matching text. `chat` will match the specific `block`
or `prev` tag matched with the `Please` 
```
{% block %}
{% client %}Please (.*){% endclient %}
{% response %}{% chat %1 %}{% endresponse %}
{% endblock %}
```

#### Full Template sample
Below sample, we are having the user input matching template and matched response template

1. user input block


When user type `Please`  with some text we have the response as `chat` this will be matched with the other blocks
with the matching user input.

```
{% block %}
{% client %}Please (.*){% endclient %}
{% response %}{% chat %1 %}{% endresponse %}
{% endblock %}
```

1. response block

Sample response for the above user input.

```
{% response %}Please tell me more.{% endresponse %}
{% response %}Let's change focus a bit... Tell me about your family.{% endresponse %}
{% response %}Can you elaborate on that?{% endresponse %}
{% response %}Why do you say that %0?{% endresponse %}
{% response %}I see.{% endresponse %}
{% response %}Very interesting.{% endresponse %}
{% response %}%0.{% endresponse %}
{% response %}I see.  And what does that tell you?{% endresponse %}
{% response %}How does that make you feel?{% endresponse %}
{% response %}How do you feel when you say that?{% endresponse %}
```

#### Chat Sample
Below example when user type `Please reply`
now chatbot will match this to recursive response as `Very interesting.` 
that we have in above full template sample.

If we ask the sample question we get the different response from first matched block.

One of our response have `{% response %}%0.{% endresponse %}` 
so we are getting the user input value as response in the last chat sample



```
> Please reply          
Very interesting.

> Please do something
How do you feel when you say that?

> Please help to get the info
help to get the info .

```