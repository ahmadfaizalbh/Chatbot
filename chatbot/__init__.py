import re
import random
import requests
import json
from os import path
from . import substitutions
from .spellcheck import correction
try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote

try:
    input_reader = raw_input
except NameError:
    input_reader = input
    
    
class MultiFunctionCall:

    def __init__(self, func={}):
        self.__func__ = func

    @staticmethod
    def default_func(string, session_id="general"):
        return string

    def call(self, string, session_id):
        s = string.split(":")
        if len(s) <= 1:
            return string
        name = s[0].strip()
        s = ":".join(s[1:])
        func = self.default_func
        try:
            func = self.__func__[name]
        except KeyError:
            s = string
        new_string = re.sub(r'([\[\]{}%:])', r"\\\1", s)
        return re.sub(r'\\([\[\]{}%:])', r"\1", func(new_string, session_id=session_id))


_function_call = MultiFunctionCall()


def register_call(function_name):
    def wrap(function):
        if type(function).__name__ != 'function':
            raise TypeError("function expected found %s" % type(function).__name__)
        mapper = _function_call.__func__
        if name in mapper:
            raise ValueError("function with same name is already registered")
        mapper[name] = function
        return function

    if type(function_name).__name__ in ('unicode', 'str'):
        name = function_name
        return wrap
    name = function.__name__
    return wrap(function_name)


class DummyMatch:

    def __init__(self, string):
        self.string = string

    def group(self, index):
        if index == 0:
            return self.string
        raise IndexError("no such group")

    @staticmethod
    def groupdict(*arg, **karg):
        return {}


class Topic:

    def __init__(self, topics):
        self.topic = {"general": ''}
        self.topics = topics

    def __setitem__(self, key, value):
        value = value.strip()
        if value and value[0] == ".":
            index = 1
            current_topic = self.topic[key].split(".")
            while value[index] == ".":
                index += 1
                current_topic.pop()
            current_topic.append(value[index:])
            value = ".".join(current_topic)
        self.topic[key] = value

    def __getitem__(self, key):
        topic = self.topic[key]
        if topic in self.topics():
            return topic
        return ''


