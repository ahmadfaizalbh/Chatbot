Currently, supported to following language support English, German, Hebrew, Portuguese (Brazil). Each language we have
substitutions and spellcheck.

# Add a new language

Add a new language inside the local folder. Folder name must be
in [ISO-639_1 codes](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes). Local folder is inside
the [chatbot](https://github.com/ahmadfaizalbh/Chatbot/tree/master/chatbot/local) folder.

# Add a template

Add a ***default.template*** file inside a specific language folder and add the template details.

## Example

iso code for english is `en`. So Folder name must be **en**. Inside this folder we create file **default.template**

# Spellcheck and Substitutions

Spellcheck we have ***words.txt*** file. If the word is more than three character then it'll be compare inside the words.txt
file for corrections.

Spellchecker works during the user input process. Typos will be autocorrected before matching it with template.

Each language folder have the ***substitutions.json*** for substitutions for texts. This will be working when the input
is processed.

substitutions file must have a dictionary with key value pairs of words and their alternatives.

## Syntax

gender: This contains male and female pronouns as key value pair. 
person: This contains the subject pronouns. 
person2: This contains the subject pronoun as key and  object pronoun as value
normal: short word as a key their full-form as value
reflections: reflections of same sentence 

{
"gender":{"he":"she", "him":"her"},
"person":{"I": "he","she": "I"},
"person2":{ "I": "you","me": "you",},
"normal":{ "wanna": "want to","gonna": "going to",},
"reflections":{ "i am": "you are","i was": "you were",} }


## Example of English
Here we have full list of english language substitutions
`
{
"gender": {
"he": "she",
"him": "her",
"his": "her",
"himself": "herself",
"she": "he",
"her": "him",
"hers": "his",
"herself": "himself"
},
"person": {
"I": "he",
"me": "him",
"my": "his",
"mine": "his",
"myself": "himself",
"he": "I",
"him": "me",
"his": "my",
"himself": "myself",
"she": "I",
"her": "me",
"hers": "mine",
"herself": "myself"
},
"person2": {
"I": "you",
"me": "you",
"my": "your",
"mine": "yours",
"myself": "yourself",
"you": "me",
"your": "my",
"yours": "mine",
"yourself": "myself"
},
"normal": {
"wanna": "want to",
"gonna": "going to",
"yha": "yes",
"aye": "yes",
"yep": "yes",
"yea": "yes",
"affirmative": "yes",
"roger": "yes",
"uh-huh": "yes",
"righto": "yes",
"yuppers": "yes",
"yup": "yes",
"ja": "yes",
"surely": "yes",
"amen": "yes",
"totally": "yes",
"sure": "yes",
"yessir": "yes",
"okey-dokey": "yes",
"uh-uh": "no",
"nix": "no",
"nixie": "no",
"nixy": "no",
"nixey": "no",
"nope": "no",
"nay": "no",
"nah": "no",
"negative": "no",
"veto": "no",
"none": "no",
"ok": "okay",
"o.k": "okay",
"okey": "okay",
"I'm": "I am",
"I'd": "I would",
"I'll": "I will",
"I've": "I have",
"you'd": "you would",
"you're": "you are",
"you've": "you have",
"you'll": "you will",
"he's": "he is",
"he'd": "he would",
"he'll": "he will",
"she's": "she is",
"she'd": "she would",
"she'll": "she will",
"we're": "we are",
"we'd": "we would",
"we'll": "we will",
"we've": "we have",
"they're": "they are",
"they'd": "they would",
"they'll": "they will",
"they've": "they have",
"y'all": "you all",
"can't": "can not",
"cannot": "can not",
"couldn't": "could not",
"wouldn't": "would not",
"shouldn't": "should not",
"isn't": "is not",
"ain't": "is not",
"don't": "do not",
"aren't": "are not",
"won't": "will not",
"weren't": "were not",
"wasn't": "was not",
"didn't": "did not",
"hasn't": "has not",
"hadn't": "had not",
"haven't": "have not",
"where's": "where is",
"where'd": "where did",
"where'll": "where will",
"who's": "who is",
"who'd": "who did",
"who'll": "who will",
"what's": "what is",
"whats": "what is",
"what'd": "what did",
"what'll": "what will",
"when's": "when is",
"when'd": "when did",
"when'll": "when will",
"why's": "why is",
"why'd": "why did",
"why'll": "why will",
"it's": "it is",
"it'd": "it would",
"it'll": "it will"
},
"reflections": {
"i am": "you are",
"i was": "you were",
"i": "you",
"i'm": "you are",
"i'd": "you would",
"i've": "you have",
"i'll": "you will",
"my": "your",
"you are": "I am",
"you were": "I was",
"you've": "I have",
"you'll": "I will",
"your": "my",
"yours": "mine",
"you": "me",
"me": "you"
}
}

`
