import chatbot
from os import path
from collections import Counter
from chatbot.spellcheck import SpellChecker


def unit_tests():
    local_path = path.join(path.dirname(path.abspath(chatbot.__file__)), "local")
    spell_checker = SpellChecker(local_path, language='en')
    assert spell_checker.correction('speling') == 'spelling'               # insert
    assert spell_checker.correction('korrectud') == 'corrected'            # replace 2
    assert spell_checker.correction('bycycle') == 'bicycle'                # replace
    assert spell_checker.correction('inconvient') == 'inconvenient'        # insert 2
    assert spell_checker.correction('arrainged') == 'arranged'             # delete
    assert spell_checker.correction('peotry') == 'poetry'                  # transpose
    assert spell_checker.correction('peotryy') == 'poetry'                 # transpose + delete
    assert spell_checker.correction('word') == 'word'                      # known
    assert spell_checker.correction('quintessential') == 'quintessential'  # unknown
    assert spell_checker.words('This is a TEST.') == ['this', 'is', 'a', 'test']
    assert Counter(
        spell_checker.words('This is a test. 123; A TEST this is.')) == (
           Counter({'123': 1, 'a': 2, 'is': 2, 'test': 2, 'this': 2}))
    assert len(spell_checker.WORDS) == 506747
    assert sum(spell_checker.WORDS.values()) == 1642669
    assert spell_checker.WORDS.most_common(10) == [
           ('the', 79811),
           ('of', 40026),
           ('and', 38315),
           ('to', 28767),
           ('in', 22026),
           ('a', 21124),
           ('that', 12513),
           ('he', 12404),
           ('was', 11411),
           ('it', 10684)]
    assert spell_checker.WORDS['the'] == 79811
    assert spell_checker.probability('quintessential') > 0
    assert 0.04 < spell_checker.probability('the') < 0.08
    return 'unit_tests pass'


def spell_test(tests, verbose=False):
    """
    Run correction(wrong) on all (right, wrong) pairs; report results.
    """
    import time
    start = time.clock()
    good, unknown = 0, 0
    n = len(tests)
    local_path = path.join(path.dirname(path.abspath(chatbot.__file__)), "local")
    spell_checker = SpellChecker(local_path, language='en')
    for right, wrong in tests:
        w = spell_checker.correction(wrong)
        good += (w == right)
        if w != right:
            unknown += (right not in spell_checker.WORDS)
            if verbose:
                print('correction({}) => {} ({}); expected {} ({})'
                      .format(wrong, w, spell_checker.WORDS[w], right, spell_checker.WORDS[right]))
    dt = time.clock() - start
    print('{:.0%} of {} correct ({:.0%} unknown) at {:.0f} words per second '
          .format(good / n, n, unknown / n, n / dt))


def test_set(lines):
    """
    Parse 'right: wrong1 wrong2' lines into [('right', 'wrong1'), ('right', 'wrong2')] pairs.
    :param lines:
    :return:
    """
    return [(right, wrong)
            for (right, wrongs) in (line.split(':') for line in lines)
            for wrong in wrongs.split()]


if __name__ == '__main__':
    print(unit_tests())
    spell_test(test_set(open(path.join(path.dirname(path.abspath(__file__)), 'spell-testset1.txt'))))
    spell_test(test_set(open(path.join(path.dirname(path.abspath(__file__)), 'spell-testset2.txt'))))
