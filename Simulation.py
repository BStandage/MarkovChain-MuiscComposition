from mido import MidiFile, MidiTrack, Message
import numpy as np
import random

from Parse import Parse

class Simulation:

    def __init__(self, tpm):
        self.tpm = tpm
        self.track = []
        self.initial_note = self.get_init_note()

        
    # *BUG* Must adjust duration
    # The problem is that the choice funciton can not select tuples.
    # To get around this we must index the list of tuples and select the index corresponding to the selected probability.
    def to_midi_message(self, n, d):
        return [Message('note_on', note=n, velocity=127, time=0),
                Message('note_off', note=n, velocity=0, time=d)]


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
            keys.append([i, self.tpm[note][i][0]])

        return keys[np.random.choice(len(keys), p=transition_probabilities)]


    # Recursively find the most probably transition note and fill the track
    def next_state(self, initial_note, l):
        if l > 0:
            while True:
                next = self.transition(initial_note[0])
                difference = abs(initial_note[0] - next[0])
                if 60 < next[0] < 84 and difference <= 9:
                    break
            self.track.append(self.to_midi_message(next[0], next[1]))
            l -= 1
            self.next_state(next, l)
        else:
            return self.track




if __name__ == '__main__':
    file = Parse('bach_846.mid')
    tpm = file.parse()
    print(tpm)
    simulate = Simulation(tpm)
    print(simulate.next_state([78, 50], 100))
    print(simulate.track)


    # CREATE A NEW CLASS TO BUILD CONVERT INTO MIDI FILE
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    for i in simulate.track:
        track.append(i[0])
        track.append(i[1])


    print(mid)

    mid.save('test.mid')







## Consider making histograms transitions in every key, then normalize and compare
