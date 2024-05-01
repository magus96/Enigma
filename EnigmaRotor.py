from EnigmaConstants import *

def apply_pemutation(letter, permutation, offset):
    idx = (ALPHABET.find(letter) + offset) % 26
    perm_letter = permutation[idx]
    perm_idx = (ALPHABET.find(perm_letter) - offset) % 26
    return perm_idx

def invert_perm(permutation):
    original_perm = [letter for letter in ALPHABET]
    rotor_perm = permutation    
    rev_perm_list = [original_perm[rotor_perm.find(orig_letter)] for orig_letter in original_perm]
    rev_perm = ''.join(rev_perm_list)
    return rev_perm

class EnigmaRotor():

    def __init__(self, permutation):
        self.offset = 0
        self.permutation = permutation
        self.carry = False
    
    def get_offset(self):
        return self.offset

    def get_permutation(self):
        return self.permutation
    
    def advance(self):
        self.offset += 1
        self.offset = self.offset % 26
    

