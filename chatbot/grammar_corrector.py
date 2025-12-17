"""
Simple grammar correction for AI-generated text.
Fixes common issues like word order, contractions, and basic sentence structure.
"""

class GrammarCorrector:
    def __init__(self):
        # Common contraction fixes
        self.contractions = {
            "s ": "'s ",
            "t ": "'t ",
            "re ": "'re ",
            "ve ": "'ve ",
            "ll ": "'ll ",
            "d ": "'d ",
            "m ": "'m ",
        }
        
        # Sentence structure patterns
        self.structure_patterns = [
            # "X is the Y of Z" structure
            (r'\bis\s+the\s+(\w+)\s+.*?\s+of\s+', 'subject_verb_object'),
            # "X Y is Z" -> "X is Y Z"
            (r'(\w+\s+\w+)\s+is\s+(\w+)', 'simple_reorder')
        ]
    
    def fix_contractions(self, text):
        """Fix broken contractions like "musk s" -> "musk's" """
        words = text.split()
        fixed = []
        
        i = 0
        while i < len(words):
            word = words[i]
            
            # Check if next word is a contraction part
            if i + 1 < len(words):
                next_word = words[i + 1]
                if next_word in ['s', 't', 're', 've', 'll', 'd', 'm']:
                    # Merge with apostrophe
                    fixed.append(word + "'" + next_word)
                    i += 2
                    continue
            
            fixed.append(word)
            i += 1
        
        return ' '.join(fixed)
    
    def fix_word_order(self, text):
        """Fix word order using flexible patterns"""
        import re
        
        words = text.split()
        if len(words) < 3:
            return text
            
        # Find structural elements
        verb_pos = self._find_verb_position(words)
        subject_words, object_words = self._extract_subject_object(words, verb_pos)
        
        # Reconstruct if we found valid structure
        if subject_words and object_words and verb_pos >= 0:
            verb = words[verb_pos]
            # Check for "the X of" pattern
            if any(w.lower() in ['capital', 'answer', 'result', 'solution'] for w in words):
                relation_word = next((w for w in words if w.lower() in ['capital', 'answer', 'result', 'solution']), 'capital')
                text = f"{' '.join(subject_words)} {verb} the {relation_word} of {' '.join(object_words)}"
        
        # Clean up trailing verbs
        text = re.sub(r'\s+(is|are)\.?$', '', text, flags=re.IGNORECASE)
        
        return text
    
    def _find_verb_position(self, words):
        """Find position of main verb (is, are, was, were)"""
        verbs = ['is', 'are', 'was', 'were']
        for i, word in enumerate(words):
            if word.lower() in verbs:
                return i
        return -1
    
    def _extract_subject_object(self, words, verb_pos):
        """Extract subject and object from word list"""
        if verb_pos < 0:
            return [], []
            
        # Find "of" position
        of_pos = next((i for i, w in enumerate(words) if w.lower() == 'of'), -1)
        
        if of_pos > verb_pos:
            # Subject is before verb, object is after "of"
            subject = [w for w in words[:verb_pos] if w.lower() not in ['the', 'a', 'an']]
            object_words = words[of_pos + 1:]
            return subject, object_words
        
        return [], []
    
    def capitalize_sentences(self, text):
        """Capitalize first letter of sentences"""
        if not text:
            return text
        
        # Capitalize first character
        text = text[0].upper() + text[1:] if len(text) > 1 else text.upper()
        
        # Capitalize after periods
        import re
        text = re.sub(r'(\.\s+)([a-z])', lambda m: m.group(1) + m.group(2).upper(), text)
        
        return text
    
    def add_punctuation(self, text):
        """Add period at end if missing"""
        if not text:
            return text
        
        if text[-1] not in '.!?':
            text += '.'
        
        return text
    
    def correct(self, text):
        """Apply all grammar corrections"""
        if not text or not text.strip():
            return text
        
        import re
        
        # Apply fixes in order
        text = self.fix_contractions(text)
        text = self.fix_word_order(text)
        text = self.capitalize_sentences(text)
        text = self.add_punctuation(text)
        
        # Clean up extra spaces
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
