import atexit
import tkinter
import tkinter.font

class EnigmaView:

    def __init__(self, enigma):

        def create_window():
            root = tkinter.Tk()
            root.title("Enigma")
            root.protocol("WM_DELETE_WINDOW", delete_window)
            self._root = root
            canvas = tkinter.Canvas(root,
                                    bg="White",
                                    width=CANVAS_WIDTH,
                                    height=CANVAS_HEIGHT,
                                    highlightthickness=0)
            canvas.pack()
            self._canvas = canvas
            self._families = tkinter.font.families()
            return canvas

        def add_background():
            bg = tkinter.PhotoImage(file="images/EnigmaTopView.png")
            self._root._bg = bg
            canvas.create_image((0,0), image=bg, anchor=tkinter.NW)

        def add_keys():
            self._keys = { }
            canvas = self._canvas
            font = create_font(KEY_FONT_FAMILIES,
                               KEY_FONT_SIZE,
                               KEY_FONT_OPTIONS)
            for letter in ALPHABET:
                x,y = KEY_LOCATIONS[letter]
                disc = canvas.create_oval(x - KEY_RADIUS,
                                          y - KEY_RADIUS,
                                          x + KEY_RADIUS,
                                          y + KEY_RADIUS,
                                          fill=KEY_BGCOLOR,
                                          outline=KEY_BORDER_COLOR,
                                          width=KEY_BORDER)
                label = canvas.create_text(x, y,
                                           text=letter,
                                           font=font,
                                           fill=KEY_UP_COLOR,
                                           anchor=tkinter.CENTER)
                self._keys[letter] = (disc,label)

        def add_lamps():
            self._lamps = { }
            canvas = self._canvas
            font = create_font(LAMP_FONT_FAMILIES,
                               LAMP_FONT_SIZE,
                               LAMP_FONT_OPTIONS)
            for letter in ALPHABET:
                x,y = LAMP_LOCATIONS[letter]
                disc = canvas.create_oval(x - LAMP_RADIUS,
                                                y - LAMP_RADIUS,
                                                x + LAMP_RADIUS,
                                                y + LAMP_RADIUS,
                                                fill=LAMP_BGCOLOR,
                                                outline=LAMP_BORDER_COLOR)
                label = canvas.create_text(x, y,
                                                 text=letter,
                                                 font=font,
                                                 fill=LAMP_OFF_COLOR,
                                                 anchor=tkinter.CENTER)
                self._lamps[letter] = (disc,label)

        def add_rotors():
            self._rotors = [ ]
            canvas = self._canvas
            font = create_font(ROTOR_FONT_FAMILIES,
                               ROTOR_FONT_SIZE,
                               ROTOR_FONT_OPTIONS)
            for index in range(N_ROTORS):
                x,y = ROTOR_LOCATIONS[index]
                frame = canvas.create_rectangle(x - ROTOR_WIDTH / 2,
                                                y - ROTOR_HEIGHT / 2,
                                                x + ROTOR_WIDTH / 2,
                                                y + ROTOR_HEIGHT / 2,
                                                outline=ROTOR_BGCOLOR,
                                                fill=ROTOR_BGCOLOR)
                label = canvas.create_text(x, y,
                                           text="A",
                                           font=font,
                                           fill=ROTOR_COLOR,
                                           anchor=tkinter.CENTER)
                self._rotors.append((frame,label))

        def create_font(families, size, options):
            return (find_font_family(families), size, options)

        def find_font_family(families):
            for family in families:
                for installed in self._families:
                    if installed.upper() == family.upper():
                        return installed
            return ""

        def button_press_action(tke):
            letter = find_key(tke)
            if letter is not None:
                self._enigma.key_pressed(letter)
            else:
                index = find_rotor(tke)
                if index is not None:
                    self._enigma.rotor_clicked(index)

        def button_release_action(tke):
            letter = find_key(tke)
            if letter is not None:
                self._enigma.key_released(letter)

        def find_key(tke):
            r2 = KEY_RADIUS ** 2
            for letter in ALPHABET:
                x,y = KEY_LOCATIONS[letter]
                if (x - tke.x) ** 2 + (y - tke.y) ** 2 <= r2:
                    return letter
            return None

        def find_rotor(tke):
            w2 = ROTOR_FRAME_WIDTH / 2
            h2 = ROTOR_FRAME_HEIGHT / 2
            for index in range(N_ROTORS):
                x,y = ROTOR_LOCATIONS[index]
                if x - w2 < tke.x < x + w2 and y - h2 < tke.y < y + h2:
                    return index
            return None

        def delete_window():
            self._root.destroy()

        def start_event_loop():
            self._root.mainloop()

        self._enigma = enigma
        canvas = create_window()
        add_background()
        add_keys()
        add_lamps()
        add_rotors()
        self._root.bind("<ButtonPress-1>", button_press_action)
        self._root.bind("<ButtonRelease-1>", button_release_action)
        atexit.register(start_event_loop)

    def update(self):

        def update_keys():
            for letter in ALPHABET:
                disc,label = self._keys[letter]
                if self._enigma.is_key_down(letter):
                    color = KEY_DOWN_COLOR
                else:
                    color = KEY_UP_COLOR
                self._canvas.itemconfigure(label, fill=color)
                
        def update_lamps():
            for letter in ALPHABET:
                disc,label = self._lamps[letter]
                if self._enigma.is_lamp_on(letter):
                    color = LAMP_ON_COLOR
                else:
                    color = LAMP_OFF_COLOR
                self._canvas.itemconfigure(label, fill=color)

        def update_rotors():
            for index in range(N_ROTORS):
                frame,label = self._rotors[index]
                letter = self._enigma.get_rotor_letter(index)
                self._canvas.itemconfigure(label, text=letter)

        update_keys()
        update_lamps()
        update_rotors()

        
