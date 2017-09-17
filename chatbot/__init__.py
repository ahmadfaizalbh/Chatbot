import re,random,requests,json
from os import path
from .DefaultSubs import *
try:
  from urllib import quote
except ImportError as e:
  from urllib.parse import quote
  
  
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


class multiFunctionCall:

    def __init__(self,func={}):
        self.__func__ = func
        
    def defaultfunc(self,string,sessionID ="general"):
        return string

    def call(self,string,sessionID):
        s = string.split(":")
        if len(s)<=1:
            return string
        name = s[0].strip()
        s = ":".join(s[1:])
        func = self.defaultfunc
        try:func = self.__func__[name]
        except:s = string
        return re.sub(r'\\([\[\]{}%:])',r"\1",func(re.sub(r'([\[\]{}%:])',r"\\\1",s),sessionID =sessionID))

class dummyMatch:
    def __init__(self,string):
        self.string = string

    def group(self,index):
        if index==0:return self.string
        raise IndexError("no such group")

    def groupdict(self,*arg,**karg):
        return {}

class Topic:
    def __init__(self,topics):
        self.topic={"general":''}
        self.topics = topics
    
    def __setitem__(self,key,value):
        value = value.strip()
        if value[0]==".":
            index=1
            current_topic = self.topic[key].split(".")
            while value[index]==".":
                index+=1
                current_topic.pop()
            current_topic.append(value[index:])
            value = ".".join(current_topic)
        self.topic[key]=value
        
    def __getitem__(self,key):
        topic = self.topic[key]
        if topic in self.topics():
            return topic
        return ''

