Chatbot
=======

Python chatbot AI that helps in creating a Python based chatbot with
minimum coding. This provides both AI bots and chat handler and also
allows easy integration of REST API's and python function calls which
makes it unique and more powerful in functionality. This AI provides
numerous features like learn, memory, conditional switch, topic-based
conversation handling, etc.

Installation
------------

Installing from PyPI:

.. code:: sh

    pip install chatbotAI

Installing from github:

.. code:: sh

    git clone https://github.com/ahmadfaizalbh/Chatbot.git
    cd Chatbot
    python setup.py install

Demo
----
.. code:: sh

    >>> from chatbot import demo
    >>> demo()
    Hi, how are you?
    > i'm fine
    Nice to know that you are fine  
    > quit
    Thank you for talking with me.
    >>>


Sample Code (with wikipedia search API integration)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

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

For details on how to build Facebook messenger bot checkout `Facebook
Integration.ipynb <https://github.com/ahmadfaizalbh/Meetup-Resources/blob/master/Facebook%20Integration.ipynb>`__

For Jupyter notebook Chatbot checkout `Infobot built using
NLTK-Chatbot <https://github.com/ahmadfaizalbh/Meetup-Resources/blob/master/How%20to%20build%20a%20bot.ipynb>`__

Sample Apps
"""""""""""

1. A sample facebook messenger bot built using
   `messengerbot <https://github.com/geeknam/messengerbot/pulls>`__,
   `Django <https://github.com/django/django>`__ and
   `NLTK-Chatbot <#chatbot>`__ is available here `Facebook messenger
   bot <https://github.com/ahmadfaizalbh/FacebookMessengerBot/>`__
2. A sample microsoft bot built using `Microsoft Bot Connector Rest API
   -
   v3.0 <https://docs.botframework.com/en-us/restapi/connector/#navtitle>`__,
   `Django <https://github.com/django/django>`__ and
   `NLTK-Chatbot <#chatbot>`__ is available here `Micosoft
   Chatbot <https://github.com/ahmadfaizalbh/Microsoft-chatbot/>`__

List of features supported in bot template
-----------------------------------------

1.  `Memory <#memory>`__
2.  `Get matched group <#get-matched-group>`__
3.  `Recursion <#recursion>`__
4.  `Condition <#condition>`__
5.  `Change Topic <#change-topic>`__
6.  `Interact with python function <#interact-with-python-function>`__
7.  `REST API integration <#rest-api-integration>`__
8.  `Topic based group <#topic-based-group>`__
9.  `Learn <#learn>`__
10. `To upper case <#to-upper-case>`__
11. `To lower case <#to-lower-case>`__
12. `Capitalize <#capitalize>`__
13. `Previous <#previous>`__

--------------

Memory
^^^^^^

Set Memory
""""""""""

.. code:: sh

    { variable : value }

In think mode

.. code:: sh

    {! variable : value }

Get Memory
""""""""""

.. code:: sh

    { variable }

Get matched group
^^^^^^^^^^^^^^^^^
for grouping in regex refer `Python regular expression docs <https://docs.python.org/3/howto/regex.html#non-capturing-and-named-groups?>`__

Get N :superscript:`th` matched group of client pattern
"""""""""""""""""""""""""""""""""""""""""""""""""""""""

.. code:: sh

    %N

Example to get first matched

.. code:: sh

    %1

Get matching named group of client's patterns
""""""""""""""""""""""""""""""""""""""""""

.. code:: sh

    %Client_pattern_group_name

Example to get matching named group ``person``

.. code:: sh

    %person

Get N :superscript:`th` matched group of bots pattern
"""""""""""""""""""""""""""""""""""""""""""""""""""""

.. code:: sh

    %!N

Example to get first matched

.. code:: sh

    %!1

Get matching named group of bot's message patterns
""""""""""""""""""""""""""""""""""""""""""""""""

.. code:: sh

    %!Bot_pattern_group_name

Example to get matching named group ``region``

.. code:: sh

    %!region

Recursion
^^^^^^^^^

Get response as if client said this new statement

.. code:: sh

    {% chat statement %}

It will do a pattern match for statement

Condition
^^^^^^^^^

::

    {% if condition %}
        do this first
    {% elif condition %}
        do this next 
    {% else %}
        do otherwise
    {% endif %}

Change Topic
^^^^^^^^^^^^

.. code:: sh

    {% topic TopicName %}

Interact with python function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


In python

.. code:: python

    @register_call("functionName")
    def function_name(session, query):
        return "response string"

In Template

.. code:: sh

    {% call functionName: value %}

REST API integration
^^^^^^^^^^^^^^^^^^^^

In API.json file
""""""""""""""""

.. code:: sh

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

*If authentication is required only then* ``auth`` *method is needed. The* ``data`` *and* ``params`` *defined in pi.json file acts as defult values and all key value pair defined in template file overrides the default value.* ``value_getter`` *consistes of list of keys in order using which info from json will be collected.*

In Template file
""""""""""""""""

.. code:: sh

    [ APIName:MethodName,Key1:value1 (,Key*:value*) ]

you can have any number of key value pair and all key value pair will
override data or params depending on ``method``, if ``method`` is
``POST`` then it overrides data and if method is ``GET`` then it
overrides ``params``.

Topic based group
^^^^^^^^^^^^^^^^^

.. code:: sh

    {% group topicName %}
      {% block %}
          {% client %}client says {% endclient %}
          {% response %}response text{% endresponse %}
      {% endblock %}
      ...
    {% endgroup %}

Learn
^^^^^

.. code:: sh

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

To upper case
^^^^^^^^^^^^^

.. code:: sh

    {% up string %}

To lower case
^^^^^^^^^^^^^

.. code:: sh

    {% low string %}

Capitalize
^^^^^^^^^^

.. code:: sh

    {% cap string %}

Previous
^^^^^^^^

.. code:: sh

    {% block %}
        {% client %}client's statement pattern{% endclient %}
        {% prev %}previous bot's statement pattern{% endprev %}
        {% response %}response string{% endresponse %}
    {% endblock %}
