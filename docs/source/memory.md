# Memory
> Memory store the information/value for any user specific attributes, for example storing users names, age, other details or any other information user want the bot to remember.
>
> Helps in setting up remainders and knowledge-base. This can be done in template response tag or python call back functions through session objects.

## SET MEMORY
### Set memory with-in template tag
Setting memory with-in template should be done between 
`{% response %}` and `{% endresponse %}` tags.

#### Set memory in copy mode
setting up memory in copy mode stores value for given variable name for current user and puts the value as part of the
text in place of set memory tag or can be used for any other purpose like with-in condition or callbacks.

##### Syntax
```
{ vairable_name : value }
```

##### Example
1. constant value set string value `Arun` in variable `Name`.

   ```
   { Name : Arun }
   ```

2. dynamic value (set from client match group) set `full_name` entity from client message match group as `Name`.

   ```
   { Name : %full_name }
   ```

   or set first matching group from client message as `Name`

   ```
   { Name : %1 }
   ```

3. dynamic variable name with constant value set `object` entity from client message group as variable name with
constant value `Hot`.

   ```
   { %object: Hot }
   ```   

4. dynamic variable name and value

   set `object` entity from client message group as variable name and `property` entity from client message group.
   
   ```
   { %object : %property }
   ```

5. Full block example
   ##### Template
   Below Template, we have the variable as `name` and value as `value` for the variable both are regex based inputs.
   when user enter the inputs it'll be stored in memory and return the response tag value to user.
   ```
   {% group %}
       {% block %}
           {% client %}remember (?P<name>.*) is (?P<value>.*){% endclient %}
           {% response %}I will remember %name is { %name : %value }{% endresponse %}
       {% endblock %}
   {% endgroup %}
   ```
   
   ##### Chat Sample
   In below example memory for current user session variable `sun` will be set with value
   `is red hot star in our solar system`.
   
   Now the response text is return automatically from the template.
   ```
   > remember sun is red hot star in our solar system
   I will remember sun is red hot star in our solar system
   ```

   

#### Set memory in think mode

setting up memory in copy mode stores value for given variable name for current user and returns nothing. Hence, when it
is used with-in response tag it'll be replaced by empty string. 

As we can see in below syntax we have the `!` symbol before the variable name to differentiate between think and copy mode of template tag.

##### Syntax

```
{! vairable_name : value }
```

##### Example
Number 25 is set to Age variable
```
{!Age: 25}
```

##### Full block example
Below example age input field takes the Integer values and store it in memory.
```
{% group %}
    {% block %}
        {% client %}My age is (?P<age>\d+){% endclient %}
        {% response %}
            I will remember your age {! age: %age }
        { % endresponse %}
    {% endblock %}
{% endgroup %}
```

##### Chat Sample  
Age will be store for the current user in memory and not included in the response, as you can see from the above
example.
```
> My age is 29
I will remember your age
```
## GET MEMORY
Get Memory is used to get the values stored in the memory object.
we can get memory in two ways   
1. Template Tag
2. Python session

### Get memory value with-in template tag
This type of get memory used inside the template tags. 
It can be used for response or ask query to user.

##### Syntax
```
{ variable_name }
```

#### Example 
`name` is the key value store in the memory. 

```
{name}
```
#### Full block sample

##### Template
Below template sample we have the query
`Do you (know|remember) my name?` for this the response will be checking the 
`name` key in the memory and return the value if it exists or just return the question.
```

{% block %}
    {% client %}Do you (know|remember) my name{% endclient %}
    {% response %}{% if {name} %}Yes I do {name}{% else %}No,{% chat what is my name %}{% endif %}{% endresponse %}
{% endblock %}
```

#####Chat Sample
Chat sample name is already stored in memory . So it's returning
`Yes I do Arun`. 

```
> do you name my name? 
> Yes I do Arun
```

### Set and Get memory value in python session
Session object in python caller function has attribute memory,
Which is dictionary kind of object where user specific info is stored.

#### Syntax set memory
```
 session.memory[variable_name] = value
```
##### Example
Below example variable name is `year` and setting value as `2021`.
```
session.memory[year] = 2021 
```

#### Syntax

1. ```
   session.memory.get(variable_name)
   ```
   
 2. ```
    session.memory[variable_name]
    ```

##### Example
To get the `year` value from the memory we can use below ways

1. ```
   session.memory.get('year')
   ```
2. ```
   session.memory['year']
   ```