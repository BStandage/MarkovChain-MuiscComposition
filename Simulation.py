from mido import MidiFile, MidiTrack, Message
import numpy as np
import random


class Simulation:


    # Simulation Constructor
    def __init__(self, tpm, track):
        self.tpm = tpm
        self.track = track
        self.messages = []
        self.initial_note = self.get_init_note()
        self.state_space = self.state_space()
        self.track.track.append(self.to_midi_message(self.initial_note[0], 250))


    # Function: to_midi_message
    # accept: a note and it's duration
    # return: a midi message
    # CHANGED DURATION TO 200ms
    def to_midi_message(self, n, d):
        return [Message('note_on', note=n, velocity=127, time=0),
                Message('note_off', note=n, velocity=0, time=d)]


    # We want to randomly begin the piece on the 1 or the 5
    # Function: get_init_note
    # accept: self
    # return: initial note given a track simulation object
    def get_init_note(self):
        return [random.choice([67])]


    # Transition function simulations transition given current state
    # Function: transition
    # accept: a note
    # return: the most likely next note given the previous note
    def transition(self, note):
        transition_probabilities = []
        keys = []

        for i in self.tpm[note]:
            transition_probabilities.append(self.tpm[note][i][1])
            keys.append([i, self.tpm[note][i][0]])

        return keys[np.random.choice(len(keys), p=transition_probabilities)]


    # Recursively find the most probable transition note and fill the track
    # Function: next_state
    # accept: a note and a number of notes
    # return: the most probable next note that is in the state space
    def next_state(self, initial_note, l):
        if l > 0:
            while True:
                next = self.transition(initial_note[0])
                difference = abs(initial_note[0] - next[0])
                # if there's a leap...
                if len(self.track.track) > 1 and abs(self.track.track[len(self.track.track) - 2][0].note - initial_note[0]) > 4:
                    next[0] = self.leap_rule()
                    print('Added via Leap: ', next)
                    break
                # downbeat and resolving note check
                elif l < 16 and initial_note[0] in [67, 71, 79, 83] and self.is_downbeat():
                    next[0] = self.resolving_note()
                    l = 0
                    print("Final Note Reached.")
                    break
                # if not then generate most probable
                elif self.not_trill(next[0]) and next[0] in self.state_space and next[0] != initial_note[0] and difference <= 9:
                    print('Added note: ', next)
                    break

            self.track.track.append(self.to_midi_message(next[0], next[1]))
            l -= 1
            self.next_state(next, l)
        else:
            return self.messages


    # Function: not_trill
    # accept: the most recently generated note
    # return: True if this note does not create a non-ornamental trill, False otherwise
    def not_trill(self, n):
        l = len(self.track.track)

        if l > 3:
            if (self.track.track[l - 1][0].note == self.track.track[l - 3][0].note
                and ((abs(self.track.track[l - 2][0].note - self.track.track[l - 1][0].note) == 1) or abs(self.track.track[l - 2][0].note - self.track.track[l - 1][0].note) == 2)) and \
                            self.track.track[l - 2][0].note == n:
                return False
            else:
                return True
        else:
            return True


    # If a leap exists (a jump in MIDI notes greater than 4) then the next note must be a step
    # in the opposite direction.
    # Function: leap_rule
    # accept: self
    # return: the next note in the state space given there was previously a leap
    def leap_rule(self):
        l = len(self.track.track)

        leap_size = self.track.track[l - 1][0].note - self.track.track[l - 2][0].note

        # if the piece leaps upwards
        if leap_size > 4:
            # move stepwise in the opposite direction, ensuring the next note is in the state space
            if self.track.track[l - 1][0].note - 2 in self.state_space:
                next = self.track.track[l - 1][0].note - 2
            else:
                next = self.track.track[l - 1][0].note - 1
        # if the piece leaps downwards
        elif leap_size < -4:
            if self.track.track[l - 1][0].note + 2 in self.state_space:
                next = self.track.track[l - 1][0].note + 2
            else:
                next = self.track.track[l - 1][0].note + 1

        return next


    # Define a statespace for the track. This state space is normalized over the C major scale
    # Function: state_space
    # accept: self
    # return: a statespace normalized about C Major
    def state_space(self):
        state_space = []
        complement = [1, 3, 6, 8, 10]
        for i in range(13):
            if i not in complement:
                #state_space.append(self.initial_note[0] + i)
                state_space.append(60 + i)

        # Extend state space an additional octave higher
        for i in range(1, len(state_space)):
          state_space.append(state_space[i] + 12)

        return state_space


    # ensures that the piece ends on a resolving tone
    # must add an additional function to make sure the resolving note also happens on the first or third beat
    # Function: resolving_note
    # accept: self
    # return: the final note of the piece
    def resolving_note(self):
        l = len(self.track.track)

        if self.track.track[l - 1][0].note == 67:
            final = random.choice([60, 72])
        elif self.track.track[l - 1][0].note == 79:
            final = random.choice([72, 84])
        elif self.track.track[l - 1][0].note == 71:
            final = 72
        elif self.track.track[l - 1][0].note == 83:
            final = 84

        return final

    # Function: is_downbeat
    # accept: self
    # return: True if the next note played will be on the first or third beat
    def is_downbeat(self):
        # if the total duration mod 1000 == 0 then it is a downbeat
        time = 0

        for i in self.track.track:
            time += i[1].time
        if time % 1000 == 0:
            return True
        else:
            return False