# Constants

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWZYZ"
N_ROTORS = 3

CANVAS_WIDTH = 818              # Width of the tkinter canvas (pixels)
CANVAS_HEIGHT = 694             # Height of the tkinter canvas (pixels)

ROTOR_BGCOLOR = "#BBAA77"       # Background color for the rotor
ROTOR_WIDTH = 24                # Width of the setting indicator
ROTOR_HEIGHT = 26               # Height of the setting indicator
ROTOR_FRAME_WIDTH = 40          # Width of clickable area
ROTOR_FRAME_HEIGHT = 100        # Height of clickable area
ROTOR_COLOR = "Black"           # Text color of the rotor
ROTOR_FONT_SIZE = -24           # 24px font
ROTOR_FONT_OPTIONS = ""
ROTOR_FONT_FAMILIES = [
"Helvetica Neue",
"Arial",
"Sans-Serif"
]

# This array specifies the coordinates of each rotor display

ROTOR_LOCATIONS = [
    (244, 94),
    (329, 94),
    (412, 94)
]

# Constants that define the keys on the Enigma keyboard

KEY_RADIUS = 24                 # Outer radius of a key in pixels
KEY_BORDER = 3                  # Width of the key border
KEY_BORDER_COLOR = "#CCCCCC"    # Fill color of the key border
KEY_BGCOLOR = "#666666"         # Background color of the key
KEY_UP_COLOR = "#CCCCCC"        # Text color when the key is up
KEY_DOWN_COLOR = "#CC3333"      # Text color when the key is down
KEY_FONT_SIZE = -28
KEY_FONT_OPTIONS = "bold"
KEY_FONT_FAMILIES = [
    "Helvetica Neue",
    "Helvetica",
    "Arial"
]

# This array determines the coordinates of a key for each letter index

KEY_LOCATIONS = {
    "A": (140, 566),
    "B": (471, 640),
    "C": (319, 639),
    "D": (294, 567),
    "E": (268, 495),
    "F": (371, 567),
    "G": (448, 567),
    "H": (523, 567),
    "I": (650, 496),
    "J": (598, 567),
    "K": (674, 567),
    "L": (699, 641),
    "M": (624, 641),
    "N": (547, 640),
    "O": (725, 497),
    "P": ( 92, 639),
    "Q": (115, 494),
    "R": (345, 495),
    "S": (217, 566),
    "T": (420, 496),
    "U": (574, 496),
    "V": (395, 639),
    "W": (192, 494),
    "X": (242, 639),
    "Y": (168, 639),
    "Z": (497, 496)
}

# Constants that define the lamps above the Enigma keyboard

LAMP_RADIUS = 23                # Radius of a lamp in pixels
LAMP_BORDER_COLOR = "#111111"   # Line color of the lamp border
LAMP_BGCOLOR = "#333333"        # Background color of the lamp
LAMP_OFF_COLOR = "#666666"      # Text color when the lamp is off
LAMP_ON_COLOR = "#FFFF99"       # Text color when the lamp is on
LAMP_FONT_SIZE = -24
LAMP_FONT_OPTIONS = "bold"
LAMP_FONT_FAMILIES = [
    "Helvetica Neue",
    "Helvetica",
    "Arial"
]

# This array determines the coordinates of a lamp for each letter index

LAMP_LOCATIONS = {
    "A": (144, 332),
    "B": (472, 403),
    "C": (321, 402),
    "D": (296, 333),
    "E": (272, 265),
    "F": (372, 333),
    "G": (448, 334),
    "H": (524, 334),
    "I": (650, 266),
    "J": (600, 335),
    "K": (676, 335),
    "L": (700, 403),
    "M": (624, 403),
    "N": (549, 403),
    "O": (725, 267),
    "P": ( 94, 401),
    "Q": (121, 264),
    "R": (347, 265),
    "S": (220, 332),
    "T": (423, 265),
    "U": (574, 266),
    "V": (397, 402),
    "W": (197, 264),
    "X": (246, 402),
    "Y": (170, 401),
    "Z": (499, 265)
}
