import mido
import random

from Parse import Parse

class Simulation:

    def __init__(self):
        

    def to_midi_message(self):
        return [mido.Message('note_on', note=0, velocity=127, time=0),
                mido.Message('note_off', note=0, velocity=0, time="duration")]


    # We want to randomly begin the piece on the 1 or the 5
    # For Fugue in C Major, start with C=60 to test
    def get_init_note(self):





    def next_state(self, initial_note):
        return

