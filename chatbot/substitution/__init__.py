from importlib import import_module
import warnings


class Substitution:
    def __init__(self, language="en"):
        try:
            self.substitutions = import_module("."+language, package="chatbot.substitution")
        except ModuleNotFoundError:
            warnings.warn("substitution for language `{}` not Implemented".format(language),
                          ImportWarning)
            self.substitutions = import_module(".en", package="chatbot.substitution")

    def __getattr__(self, item):
        try:
            return getattr(self.substitutions, item)
        except AttributeError:
            warnings.warn("substitution doesnt have {}".format(item),
                          Warning)
        return {}