class Chat(object):
    def __init__(self, pairs=(), reflections=reflections, call=multiFunctionCall(), api={}, normalizer=defaultNormal,default_template=path.join(path.dirname(path.abspath(__file__)),"default.template")):
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
        self.__init__handler()
        defaultpairs = self.__processTemplateFile(default_template)
        try:
            if type(pairs) in (str,unicode):pairs = self.__processTemplateFile(pairs)
        except NameError as e:
            if type(pairs) == str:pairs = self.__processTemplateFile(pairs)
        self._pairs = {'':{"pairs":[],"defaults":[]}} 
        if type(pairs)==dict:
            if not '' in pairs:
                raise KeyError("Default topic missing")   
        else:
            pairs = {'':{"pairs":pairs,"defaults":[]}}
        self._normalizer = dict(normalizer)
        for key in normalizer:
            self._normalizer[key.lower()] = normalizer[key]
        self._normalizer_regex = self._compile_reflections(normalizer)
        self.__processLearn(defaultpairs)
        self.__processLearn(pairs)
        self._reflections = reflections
        self._regex = self._compile_reflections(reflections)
        self._memory = {"general":{}}
        self.conversation = {"general":[]}
        self.sessionID = "general"
        self.attr = {"general":{"match":None,"pmatch":None,"_quote":False,"substitute":True}}
        self.call = call
        self.topic = Topic(self._pairs.keys)
        try:self._api = api if type(api)==dict else json.load(api)
        except:raise SyntaxError("Invalid value for api")

    def __init__handler(self):
        """
        initialize handlers and operator functionality
        """
        self.__action_handlers = {"chat":self.__chat_handler,
                          "low":self.__low_handler,
                          "up":self.__up_handler,
                          "cap":self.__cap_handler,
                          "call":self.__call_handler,
                          "topic":self.__topic_handler,
                          "map":self.__map_handler,
                          "eval":self.__eval_handler,
            }
        self.__confitional_operator = {
                "!=":lambda a,b:a!=b,
                ">=":lambda a,b:a>=b,
                "<=":lambda a,b:a<=b,
                "==":lambda a,b:a==b,
                "<":lambda a,b:a<b,
                ">":lambda a,b:a>b
            }
        self.__logical_operator ={
                '&':lambda a,b:a and b,
                '|':lambda a,b:a or b,
                '^':lambda a,b:a ^ b
            }
        

    def __normalize(self,text):
        """
        Substitute words in the string, according to the specified Normal,
        e.g. "I'm" -> "I am"

        :type str: str
        :param str: The string to be mapped
        :rtype: str
        """
        return self._normalizer_regex.sub(lambda mo:
                self._normalizer[mo.string[mo.start():mo.end()]],
                    text.lower())

    def __errorMessage(self,expected,found):
        return "Expected '%s' tag found '%s'" % (expected,found)

    def __responseTags(self,text,pos,index):
        next_index=index+1
        if pos[next_index][2]!="endresponse":
            raise SyntaxError(self.__errorMessage("endresponse",pos[next_index][2]))
        return text[pos[index][1]:pos[next_index][0]].strip(" \t\n")
              
    def __blockTags(self,text,pos,length,index):
        withinblock = {"learn":{},"response":[],"client":[],"prev":[]}
        while pos[index][2]!="endblock":
            if pos[index][2]=="learn":
                withinblock["learn"]={}
                index = self.__GroupTags(text,pos,withinblock["learn"],(lambda i:pos[i][2]!="endlearn"),length,index+1)
            elif pos[index][2]=="response":
                withinblock["response"].append(self.__responseTags(text,pos,index))
                index+=1
            elif pos[index][2]=="client":
                index+=1
                if pos[index][2]!="endclient":
                    raise SyntaxError(self.__errorMessage("endclient",pos[index][2]))
                withinblock["client"].append(text[pos[index-1][1]:pos[index][0]].strip(" \t\n"))
            elif pos[index][2]=="prev":
                index+=1
                if pos[index][2]!="endprev":
                    raise SyntaxError(self.__errorMessage("endprev",pos[index][2]))
                withinblock["prev"].append(text[pos[index-1][1]:pos[index][0]].strip(" \t\n"))
            else:
                raise NameError("Invalid Tag '%s'" %  pos[index][2])
            index+=1
        return index+1,(withinblock["client"][0],
                    withinblock["prev"][0] if withinblock["prev"] else None,
                    withinblock["response"],
                    withinblock["learn"] )
    
    def __GroupTags(self,text,pos,groups,condition,length,index=0,name=""):
        pairs=[]
        defaults=[]
        while condition(index):
            if pos[index][2]=="block":
                p,within = self.__blockTags(text,pos,length,index+1)
                pairs.append(within)
                index=p
            elif pos[index][2]=="response":
                defaults.append(self.__responseTags(text,pos,index))
                index+=2
            elif pos[index][2]=="group":
                index = self.__GroupTags(text,pos,groups,(lambda i:pos[i][2]!="endgroup"),length,index+1, name=name+"."+pos[index][3].strip())
            else:
                raise SyntaxError(self.__errorMessage('group, block, or response',pos[index][2]))
        if name in groups:
            groups[name]["pairs"].extend(pairs)
            groups[name]["defaults"].extend(defaults)
        else:
            groups[name]={"pairs":pairs,"defaults":defaults}
        return index+1
        
    def __processTemplateFile(self,fileName):
        with open(fileName) as template:
            text = template.read()
        pos = [(m.start(0),m.end(0),text[m.start(1):m.end(1)],text[m.start(4):m.end(4)]) \
                for m in  re.finditer( 
                    r'{%[\s\t]+((end)?(block|learn|response|client|prev|group))[\s\t]+([^%]*|%(?=[^}]))%}',
                    text)
              ]
        length = len(pos)
        groups = {}
        self.__GroupTags(text,pos,groups,(lambda i:i<length),length)
        return groups
        
    def __processLearn(self,pairs):
        for topic in pairs:
            if topic not in self._pairs:
                self._pairs[topic]={"pairs":[],"defaults":[]}
            self._pairs[topic]["defaults"].extend([(i,self._condition(i)) for i in pairs[topic].get("defaults",[])])
            for p in pairs[topic]["pairs"][::-1]:
                l={}
                y = None
                if len(p)<2:
                    raise ValueError("Response not specified")
                elif len(p)==2:
                    if type(p[1]) not in (tuple,list):
                        raise ValueError("Response not specified")
                    x,z = p
                elif len(p)==3:
                    if type(p[1]) not in (tuple,list):
                       x,y,z = p
                    else:
                        x,z,l = p
                else:
                    x,y,z,l = p[:4]
                if type(l) != dict:
                    raise TypeError("Invalid Type for learn expected dict got '%s'" % type(l).__name__)
                z=tuple((i,self._condition(i)) for i in z)
                if y:
                    self._pairs[topic]["pairs"].insert(0,(re.compile(self.__normalize(x), re.IGNORECASE),re.compile(self.__normalize(y), re.IGNORECASE),z,l))
                else:
                    self._pairs[topic]["pairs"].insert(0,(re.compile(x, re.IGNORECASE),y,z,l))
        
    
    def _startNewSession(self,sessionID):
        self._memory[sessionID]={}
        self.conversation[sessionID]=[]
        self.attr[sessionID]={"match":None,"pmatch":None,"_quote":False,"substitute":True}
        self.topic[sessionID] = ''

    def _restructure(self,group,index=None):
        if index==None:
            toremove={}
            allElem = list(group)
            for i in group:
                toremove[i]=set()
                for j in group[i]:
                    toremove[i].update(set(group[i]).intersection(group[j]))
            for i in group:
                for j in toremove[i]:
                    group[i].remove(j)
                    try: allElem.remove(j)
                    except: pass
            index = list(group)
            toremove = [j for i in list(allElem) for j in group[i]]
            for i in toremove:
                try: allElem.remove(i)
                except: pass
        else:
            allElem = list(index)
        while index:
            i = index.pop()
            if type(group[i])==list:
                group[i] = self._restructure(dict(group),group[i])
                for j in list(group[i]):
                    try: index.remove(j)
                    except: pass
        return {i:group[i] for i in allElem}
        
    def _subAction(self,group,start_end_pair,action):
        return {i:{
                    "action":action[i],
                    "start":start_end_pair[i][0],
                    "end":start_end_pair[i][1],
                    "child":self._subAction(group[i],start_end_pair,action)
                  } for i in group}
    
    def _getWithin(self,group,index):

        
        def init_group(i):
            group[index[i]]["within"]=[]
            orderedGroup.append(group[index[i]])
            return i+1

        def append_group(pos,i):
            pos,within = self._getWithin(group,index[pos:])
            group[index[i-1]]["within"]+=within
            return pos

        i = 0
        orderedGroup = []
        while i<len(index):
            if group[index[i]]["action"]=="if":
                i=init_group(i)
                startIF = True 
                while startIF:
                    if i>=len(index):
                        raise SyntaxError("If not closed in Conditional statement")
                    if group[index[i]]["action"]=="elif": i = init_group(i)
                    elif group[index[i]]["action"]=="else":
                        pos = i = init_group(i)
                        startIF = False
                        while group[index[pos]]["action"]!="endif": pos = append_group(pos,i)+i
                        i = init_group(pos)
                    elif group[index[i]]["action"]=="endif":
                        i = init_group(i)
                        startIF = False
                    else:
                        pos = append_group(i,i)
                        for j in range(i,pos): del group[index[j]]
                        i += pos
            elif group[index[i]]["action"] in self.__action_handlers .keys():
                orderedGroup.append(group[index[i]])
                i += 1
            else:return i,orderedGroup
        return i,orderedGroup
                
    def _setwithin(self,group):
        old =group
        for i in group:
            if group[i]["child"]:
                group[i]["child"] = self._setwithin(group[i]["child"])
        index = list(group)
        index.sort(key =lambda x: group[x]["start"])
        pos,orderedGroup = self._getWithin(group,index)
        if pos<len(index):
            raise SyntaxError("invalid statement")
        return orderedGroup
    
    def _inherit(self,start_end_pair,action):
        group = {}
        for i in range(len(start_end_pair)):
            group[i] = []
            for j in range(len(start_end_pair)):
                if start_end_pair[i][0]<start_end_pair[j][0] and start_end_pair[i][1]>start_end_pair[j][1]:
                    group[i].append(j)
        group = self._restructure(group)
        group = self._subAction(group,start_end_pair,action)
        return self._setwithin(group)

    def _condition(self,response):
        pos = [(m.start(0),m.end(0)) for m in re.finditer(r'{%?|%?}|\[|\]', response)]
        newPos = [(start,end) for start,end in pos if (not start) or response[start-1]!="\\" ]
        i=0
        start_end_pair = []
        actions = []
        while newPos:
            for i in range(1,len(newPos)):
                if response[newPos[i][1]-1] in "}]":
                    break
            if response[newPos[i-1][0]] in "{[":
                endTag = newPos.pop(i)
                biginTag = newPos.pop(i-1)
                bN = biginTag[1]-biginTag[0]
                eN = endTag[1]-endTag[0]
                if bN != eN or not ((response[biginTag[0]] == "{" and response[endTag[1]-1] == "}") or (response[biginTag[0]] == "[" and response[endTag[1]-1] == "]")):
                    raise SyntaxError("invalid syntax '%s'" % response)
                start_end_pair.append((biginTag[1],endTag[0]))
                if bN == 2:
                    statement = re.findall( r'^[\s\t]*(if|endif|elif|else|chat|low|up|cap|call|topic)[\s\t]+',
                                            response[biginTag[1]:endTag[0]])
                    if statement:
                        actions.append(statement[0])
                    else:
                        raise SyntaxError("invalid statement '%s'" % response[biginTag[1]:endTag[0]] )
                else:
                    if response[biginTag[0]] == "{":
                        actions.append("map")
                    else:
                        actions.append("eval")
            else:
                raise SyntaxError("invalid syntax in \"%s\"" % response)
        try:
            group = self._inherit(start_end_pair,actions)
        except SyntaxError:
            raise SyntaxError("invalid statement in \"%s\"" % response)
        return group
    
    def _compile_reflections(self,normal):
        sorted_refl = sorted(normal.keys(), key=len, reverse=True)
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
        if not self.attr.get("substitute",True):return str
        return self._regex.sub(lambda mo:
                self._reflections[mo.string[mo.start():mo.end()]],
                    str.lower())
    
    def _checkIF(self,con,sessionID = "general"):
        pos = [(m.start(0),m.end(0),m.group(0)) for m in re.finditer(r'([\<\>!=]=|[\<\>]|&|\|)', con)]
        if not pos:return con.strip()
        res = prevres = True
        prevO = None
        pcsymbol = "&"
        A = con[0:pos[0][0]].strip()
        for j in  range(len(pos)):
            s,e,o = pos[j]
            try:B = con[e:pos[j+1][0]].strip()
            except:B = con[e:].strip()
            try:a,b = float(A),float(b)
            except:a,b = A,B
            try:res = self.__confitional_operator[o](a,b) and res
            except:
                try:prevres,res = self.__logical_operator[pcsymbol](prevres,res),True
                except:SyntaxError("invalid conditional operator \"%s\"" % pcsymbol)
                pcsymbol = o
            A = B
        return self.__logical_operator[pcsymbol](prevres,res)
    
    def __if_handler(self,i,condition,response,sessionID):
        start = self.__get_start_pos(condition[i]["start"],response,"if")
        end = condition[i]["end"]
        check = True
        matchedIndex = None
        _quote = self.attr[sessionID]["_quote"]
        self.attr[sessionID]["_quote"] = False
        substitute = self.attr.get("substitute",True)
        self.attr["substitute"] = False
        while check:
            con = self._checkAndEvaluateCondition(response,condition[i]["child"],start,end,sessionID =sessionID)
            i+=1
            if self._checkIF(con,sessionID =sessionID):
                matchedIndex = i-1
                while condition[i]["action"] != "endif":
                    i+=1
                check = False
            elif condition[i]["action"] == "else":
                matchedIndex = i
                while condition[i]["action"] != "endif":
                    i+=1
                check = False                        
            elif condition[i]["action"] == "elif":
                start = self.__get_start_pos(condition[i]["start"],response,"elif")
                end = condition[i]["end"]
            elif condition[i]["action"] == "endif":
                check = False
        self.attr[sessionID]["_quote"] = _quote
        self.attr["substitute"] = substitute
        return ((self._checkAndEvaluateCondition(
                                response,
                                condition[matchedIndex]["within"],
                                condition[matchedIndex]["end"]+2,
                                condition[matchedIndex+1]["start"]-2,
                                sessionID =sessionID
                                ) if matchedIndex!=None else ""),i)
    
    def __handler(self,condition,response,action,sessionID):
        return self._checkAndEvaluateCondition(
                                response,
                                condition["child"],
                                self.__get_start_pos(condition["start"],response,action),
                                condition["end"],
                                sessionID =sessionID
                                )
    
    def __chat_handler(self,i,condition,response,sessionID):
        substitute = self.attr.get("substitute",True)
        self.attr["substitute"] = False
        response = self.respond(self.__handler(condition[i],response,"chat",sessionID),sessionID =sessionID)
        self.attr["substitute"] = substitute
        return response
    
    def __low_handler(self,i,condition,response,sessionID):
        return self.__handler(condition[i],response,"low",sessionID).lower()
        
    def __up_handler(self,i,condition,response,sessionID):
        return self.__handler(condition[i],response,"up",sessionID).upper()
        
    def __cap_handler(self,i,condition,response,sessionID):
        return self.__handler(condition[i],response,"cap",sessionID).capitalize()
    
    def __call_handler(self,i,condition,response,sessionID):
        return self.call.call(self.__handler(condition[i],response,"call",sessionID),sessionID =sessionID)
    
    def __topic_handler(self,i,condition,response,sessionID):
        self.topic[sessionID] = self.__handler(condition[i],response,"topic",sessionID).strip()
        return ""
        
    def __get_start_pos(self,start,response,exp):
        return start+re.compile(r"([\s\t]*"+exp+"[\s\t]+)").search(response[start:]).end(1)

    def __map_handler(self,i,condition,response,sessionID):
        start = condition[i]["start"]
        end = condition[i]["end"]
        think = False
        if response[start] == "!":
            think = True
            start +=1
        content = self._checkAndEvaluateCondition(
                                    response,
                                    condition[i]["child"],
                                    start,
                                    end,
                                    sessionID =sessionID
                                    ).strip().split(":")
        name = content[0]
        thisIndex=0
        for thisIndex in range(1,len(content)):
            if name[-1]=="\\":
                name += ":"+content[thisIndex]
            else:
                thisIndex-=1
                break
        thisIndex+=1
        name = name.strip().lower()
        if thisIndex<(len(content)):
            value = content[thisIndex]
            for thisIndex in range(thisIndex+1,len(content)):
                if value[-1]=="\\":
                    value += ":"+content[thisIndex]
                else:
                    break
            self._memory[sessionID][name] = self._substitute(value.strip())
        return self._memory[sessionID][name] if not think and name in self._memory[sessionID] else ""
    
    def __eval_handler(self,i,condition,restopnse,sessionID):
        start = condition[i]["start"]
        end = condition[i]["end"]
        think = False
        if response[start] == "!":
            think = True
            start +=1
        _quote = self.attr[sessionID]["_quote"]
        self.attr[sessionID]["_quote"] = True
        content = self._checkAndEvaluateCondition(
                                    response,
                                    condition[i]["child"],
                                    start,
                                    end,
                                    sessionID =sessionID
                                    ).strip()
        self.attr[sessionID]["_quote"] = _quote
        vals = content.split(",")
        names = vals[0].split(":")
        apiName = names[0]
        methodName = ":".join(names[1:])
        data={}
        key=None
        for i in vals[1:]:
            pair = vals[i].split(":")
            if len(pair)>=2:
                key = pair[0]
                data[key]=":".join(pair[1:])
            elif key!=None:
                data[key]+=","+pair[0]
            else:raise SyntaxError("invalid syntax '%s'" % response[start:end] )
        result = self.__api_handler(apiName,methodName,data)
        return "" if think else result
        
    def __api_request(self,url,method,**karg):
        try:return requests.__dict__[method.lower().strip()](url,**karg)
        except requests.exceptions.MissingSchema as e:
            return self.__api_request("http://"+url,method,**karg)
        except requests.exceptions.ConnectionError as e:
            raise RuntimeError("Couldn't connect to server (unreachable). Check your network")
        except KeyError as e:
            raise RuntimeError("Invalid method name '%s' in api.json" % method)
    
    def __api_handler(self,apiName,methodName,data={}):
        if apiName not in self._api or methodName not in self._api[apiName]:
            raise RuntimeError("Invalid method name '%s' for api '%s' ",(methodName,apiName))
        api_params = dict(self._api[apiName][methodName])
        if "auth" in self._api[apiName]:
            try:api_params["cookies"] = self.__api_request(**self._api[apiName]["auth"]).cookies
            except:raise ValueError("In api.json 'auth' of '%s' is wrongly configured." % apiName)
        param = "params" if self._api[apiName][methodName]["method"].upper().strip() == "GET" else "data"
        try:api_params[param].update(data)
        except:api_params[param] = data
        api_type = "normal"
        if "type" in api_params:
            api_type = api_params["type"]
            del api_params["type"]
        api_data_getter = []
        if "value_getter" in api_params:
            api_data_getter = api_params["value_getter"]
            del api_params["value_getter"]
        response = self.__api_request(**api_params)
        responseText = response.json() if api_type.upper().strip()=="JSON" else response.content
        for key in api_data_getter:
            responseText = responseText[key]
        return responseText
    
    def _quote(self,string,sessionID):
        if self.attr[sessionID]["_quote"]:
            try:return urllib2.quote(string)
            except:return urllib2.quote(string.encode("UTF-8"))
        return string

    def __substituteFromClientStatement(self,match,prevResponse,extraSymbol="",sessionID = "general"):
        """
        Substitute from Client statement into respose
        """
        prev = 0
        startPadding = 1+len(extraSymbol)
        finalResponse = ""
        for m in re.finditer(r'%'+extraSymbol+'[0-9]+', prevResponse):
            start = m.start(0)
            end = m.end(0)     
            num = int(prevResponse[start+startPadding:end])
            finalResponse += prevResponse[prev:start]
            try:finalResponse += self._quote(self._substitute(match.group(num)),sessionID)
            except IndexError as e:pass
            prev = end
        namedGroup = match.groupdict()
        if namedGroup:
            prevResponse = finalResponse + prevResponse[prev:]
            finalResponse = ""
            prev = 0
            for m in re.finditer(r'%'+extraSymbol+'([a-zA-Z_][a-zA-Z_0-9]*)([^a-zA-Z_0-9]|$)', prevResponse):
                start = m.start(1)
                end = m.end(1)
                finalResponse += prevResponse[prev:start]
                try:
                    value = namedGroup[prevResponse[start+startPadding:end]]
                    if value:finalResponse += self._quote(self._substitute(value),sessionID)
                except KeyError as e:pass
                prev = end
        return finalResponse + prevResponse[prev:]
    
    def _checkAndEvaluateCondition(self, response,condition=[],startIndex=0,endIndex=None,sessionID = "general"):
        endIndex = endIndex if endIndex != None else len(response)
        if not condition:
            finalResponse = self.__substituteFromClientStatement(self.attr[sessionID]["match"],response[startIndex:endIndex],sessionID = sessionID)
            parentMatch=self.attr[sessionID]["pmatch"]
            return self.__substituteFromClientStatement(parentMatch,finalResponse,extraSymbol = '!',sessionID = sessionID) if parentMatch!=None else finalResponse
        i=0
        finalResponse = ""
        while i < len(condition):
            pos =  condition[i]["start"]-(1 if condition[i]["action"] in  ["map","eval"] else 2) 
            finalResponse += self._checkAndEvaluateCondition(response[startIndex:pos],sessionID =sessionID)
            _quote = self.attr[sessionID]["_quote"]
            try:
                self.attr[sessionID]["_quote"] = False
                tempResponse = self.__action_handlers[condition[i]["action"]](i,condition,response,sessionID)
                self.attr[sessionID]["_quote"] = _quote
                finalResponse += self._quote(tempResponse,sessionID)
            except KeyError as e:
                if condition[i]["action"] == "if":
                    self.attr[sessionID]["_quote"] = _quote
                    response_txt,i = self.__if_handler(i,condition,response,sessionID)
                    finalResponse += response_txt
            startIndex = condition[i]["end"]+(1 if condition[i]["action"] in  ["map","eval"] else 2) 
            i+=1
        self.attr[sessionID]["_quote"] = _quote
        finalResponse += self._checkAndEvaluateCondition(response[startIndex:endIndex],sessionID = sessionID)
        return finalResponse
    
    def _wildcards(self, response, match, parentMatch,sessionID = "general"):
        self.attr[sessionID]["match"]=match
        self.attr[sessionID]["pmatch"]=parentMatch
        response,condition =  response
        return re.sub(r'\\([\[\]{}%:])',r"\1",self._checkAndEvaluateCondition(response,condition,sessionID = sessionID ))

    def __response_on_topic(self, text, previousText, current_topic, sessionID = "general"):
      for (pattern, parent, response,learn) in self._pairs[current_topic]["pairs"]:# check each pattern
            match = pattern.match(text)
            parentMatch = parent.match(previousText) if parent!=None else True
            # did the pattern match?
            if parentMatch and match:
                parentMatch = None if parentMatch==True else parentMatch
                resp = random.choice(response)    # pick a random response
                resp = self._wildcards(resp, match, parentMatch,sessionID = sessionID) # process wildcards
                # fix munged punctuation at the end
                if resp[-2:] == '?.': resp = resp[:-2] + '.'
                if resp[-2:] == '??': resp = resp[:-2] + '?'
                if learn:
                    learn = {
                        self._wildcards((topic,self._condition(topic)), match, parentMatch,sessionID = sessionID): \
                        tuple(self.__substituteInLearn(pair, match, parentMatch,sessionID = sessionID)  for pair in learn[topic]) \
                        for topic in learn}
                    self.__processLearn(learn)
                return resp
      if self._pairs[current_topic]["defaults"]:
        resp = self._wildcards(random.choice(self._pairs[current_topic]["defaults"]),
                               dummyMatch(match), None, sessionID = sessionID)
        if resp[-2:] == '?.': resp = resp[:-2] + '.'
        if resp[-2:] == '??': resp = resp[:-2] + '?'
        return resp
      raise ValueError("No match found")
      
    def respond(self, text, sessionID = "general"):
        """
        Generate a response to the user input.

        :type text: str
        :param text: The string to be mapped
        :rtype: str
        """
        text =  self.__normalize(text)
        previousText = self.__normalize(self.conversation[sessionID][-2])
        current_topic = self.topic[sessionID]
        current_topic_order = current_topic.split(".")
        while current_topic_order:
          try:return self.__response_on_topic(text, previousText, current_topic, sessionID)
          except ValueError as e:pass
          current_topic_order.pop()
          current_topic = ".".join(current_topic_order) # process wildcards

        
                
    def __substituteInLearn(self,pair, match, parentMatch,sessionID = "general"):
        return tuple((self.__substituteInLearn(i, match, parentMatch,sessionID = sessionID) if type(i) in (tuple,list) else \
            (i if type(i) == dict else (self._wildcards((i,self._condition(i)), match, parentMatch,sessionID = sessionID) if i else i))) for i in pair)
  
    def save_template(self,filename):
        with open(filename,"w") as template:
            self.__genrate_and_wrie_template(template,self._pairs)

    def __genrate_and_wrie_template(self,template,pairs):
        for topic in self._pairs:
            template.write("{% group "+topic+" %}")
            for (pattern, parent, response,learn) in pairs[topic]:
                template.write("{% block %}")
                template.write("{% client %}"+pattern.pattern+"{% endclient %}")
                if parent!=None:
                    template.write("{% prev %}"+parent.pattern+"{% endprev %}")
                for res in response:
                    template.write("{% response %}"+res[0]+"{% response %}")
                if learn:
                    template.write("{% learn %}")
                    self.__genrate_and_wrie_template(template,learn)
                    template.write("{% endlearn %}")
                template.write("{% endblock %}")
            template.write("{% endgroup %}")
                        
    # Hold a conversation with a chatbot                                       
    def converse(self,firstQuestion=None ,quit="quit",sessionID = "general"):
        if firstQuestion!= None:
            self.conversation[sessionID].append(firstQuestion)
            print (firstQuestion)
        try:input_reader = raw_input
        except NameError:input_reader = input
        input_sentence = ""
        while input_sentence != quit:
            input_sentence = quit
            try: input_sentence = input_reader(">")
            except EOFError:print (input_sentence)
            if input_sentence:
                self.conversation[sessionID].append(input_sentence)
                while input_sentence[-1] in "!.": input_sentence = input_sentence[:-1]
                self.conversation[sessionID].append(self.respond(input_sentence,sessionID=sessionID))
                print (self.conversation[sessionID][-1])


def demo():
    firstQuestion="Hi, how are you?"
    Chat().converse(firstQuestion)

