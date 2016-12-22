import re

class Learn:

    def __init__(self,statements=[],falseStatements=[]):
        sentenceToWords = [s.split() for s in statements]
        if len(sentenceToWords):
            stripper = re.compile("(^[^a-z0-9]+|[^a-z0-9]+$)")
            commonWords = set(stripper.sub("",word) for word in sentenceToWords[0])
            for words in sentenceToWords[1:]:
                commonWords = commonWords.intersection(stripper.sub("",word)  for word in words)
            
