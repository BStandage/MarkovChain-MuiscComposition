import mido
from mido import MidiFile, MidiTrack
import numpy as np
import json
import random

from Parse import Parse

class Simulation:

    def __init__(self, tpm):
        self.tpm = tpm
        self.track = []
        self.initial_note = self.get_init_note()

        
    # Must adjust duration
    def to_midi_message(self, n):
        return [mido.Message('note_on', note=n, velocity=127, time=0),
                mido.Message('note_off', note=n, velocity=0, time=50)]


    # We want to randomly begin the piece on the 1 or the 5
    # For Fugue in C Major, start with C=60 to test
    def get_init_note(self):
        self.initial_note = 60


    # Transition function simulations transition given current state
    def transition(self, note):
        transition_probabilities = []
        keys = []

        #What if the note generated is not in the matrix?
        print(note)
        for i in self.tpm[note]:
            transition_probabilities.append(self.tpm[note][i][1])
            # [i, self.tpm[note][i][0]]
            keys.append(i)

        return np.random.choice(keys, p=transition_probabilities)


    # Recursive
    def next_state(self, initial_note, l):
        if(l > 0):
            next = self.transition(initial_note)
            self.track.append(self.to_midi_message(next))
            l -= 1
            self.next_state(next, l)
        else:
            return self.track




if __name__ == '__main__':
    file = Parse('bach_846.mid')
    tpm = file.parse()
    print(tpm)
    simulate = Simulation(tpm)
    print(simulate.next_state(72, 100))
    print(simulate.track)


    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    for i in simulate.track:
        track.append(i[0])
        track.append(i[1])


    print(mid)

    mid.save('test.mid')







## Consider making histograms transitions in every key, then normalize and compare
