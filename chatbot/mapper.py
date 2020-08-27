class Session:

    def __init__(self, chat, session_id):
        self.__chat = chat
        self.session_id = session_id

    @property
    def conversation(self):
        return self.__chat._conversation[self.session_id]

    @conversation.setter
    def conversation(self, value):
        self.__chat._conversation[self.session_id] = value

    @property
    def memory(self):
        return self.__chat._memory[self.session_id]

    @memory.setter
    def memory(self, value):
        self.__chat._memory[self.session_id] = value

    @property
    def attr(self):
        return self.__chat._attr[self.session_id]

    @attr.setter
    def attr(self, value):
        self.__chat._attr[self.session_id] = value

    @property
    def topic(self):
        return self.__chat._topic[self.session_id]

    @topic.setter
    def topic(self, value):
        self.__chat._topic[self.session_id] = value


class Conversation(list):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__bot_message = []
        self.__user_message = []

    def append_bot_message(self, message):
        self.__bot_message.append(message)
        self.append(message)

    def append_user_message(self, message):
        self.__user_message.append(message)
        self.append(message)

    def get_bot_message(self, index):
        return self.__bot_message[index]

    def get_user_message(self, index):
        return self.__user_message[index]


class SessionHandler:

    def __init__(self, _class, **kwargs):
        self._class = _class
        self.__data = {key: _class(value) for key, value in kwargs.items()}

    def __getitem__(self, key):
        return self.__data[key]

    def __setitem__(self, sender_id, val):
        self.__data[sender_id] = self._class(val)

    def update(self, *args, **kwargs):
        data = dict(*args, **kwargs)
        for key, val in data.items():
            self.__data[key] = self._class(val)

    def __delitem__(self, *args, **kwargs):
        return self.__data.__delitem__(*args, **kwargs)

    def __contains__(self, *args, **kwargs):
        return self.__data.__contains__(*args, **kwargs)

    def __iter__(self):
        return self.__data.__iter__()

    def __len__(self):
        return self.__data.__len__()

    def __repr__(self, *args, **kwargs):
        return self.__data.__repr__()

    def __sizeof__(self, *args, **kwargs):
        return self.__data.__sizeof__()

    def __str__(self, *args, **kwargs):
        return self.__data.__str__()

    def clear(self):
        return self.__data.clear()

    def copy(self):
        return SessionHandler(self._class, **self.__data)

    def fromkeys(self, *args):
        return self.__data.fromkeys(*args)

    def get(self, *args):
        return self.__data.get(*args)

    def items(self):
        return self.__data.items()

    def keys(self):
        return self.__data.keys()

    def pop(self, *args):
        return self.__data.pop(*args)

    def popitem(self):
        return self.__data.popitem()

    def setdefault(self, *args, **kwargs):
        return self.__data.setdefault(*args, **kwargs)

    def values(self):
        return self.__data.values()
