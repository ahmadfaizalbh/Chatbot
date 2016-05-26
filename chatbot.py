# Natural Language Toolkit: Chatbot Utilities
#
# Copyright (C) 2001-2016 NLTK Project
# Authors: Steven Bird <stevenbird1@gmail.com>
# URL: <http://nltk.org/>
# For license information, see LICENSE.TXT

# Based on an Eliza implementation by Joe Strout <joe@strout.net>,
# Jeff Epler <jepler@inetnebr.com> and Jez Higgins <jez@jezuk.co.uk>.
from __future__ import print_function

import re
import random
from nltk import compat
from py_execute.process_executor import execute
from mock import Mock


reflections = {
  "i am"       : "you are",
  "i was"      : "you were",
  "i"          : "you",
  "i'm"        : "you are",
  "i'd"        : "you would",
  "i've"       : "you have",
  "i'll"       : "you will",
  "my"         : "your",
  "you are"    : "I am",
  "you were"   : "I was",
  "you've"     : "I have",
  "you'll"     : "I will",
  "your"       : "my",
  "yours"      : "mine",
  "you"        : "me",
  "me"         : "you"
}


class Chat(object):
    def __init__(self, pairs, reflections={}):
        """
        Initialize the chatbot.  Pairs is a list of patterns and responses.  Each
        pattern is a regular expression matching the user's statement or question,
        e.g. r'I like (.*)'.  For each such pattern a list of possible responses
        is given, e.g. ['Why do you like %1', 'Did you ever dislike %1'].  Material
        which is matched by parenthesized sections of the patterns (e.g. .*) is mapped to
        the numbered positions in the responses, e.g. %1.

        :type pairs: list of tuple
        :param pairs: The patterns and responses
        :type reflections: dict
        :param reflections: A mapping between first and second person expressions
        :rtype: None
        """

        self._pairs = [(re.compile(x, re.IGNORECASE),y) for (x,y) in pairs]
        self._reflections = reflections
        self._regex = self._compile_reflections()
        self._memory = {}


    def _compile_reflections(self):
        sorted_refl = sorted(self._reflections.keys(), key=len,
                reverse=True)
        return  re.compile(r"\b({0})\b".format("|".join(map(re.escape,
            sorted_refl))), re.IGNORECASE)

    def _substitute(self, str):
        """
        Substitute words in the string, according to the specified reflections,
        e.g. "I'm" -> "you are"

        :type str: str
        :param str: The string to be mapped
        :rtype: str
        """

        return self._regex.sub(lambda mo:
                self._reflections[mo.string[mo.start():mo.end()]],
                    str.lower())
        
    def _mapSolve(self,response,start,end):
        think=0
        if response[start+1] != "!":
            s=response[start+1:end].strip().split(":")
        else:
            think=1
            s=response[start+2:end].strip().split(":")
        name = s[0]
        i=0
        for i in range(1,len(s)):
            if name[-1]=="\\":
                name += ":"+s[i]
            else:
                i-=1
                break
        i+=1
        name = name.strip().lower()
        if i<(len(s)):
            value = s[i]
            for i in range(i+1,len(s)):
                if value[-1]=="\\":
                    value += ":"+s[i]
                else:
                    break
            self._memory[name] = self._substitute(value.strip())
        if think or not name in self._memory:
            return ""
        return self._memory[name]
    
    def _map(self,response):
        pos = [m.start(0) for m in re.finditer(r'[{}]', response)]
        newPos = [start for start in pos if (not start) or response[start-1]!="\\" ]
        i=0
        while newPos:
            for i in range(1,len(newPos)):
                if response[newPos[i]] == "}":
                    break
            if response[newPos[i-1]] == "{":
                start,end = newPos[i-1],newPos[i]
                substitution = self._mapSolve(response,start,end)
                diff = len(substitution) - (end-start+1)
                for j in range(i+1,len(newPos)):
                    newPos[j] += diff
                newPos.pop(i)
                newPos.pop(i-1)
                response = response[:start] + substitution + response[end+1:]
            else:
                raise SyntaxError("invalid syntax")
        return response
    
    def _evalSolve(self,response,start,end):
        think=0
        cmdStart = start+1
        if response[cmdStart] == "!":
            think=1
            cmdStart += 1
        cmd = response[cmdStart:end]
        cmd = self._map(cmd)
        result = execute(cmd, ui=Mock())
        if result[0]:
            raise SystemError("%d\n%s" % result)
        if think:
            return ""
        return result[1].replace("{","\{").replace("}","\}")
    
    def _eval(self,response):
        pos = [m.start(0) for m in re.finditer(r'[\[\]]', response)]
        newPos = [start for start in pos if (not start) or response[start-1]!="\\" ]
        i=0
        while newPos:
            for i in range(1,len(newPos)):
                if response[newPos[i]] == "]":
                    break
            if response[newPos[i-1]] == "[":
                start,end = newPos[i-1],newPos[i]
                substitution = self._evalSolve(response,start,end)
                diff = len(substitution) - (end-start+1)
                for j in range(i+1,len(newPos)):
                    newPos[j] += diff
                newPos.pop(i)
                newPos.pop(i-1)
                response = response[:start] + substitution + response[end+1:]
            else:
                raise SyntaxError("invalid syntax")
        return self._map(response).replace("\{","{").replace("\}","}")
   
    def _wildcards(self, response, match):
        pos = response.find('%')
        for m in re.finditer(r'%[0-9]+', response):
            start = m.start(0)
            end = m.end(0)            
            num = int(response[start+1:end])
            response = response[:start] + \
                self._substitute(match.group(num)) + \
                response[end:]
        return self._eval(response)

    def respond(self, str):
        """
        Generate a response to the user input.

        :type str: str
        :param str: The string to be mapped
        :rtype: str
        """

        # check each pattern
        for (pattern, response) in self._pairs:
            match = pattern.match(str)

            # did the pattern match?
            if match:
                resp = random.choice(response)    # pick a random response
                resp = self._wildcards(resp, match) # process wildcards

                # fix munged punctuation at the end
                if resp[-2:] == '?.': resp = resp[:-2] + '.'
                if resp[-2:] == '??': resp = resp[:-2] + '?'
                return resp

    # Hold a conversation with a chatbot

    def converse(self, quit="quit"):
        input = ""
        while input != quit:
            input = quit
            try: input = compat.raw_input(">")
            except EOFError:
                print(input)
            if input:
                while input[-1] in "!.": input = input[:-1]
                print(self.respond(input))


