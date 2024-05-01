from EnigmaView import EnigmaView
from EnigmaConstants import *
from EnigmaRotor import EnigmaRotor, apply_pemutation, invert_perm

class EnigmaModel:

    def __init__(self):
        self._views = [ ]
        self._key_states = {key:False for key in ALPHABET}
        self._lamp_states = {key:False for key in ALPHABET}
        self._slow_rotor = EnigmaRotor(ROTOR_PERMUTATIONS[0])
        self._medium_rotor = EnigmaRotor(ROTOR_PERMUTATIONS[1])
        self._fast_rotor = EnigmaRotor(ROTOR_PERMUTATIONS[2])
        self._slow_rotor_rev = EnigmaRotor(invert_perm(ROTOR_PERMUTATIONS[0]))
        self._medium_rotor_rev = EnigmaRotor(invert_perm(ROTOR_PERMUTATIONS[1]))
        self._fast_rotor_rev = EnigmaRotor(invert_perm(ROTOR_PERMUTATIONS[2]))
        self.rotors = [self._slow_rotor, self._medium_rotor, self._fast_rotor, self._slow_rotor_rev, self._medium_rotor_rev, self._fast_rotor_rev]

    def add_view(self, view):
        self._views.append(view)

    def update(self):
        for view in self._views:
            view.update()

    def is_key_down(self, letter):
        return self._key_states[letter]       

    def is_lamp_on(self, letter):
        return self._lamp_states[letter]        

    def key_pressed(self, letter):
        self._key_states[letter] = True
        self.rotor_clicked(2)

        if self.rotors[1].carry == True:
            self.rotor_clicked(0)

        if self.rotors[2].carry == True:
            self.rotor_clicked(1)
        
        if self.rotors[2].get_offset() == 25:
            self.rotors[2].carry = True
        elif self.rotors[2].get_offset() != 25:
            self.rotors[2].carry = False
        
        if self.rotors[1].get_offset() == 25:
            self.rotors[1].carry = True
        elif self.rotors[1].get_offset() != 25:
            self.rotors[1].carry = False

        lamp_idx = apply_pemutation(letter, self.rotors[2].get_permutation(), self.rotors[2].get_offset())
        lamp_idx = apply_pemutation(ALPHABET[lamp_idx], self.rotors[1].get_permutation(), self.rotors[1].get_offset())
        lamp_idx = apply_pemutation(ALPHABET[lamp_idx], self.rotors[0].get_permutation(), self.rotors[0].get_offset())
        lamp_idx = apply_pemutation(ALPHABET[lamp_idx], REFLECTOR_PERMUTATION, 0)
        lamp_idx = apply_pemutation(ALPHABET[lamp_idx], self.rotors[3].get_permutation(), self.rotors[3].get_offset())
        lamp_idx = apply_pemutation(ALPHABET[lamp_idx], self.rotors[4].get_permutation(), self.rotors[4].get_offset())
        lamp_idx = apply_pemutation(ALPHABET[lamp_idx], self.rotors[5].get_permutation(), self.rotors[5].get_offset())
        self._lamp_states[ALPHABET[lamp_idx]] = True
        self.update()

    def key_released(self, letter):
        self._key_states[letter] = False
        lamp_idx = apply_pemutation(letter, self.rotors[2].get_permutation(), self.rotors[2].get_offset())
        lamp_idx = apply_pemutation(ALPHABET[lamp_idx], self.rotors[1].get_permutation(), self.rotors[1].get_offset())
        lamp_idx = apply_pemutation(ALPHABET[lamp_idx], self.rotors[0].get_permutation(), self.rotors[0].get_offset())
        lamp_idx = apply_pemutation(ALPHABET[lamp_idx], REFLECTOR_PERMUTATION, 0)
        lamp_idx = apply_pemutation(ALPHABET[lamp_idx], self.rotors[3].get_permutation(), self.rotors[3].get_offset())
        lamp_idx = apply_pemutation(ALPHABET[lamp_idx], self.rotors[4].get_permutation(), self.rotors[4].get_offset())
        lamp_idx = apply_pemutation(ALPHABET[lamp_idx], self.rotors[5].get_permutation(), self.rotors[5].get_offset())
        self._lamp_states[ALPHABET[lamp_idx]] = False
        self.update()

    def get_rotor_letter(self, index):
        offset = self.rotors[index].get_offset()
        letter = ALPHABET[offset]
        return letter          

    def rotor_clicked(self, index):
        self.rotors[index].advance()
        self.update()

def enigma():
    """Runs the Enigma simulator."""
    model = EnigmaModel()
    view = EnigmaView(model)
    model.add_view(view)

# Startup code

if __name__ == "__main__":
    enigma()