class Chat(object):
    def __init__(self, pairs=(), reflections=substitutions.reflections, call=_function_call,
                 api={}, normalizer=substitutions.normal, default_template=None, language="en"):
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
        :type call: MultiFunctionCall
        :param call: A mapping between user defined function and template function call name
        :rtype: None
        """
        self.__init__handler()
        if default_template is None:
            default_template = path.join(path.dirname(path.abspath(__file__)), "local", language+".template")
        default_pairs = self.__process_template_file(default_template)
        if type(pairs).__name__ in ('unicode', 'str'):
            pairs = self.__process_template_file(pairs)
        self._pairs = {'': {"pairs": [], "defaults": []}}
        if type(pairs) != dict:
            pairs = {'': {"pairs": pairs, "defaults": []}}
        elif '' not in pairs:
            raise KeyError("Default topic missing")
        self._normalizer = dict(normalizer)
        for key in normalizer:
            self._normalizer[key.lower()] = normalizer[key]
        self._normalizer_regex = self._compile_reflections(normalizer)
        self.__process_learn(default_pairs)
        self.__process_learn(pairs)
        self._reflections = reflections
        self._regex = self._compile_reflections(reflections)
        self._memory = {"general": {}}
        self.conversation = {"general": []}
        self.session_id = "general"
        self.attr = {"general": {"match": None, "pmatch": None, "_quote": False, "substitute": True}}
        self.call = call
        self.topic = Topic(self._pairs.keys)
        try:
            self._api = api if type(api) == dict else json.load(api)
        except Exception:
            raise SyntaxError("Invalid value for api")

    def __init__handler(self):
        """
        initialize handlers and operator functionality
        """
        self.__action_handlers = {
            "chat": self.__chat_handler,
            "low": self.__low_handler,
            "up": self.__up_handler,
            "cap": self.__cap_handler,
            "call": self.__call_handler,
            "topic": self.__topic_handler,
            "map": self.__map_handler,
            "eval": self.__eval_handler,
            }
        self.__conditional_operator = {
                "!=": lambda a, b: a != b,
                ">=": lambda a, b: a >= b,
                "<=": lambda a, b: a <= b,
                "==": lambda a, b: a == b,
                "<": lambda a, b: a < b,
                ">": lambda a, b: a > b
            }
        self.__logical_operator = {
                '&': lambda a, b: a and b,
                '|': lambda a, b: a or b,
                '^': lambda a, b: a ^ b
            }

    def __normalize(self, text):
        """
        Substitute words in the string, according to the specified Normal,
        e.g. "I'm" -> "I am"

        :type text: str
        :param text: The string to be normalized
        :rtype: str
        """
        return self._normalizer_regex.sub(lambda mo: self._normalizer[mo.string[mo.start():mo.end()].lower()], text)

    @staticmethod
    def __error_message(expected, found):
        return "Expected '%s' tag found '%s'" % (expected, found)

    def __response_tags(self, text, pos, index):
        next_index = index+1
        if pos[next_index][2] != "endresponse":
            raise SyntaxError(self.__error_message("endresponse", pos[next_index][2]))
        return text[pos[index][1]:pos[next_index][0]].strip(" \t\n")

    def __block_tags(self, text, pos, length, index):
        within_block = {"learn": {}, "response": [], "client": [], "prev": []}
        while pos[index][2] != "endblock":
            if pos[index][2] == "learn":
                within_block["learn"] = {}
                index = self.__group_tags(text, pos, within_block["learn"],
                                          (lambda i: pos[i][2] != "endlearn"), length, index+1)
                index -= 1
            elif pos[index][2] == "response":
                within_block["response"].append(self.__response_tags(text, pos, index))
                index += 1
            elif pos[index][2] == "client":
                index += 1
                if pos[index][2] != "endclient":
                    raise SyntaxError(self.__error_message("endclient", pos[index][2]))
                within_block["client"].append(text[pos[index-1][1]:pos[index][0]].strip(" \t\n"))
            elif pos[index][2] == "prev":
                index += 1
                if pos[index][2] != "endprev":
                    raise SyntaxError(self.__error_message("endprev", pos[index][2]))
                within_block["prev"].append(text[pos[index-1][1]:pos[index][0]].strip(" \t\n"))
            else:
                raise NameError("Invalid Tag '%s'" % pos[index][2])
            index += 1
        return index+1, (within_block["client"],
                         within_block["prev"] if within_block["prev"] else None,
                         within_block["response"],
                         within_block["learn"])

    def __group_tags(self, text, pos, groups, condition, length, index=0, name=""):
        pairs = []
        defaults = []
        while condition(index):
            if pos[index][2] == "block":
                p, within = self.__block_tags(text, pos, length, index+1)
                pairs.append(within)
                index = p
            elif pos[index][2] == "response":
                defaults.append(self.__response_tags(text, pos, index))
                index += 2
            elif pos[index][2] == "group":
                child_name = (name+"."+pos[index][3].strip()) if name else pos[index][3].strip()
                index = self.__group_tags(text, pos, groups,
                                          (lambda i: pos[i][2] != "endgroup"), length, index+1, name=child_name)
            else:
                raise SyntaxError(self.__error_message('group, block, or response', pos[index][2]))
        if name in groups:
            groups[name]["pairs"].extend(pairs)
            groups[name]["defaults"].extend(defaults)
        else:
            groups[name] = {"pairs": pairs, "defaults": defaults}
        return index+1

    def __process_template_file(self, file_name):
        with open(file_name, encoding='utf-8') as template:
            text = template.read()
        pos = [(m.start(0), m.end(0), text[m.start(1):m.end(1)], text[m.start(4):m.end(4)])
               for m in re.finditer(
                    r'{%[\s\t]+((end)?(block|learn|response|client|prev|group))[\s\t]+([^%]*|%(?=[^}]))%}',
                    text)
               ]
        length = len(pos)
        groups = {}
        self.__group_tags(text, pos, groups, (lambda i: i < length), length)
        return groups

    def __build_pattern(self, patterns):
        if patterns is None:
            return
        if type(patterns).__name__ in ('unicode', 'str'):
            patterns = [patterns]
        regexps = []
        for pattern in patterns:
            try:
                regexps.append(re.compile(self.__normalize(pattern), re.IGNORECASE))
            except Exception as e:
                e.args = (str(e) + " in pattern "+pattern, )
                raise e
        return regexps

    def __process_learn(self, pairs):
        for topic in pairs:
            if topic not in self._pairs:
                self._pairs[topic] = {"pairs": [], "defaults": []}
            self._pairs[topic]["defaults"].extend([(i, self._condition(i))
                                                   for i in pairs[topic].get("defaults", [])])
            for pair in pairs[topic]["pairs"][::-1]:
                learn, previous = {}, None
                length = len(pair)
                if length > 3:
                    client, previous, responses, learn = pair[:4]
                elif length == 3:
                    if type(pair[1]) in (tuple, list):
                        client, responses, learn = pair
                    else:
                        client, previous, responses = pair
                elif length == 2 and type(pair[1]) in (tuple, list):
                    client, responses = pair
                else:
                    raise ValueError("Response not specified")
                if type(learn) != dict:
                    raise TypeError("Invalid Type for learn expected dict got '%s'" % type(learn).__name__)
                if not client:
                    raise ValueError("Each block should contain at least 1 client regex")
                self._pairs[topic]["pairs"].insert(0, (self.__build_pattern(client),
                                                       self.__build_pattern(previous),
                                                       tuple((i, self._condition(i)) for i in responses),
                                                       learn))

    def start_new_session(self, session_id, topic=''):
        self._memory[session_id] = {}
        self.conversation[session_id] = []
        self.attr[session_id] = {"match": None, "pmatch": None, "_quote": False, "substitute": True}
        self.topic[session_id] = topic

    def _restructure(self, group, index=None):
        if index is None:
            to_remove = {}
            groups = list(group)
            for i in group:
                to_remove[i] = set()
                for j in group[i]:
                    to_remove[i].update(set(group[i]).intersection(group[j]))
            for i in group:
                for j in to_remove[i]:
                    group[i].remove(j)
                    try:
                        groups.remove(j)
                    except Exception:
                        pass
            index = list(group)
            to_remove = [j for i in list(groups) for j in group[i]]
            for i in to_remove:
                try:
                    groups.remove(i)
                except Exception:
                    pass
        else:
            groups = list(index)
        while index:
            i = index.pop()
            if type(group[i]) == list:
                group[i] = self._restructure(dict(group), group[i])
                for j in list(group[i]):
                    try:
                        index.remove(j)
                    except Exception:
                        pass
        return {i: group[i] for i in groups}

    def _sub_action(self, group, start_end_pair, action):
        return {i: {
                    "action": action[i],
                    "start": start_end_pair[i][0],
                    "end": start_end_pair[i][1],
                    "child": self._sub_action(group[i], start_end_pair, action)
                  } for i in group}

    def _get_within(self, group, index):

        def init_group(p):
            group[index[p]]["within"] = []
            ordered_group.append(group[index[p]])
            return p+1

        def append_group(position, p):
            position, within = self._get_within(group, index[position:])
            group[index[p-1]]["within"] += within
            return position

        i = 0
        ordered_group = []
        while i < len(index):
            if group[index[i]]["action"] == "if":
                i = init_group(i)
                start_if = True
                while start_if:
                    if i >= len(index):
                        raise SyntaxError("If not closed in Conditional statement")
                    if group[index[i]]["action"] == "elif":
                        i = init_group(i)
                    elif group[index[i]]["action"] == "else":
                        pos = i = init_group(i)
                        start_if = False
                        while group[index[pos]]["action"] != "endif":
                            pos = append_group(pos, i)+i
                        i = init_group(pos)
                    elif group[index[i]]["action"] == "endif":
                        i = init_group(i)
                        start_if = False
                    else:
                        pos = append_group(i, i)
                        for j in range(i, pos):
                            del group[index[j]]
                        i += pos
            elif group[index[i]]["action"] in self.__action_handlers.keys():
                ordered_group.append(group[index[i]])
                i += 1
            else:
                return i, ordered_group
        return i, ordered_group

    def _set_within(self, group):
        for i in group:
            group[i]["child"] = self._set_within(group[i]["child"]) if group[i]["child"] else []
        index = list(group)
        index.sort(key=lambda x: group[x]["start"])
        pos, ordered_group = self._get_within(group, index)
        if pos < len(index):
            raise SyntaxError("invalid statement")
        return ordered_group

    def _inherit(self, start_end_pair, action):
        group = {}
        for i in range(len(start_end_pair)):
            group[i] = []
            for j in range(len(start_end_pair)):
                if start_end_pair[i][0] < start_end_pair[j][0] and start_end_pair[i][1] > start_end_pair[j][1]:
                    group[i].append(j)
        group = self._restructure(group)
        group = self._sub_action(group, start_end_pair, action)
        return self._set_within(group)

    def _condition(self, response):
        pos = [(m.start(0), m.end(0)) for m in re.finditer(r'{%?|%?}|\[|\]', response)]
        new_pos = [(start, end) for start, end in pos if (not start) or response[start-1] != "\\"]
        i = 0
        start_end_pair = []
        actions = []
        while new_pos:
            for i in range(1, len(new_pos)):
                if response[new_pos[i][1]-1] in "}]":
                    break
            if response[new_pos[i-1][0]] in "{[":
                end_tag = new_pos.pop(i)
                begin_tag = new_pos.pop(i-1)
                b_n = begin_tag[1]-begin_tag[0]
                e_n = end_tag[1]-end_tag[0]
                if b_n != e_n or not ((response[begin_tag[0]] == "{" and response[end_tag[1]-1] == "}") or
                                      (response[begin_tag[0]] == "[" and response[end_tag[1]-1] == "]")):
                    raise SyntaxError("invalid syntax '%s'" % response)
                start_end_pair.append((begin_tag[1], end_tag[0]))
                if b_n == 2:
                    statement = re.findall(r'^[\s\t]*(if|endif|elif|else|chat|low|up|cap|call|topic)[\s\t]+',
                                           response[begin_tag[1]: end_tag[0]])
                    if statement:
                        actions.append(statement[0])
                    else:
                        raise SyntaxError("invalid statement '%s'" % response[begin_tag[1]:end_tag[0]])
                else:
                    if response[begin_tag[0]] == "{":
                        actions.append("map")
                    else:
                        actions.append("eval")
            else:
                raise SyntaxError("invalid syntax in \"%s\"" % response)
        try:
            group = self._inherit(start_end_pair, actions)
        except SyntaxError:
            raise SyntaxError("invalid statement in \"%s\"" % response)
        return group

    @staticmethod
    def _compile_reflections(normal):
        sorted_reflection = sorted(normal.keys(), key=len, reverse=True)
        return re.compile(r"\b({0})\b".format("|".join(map(re.escape, sorted_reflection))), re.IGNORECASE)

    def _substitute(self, str):
        """
        Substitute words in the string, according to the specified reflections,
        e.g. "I'm" -> "you are"

        :type str: str
        :param str: The string to be mapped
        :rtype: str
        """
        if not self.attr.get("substitute", True):
            return str
        return self._regex.sub(lambda mo: self._reflections[mo.string[mo.start():mo.end()]], str.lower())

    def _check_if(self, con, session_id="general"):
        pos = [(m.start(0), m.end(0), m.group(0)) for m in re.finditer(r'([\<\>!=]=|[\<\>]|&|\|)', con)]
        if not pos:
            return con.strip()
        res = prev_res = True
        symbol = "&"
        first = con[0:pos[0][0]].strip()
        for j in range(len(pos)):
            s, e, o = pos[j]
            try:
                second = con[e:pos[j+1][0]].strip()
            except Exception:
                second = con[e:].strip()
            try:
                a, b = float(first), float(second)
            except Exception:
                a, b = first, second
            try:
                res = self.__conditional_operator[o](a, b) and res
            except Exception:
                try:
                    prev_res, res = self.__logical_operator[symbol](prev_res, res), True
                except Exception:
                    raise SyntaxError("invalid conditional operator \"%s\"" % symbol)
                symbol = o
            first = second
        return self.__logical_operator[symbol](prev_res, res)

    def __if_handler(self, i, condition, response, session_id):
        start = self.__get_start_pos(condition[i]["start"], response, "if")
        end = condition[i]["end"]
        check = True
        matched_index = None
        _quote = self.attr[session_id]["_quote"]
        self.attr[session_id]["_quote"] = False
        substitute = self.attr.get("substitute", True)
        self.attr["substitute"] = False
        while check:
            con = self._check_and_evaluate_condition(response, condition[i]["child"], start, end, session_id=session_id)
            i += 1
            if self._check_if(con, session_id=session_id):
                matched_index = i-1
                while condition[i]["action"] != "endif":
                    i += 1
                check = False
            elif condition[i]["action"] == "else":
                matched_index = i
                while condition[i]["action"] != "endif":
                    i += 1
                check = False
            elif condition[i]["action"] == "elif":
                start = self.__get_start_pos(condition[i]["start"], response, "elif")
                end = condition[i]["end"]
            elif condition[i]["action"] == "endif":
                check = False
        self.attr[session_id]["_quote"] = _quote
        self.attr["substitute"] = substitute
        return ((self._check_and_evaluate_condition(
                                response,
                                condition[matched_index]["within"],
                                condition[matched_index]["end"]+2,
                                condition[matched_index+1]["start"]-2,
                                session_id=session_id
                                ) if matched_index is not None else ""), i)

    def __handler(self, condition, response, action, session_id):
        return self._check_and_evaluate_condition(
                                response,
                                condition["child"],
                                self.__get_start_pos(condition["start"], response, action),
                                condition["end"],
                                session_id=session_id
                                )

    def __chat_handler(self, condition, response, session_id):
        substitute = self.attr.get("substitute", True)
        self.attr["substitute"] = False
        response = self.respond(self.__handler(condition, response, "chat", session_id), session_id=session_id)
        self.attr["substitute"] = substitute
        return response

    def __low_handler(self, condition, response, session_id):
        return self.__handler(condition, response, "low", session_id).lower()

    def __up_handler(self, condition, response, session_id):
        return self.__handler(condition, response, "up", session_id).upper()

    def __cap_handler(self, condition, response, session_id):
        return self.__handler(condition, response, "cap", session_id).capitalize()

    def __call_handler(self, condition, response, session_id):
        substitute = self.attr.get("substitute", True)
        self.attr["substitute"] = False
        response = self.call.call(self.__handler(condition, response, "call", session_id), session_id=session_id)
        self.attr["substitute"] = substitute
        return response

    def __topic_handler(self, condition, response, session_id):
        self.topic[session_id] = self.__handler(condition, response, "topic", session_id).strip()
        return ""

    @staticmethod
    def __get_start_pos(start, response, exp):
        return start+re.compile(r"([\s\t]*"+exp+r"[\s\t]+)").search(response[start:]).end(1)

    def __map_handler(self, condition, response, session_id):
        start = condition["start"]
        end = condition["end"]
        think = False
        if response[start] == "!":
            think = True
            start += 1
        content = self._check_and_evaluate_condition(
                                    response,
                                    condition["child"],
                                    start,
                                    end,
                                    session_id=session_id
                                    ).strip().split(":")
        name = content[0]
        this_index = 0
        for this_index in range(1, len(content)):
            if name[-1] == "\\":
                name += ":"+content[this_index]
            else:
                this_index -= 1
                break
        this_index += 1
        name = name.strip().lower()
        if this_index < (len(content)):
            value = content[this_index]
            for this_index in range(this_index+1, len(content)):
                if value[-1] == "\\":
                    value += ":"+content[this_index]
                else:
                    break
            self._memory[session_id][name] = self._substitute(value.strip())
        return self._memory[session_id][name] if not think and name in self._memory[session_id] else ""

    def __eval_handler(self, condition, response, session_id):
        start = condition["start"]
        end = condition["end"]
        think = False
        if response[start] == "!":
            think = True
            start += 1
        _quote = self.attr[session_id]["_quote"]
        self.attr[session_id]["_quote"] = True
        content = self._check_and_evaluate_condition(
                                    response,
                                    condition["child"],
                                    start,
                                    end,
                                    session_id=session_id
                                    ).strip()
        self.attr[session_id]["_quote"] = _quote
        values = content.split(",")
        names = values[0].split(":")
        api_name = names[0]
        method_name = ":".join(names[1:])
        data = {}
        key = None
        for i in values[1:]:
            pair = i.split(":")
            if len(pair) >= 2:
                key = pair[0]
                data[key] = ":".join(pair[1:])
            elif key is not None:
                data[key] += ","+pair[0]
            else:
                raise SyntaxError("invalid syntax '%s'" % response[start:end])
        result = self.__api_handler(api_name, method_name, data)
        return "" if think else result

    def __api_request(self, url, method, **karg):
        try:
            return requests.__dict__[method.lower().strip()](url, **karg)
        except requests.exceptions.MissingSchema:
            return self.__api_request("http://"+url, method, **karg)
        except requests.exceptions.ConnectionError:
            raise RuntimeError("Couldn't connect to server (unreachable). Check your network")
        except KeyError:
            raise RuntimeError("Invalid method name '%s' in api.json" % method)

    def __api_handler(self, api_name, method_name, data={}):
        if api_name not in self._api or method_name not in self._api[api_name]:
            raise RuntimeError("Invalid method name '%s' for api '%s' ", (method_name, api_name))
        api_params = dict(self._api[api_name][method_name])
        if "auth" in self._api[api_name]:
            try:
                api_params["cookies"] = self.__api_request(**self._api[api_name]["auth"]).cookies
            except Exception:
                raise ValueError("In api.json 'auth' of '%s' is wrongly configured." % api_name)
        param = "params" if self._api[api_name][method_name]["method"].upper().strip() == "GET" else "data"
        try:
            api_params[param].update(data)
        except Exception:
            api_params[param] = data
        api_type = "normal"
        if "type" in api_params:
            api_type = api_params["type"]
            del api_params["type"]
        api_data_getter = []
        if "value_getter" in api_params:
            api_data_getter = api_params["value_getter"]
            del api_params["value_getter"]
        response = self.__api_request(**api_params)
        response_text = response.json() if api_type.upper().strip() == "JSON" else response.content
        for key in api_data_getter:
            response_text = response_text[key]
        return response_text

    def _quote(self, string, session_id):
        if self.attr[session_id]["_quote"]:
            try:
                return quote(string)
            except Exception:
                return quote(string.encode("UTF-8"))
        return string

    def __substitute_from_client_statement(self, match, prev_response, extra_symbol="", session_id="general"):
        """
        Substitute from Client statement into response
        """
        # TODO: Need to move re.find to pre processing
        prev = 0
        start_padding = 1+len(extra_symbol)
        final_response = ""
        for m in re.finditer(r'%'+extra_symbol+'[0-9]+', prev_response):
            start = m.start(0)
            end = m.end(0)
            num = int(prev_response[start+start_padding:end])
            final_response += prev_response[prev:start]
            try:
                final_response += self._quote(self._substitute(match.group(num)), session_id)
            except IndexError:
                pass
            prev = end
        named_group = match.groupdict()
        prev_response = final_response + prev_response[prev:]
        final_response = ""
        prev = 0
        for m in re.finditer(r'%'+extra_symbol+'([a-zA-Z_][a-zA-Z_0-9]*)([^a-zA-Z_0-9]|$)', prev_response):
            start = m.start(1)
            end = m.end(1)
            final_response += prev_response[prev:start-start_padding]
            value = named_group.get(prev_response[start:end], "").strip()
            if value:
                final_response += self._quote(self._substitute(value), session_id)
            prev = end
        return final_response + prev_response[prev:]

    def _check_and_evaluate_condition(self, response, condition=[], start_index=0, end_index=None,
                                      session_id="general"):
        end_index = end_index if end_index is not None else len(response)
        if not condition:
            final_response = self.__substitute_from_client_statement(self.attr[session_id]["match"],
                                                                     response[start_index:end_index],
                                                                     session_id=session_id)
            parent_match = self.attr[session_id]["pmatch"]
            return self.__substitute_from_client_statement(parent_match, final_response, extra_symbol='!',
                                                           session_id=session_id)\
                if parent_match is not None else final_response
        i = 0
        final_response = ""
        _quote = self.attr[session_id].get("_quote", True)
        while i < len(condition):
            pos = condition[i]["start"]-(1 if condition[i]["action"] in ("map", "eval") else 2)
            final_response += self._check_and_evaluate_condition(response[start_index:pos], session_id=session_id)
            try:
                self.attr[session_id]["_quote"] = False
                temp_response = self.__action_handlers[condition[i]["action"]](condition[i], response, session_id)
                self.attr[session_id]["_quote"] = _quote
                final_response += self._quote(temp_response, session_id)
            except KeyError:
                self.attr[session_id]["_quote"] = _quote
                if condition[i]["action"] == "if":
                    response_txt, i = self.__if_handler(i, condition, response, session_id)
                    final_response += response_txt
            start_index = condition[i]["end"]+(1 if condition[i]["action"] in ("map", "eval") else 2)
            i += 1
        final_response += self._check_and_evaluate_condition(response[start_index:end_index], session_id=session_id)
        return final_response

    def _wildcards(self, response, match, parent_match, session_id="general"):
        self.attr[session_id]["match"] = match
        self.attr[session_id]["pmatch"] = parent_match
        response, condition = response
        return re.sub(r'\\([\[\]{}%:])', r"\1",
                      self._check_and_evaluate_condition(response, condition, session_id=session_id))

    def __chose_and_process(self, choices, match, parent_match, session_id):
        resp = random.choice(choices)    # pick a random response
        resp = self._wildcards(resp, match, parent_match, session_id=session_id)  # process wildcards
        # fix munged punctuation at the end
        if resp[-2:] == '?.':
            resp = resp[:-2] + '.'
        if resp[-2:] == '??':
            resp = resp[:-2] + '?'
        return resp

    def __intend_selection(self, text, previous_text, current_topic):
        for (patterns, parents, response, learn) in self._pairs[current_topic]["pairs"]:  # check each pattern
            for pattern in patterns:
                match = pattern.match(text)
                if match:
                    break
            else:
                continue
            if parents is None:
                return match, None, response, learn
            for parent in parents:
                parent_match = parent.match(previous_text)
                if parent_match:  # did the pattern match?
                    return match, parent_match, response, learn

    def __response_on_topic(self, text, previous_text, text_correction, current_topic, session_id="general"):
        match = self.__intend_selection(text, previous_text, current_topic) or \
              self.__intend_selection(text_correction, previous_text, current_topic)
        if match:
            match, parent_match, response, learn = match
            if learn:
                self.__process_learn({
                    self._wildcards((topic, self._condition(topic)), match, parent_match, session_id=session_id):
                    {
                        'pairs': [self.__substitute_in_learn(pair, match, parent_match, session_id=session_id)
                                  for pair in learn[topic]['pairs']],
                        'defaults': [self._wildcards((default, self._condition(default)), match,
                                                     parent_match, session_id=session_id)
                                     for default in learn[topic]['defaults']]}
                    for topic in learn
                })
            return self.__chose_and_process(response, match, parent_match, session_id)
        if self._pairs[current_topic]["defaults"]:
            return self.__chose_and_process(self._pairs[current_topic]["defaults"], DummyMatch(text), None, session_id)
        raise ValueError("No match found")

    def respond(self, text, session_id="general"):
        """
        Generate a response to the user input.

        :type text: str
        :param text: The string to be mapped
        :type session_id: str
        :param session_id: Current User session when used for multi user scenario
        :rtype: str
        """
        text = self.__normalize(text)
        try:
          previous_text = self.__normalize(self.conversation[session_id][-2])
        except IndexError:
          previous_text = ""
        text_correction = correction(text)
        current_topic = self.topic[session_id]
        current_topic_order = current_topic.split(".")
        while current_topic_order:
            try:
                return self.__response_on_topic(text, previous_text, text_correction, current_topic, session_id)
            except ValueError:
                pass
            current_topic_order.pop()
            current_topic = ".".join(current_topic_order)
        try:
            return self.__response_on_topic(text, previous_text, text_correction, current_topic, session_id)
        except ValueError:
            return "Sorry I couldn't find anything relevant"

    def __substitute_in_learn(self, pair, match, parent_match, session_id="general"):
        return tuple((self.__substitute_in_learn(i, match, parent_match, session_id=session_id)
                      if type(i) in (tuple, list) else
                      (i if type(i) == dict else (self._wildcards((i, self._condition(i)), match, parent_match,
                                                                  session_id=session_id) if i else i))) for i in pair)

    @staticmethod
    def __get_topic_recursion(topics):
        result = {}
        for topic in topics:
            topic_depth = result
            for sub_topic in topic.split("."):
                topic_depth = topic_depth.setdefault(sub_topic, {})
        try:
            del result['']
            result = {'': result}
        except Exception:
            pass
        return result

    def save_template(self, filename):
        with open(filename, "w") as template:
            for topic_name, sub_topic in self.__get_topic_recursion(self._pairs).items():
                self.__generate_and_write_template(template, self._pairs, topic_name, sub_topic)

    def __generate_and_write_template(self, template, pairs, topic, sub_topics, base_path=None, padding=""):
        full_path = (base_path+"."+topic) if base_path else topic
        if topic:
            template.write(padding + "{% group "+topic+" %}\n")
            new_padding = padding + "\t"
        else:
            new_padding = padding
        for topic_name, sub_topic in sub_topics.items():
            self.__generate_and_write_template(template, pairs, topic_name, sub_topic, full_path,
                                               padding=new_padding+"\t")
        for (patterns, parents, response, learn) in pairs[full_path]["pairs"]:
            template.write(new_padding + "{% block %}\n")
            if parents is None:
                parents = []
            for parent in parents:
                template.write(new_padding + "\t{% prev %}"+parent.pattern+"{% endprev %}\n")
            for pattern in patterns:
                template.write(new_padding + "\t{% client %}"+pattern.pattern+"{% endclient %}\n")
            for res in response:
                template.write(new_padding + "\t{% response %}"+res[0]+"{% response %}\n")
            if learn:
                template.write(new_padding + "\t{% learn %}\n")
                for topic_name, sub_topic in self.__get_topic_recursion(learn).items():
                    self.__generate_and_write_template(template, learn, topic_name, sub_topic,
                                                       padding=new_padding+"\t")
                template.write(new_padding + "\t{% endlearn %}\n")
            template.write(new_padding + "{% endblock %}\n")
        for res in pairs[topic]["defaults"]:
            template.write(new_padding + "{% response %}"+res[0]+"{% response %}\n")
        if topic:
            template.write(padding + "{% endgroup %}\n")

    def say(self, message, session_id="general"):
        """
        say is a messagehandler takes a client message and returns response 
        :type message: str
        :param message: Client message
        :type session_id: str
        :param session_id: Current User session when used for multi user scenario
        :rtype: str
        """
        self.conversation[session_id].append(message)
        respnse = self.respond(message.rstrip("!."), session_id=session_id)
        self.conversation[session_id].append(respnse)
        return response

    # Hold a conversation with a chatbot
    def converse(self, first_question=None, quit="quit", session_id="general"):
        """
        Conversation initiator

        :type first_question: str
        :param first_question: Start up message
        :type quit: str
        :param quit: Conversation termination command
        :type session_id: str
        :param session_id: Current User session when used for multi user scenario
        :rtype: str
        """
        if first_question:
            self.conversation[session_id].append(first_question)
            print(first_question)
        input_sentence = ""
        while input_sentence != quit:
            input_sentence = quit
            try:
                input_sentence = input_reader("> ")
            except EOFError:
                print(input_sentence)
            if input_sentence:
                print(self.say(input_sentence))


def demo():
    first_question = "Hi, how are you?"
    Chat().converse(first_question)
