from mido import MidiFile
import itertools

'''
1) Check if a note is played at the same time:
- if yes, then add the note to the current "chord"
2) if no, then permute all possible transitions from each note in the previous state to each note in the current state
- Add each combination to the markov chain. With transitions being represented by the each note in the previous state
transitioning to a note in the current state *with a specific duration*

'''

#begins as an empty dictionary
mc = {}

def parse(filename):
    midi = MidiFile(filename)

    current_state = []
    prev_state = []

    for track in midi.tracks:
        for message in track:
            if message.type == "set_tempo":
                tempo = message.tempo
            elif message.type == "note_on":
                # note is played at the same time
                if message.time == 0:
                    current_state.append(message.note)
                # if the note is not played at the same time, then it is the next state from the previous state
                # This means we must permute all possible transitions from notes in the previous state to notes
                # in the current state and add them to the markov chain
                else:
                    permute_transitions(prev_state, current_state, message.time, tempo, midi.ticks_per_beat)
                    prev_state = current_state
                    current_state = []



def permute_transitions(prev_state, current_state, ticks, tempo, tpb):
    for x in list(itertools.product(prev_state, current_state)):
        # add x[0]:{x[1]: [time, count]} to the Markov Chain
        if x[0] not in mc:
            mc[x[0]] = {}
            mc[x[0]][x[1]] = [duration(ticks, tempo, tpb), 1]

        # if the note has already been transitioned to, increase the transition count by 1
        # if the key is in the dict and the value is == dict[key]
        elif x[1] in mc[x[0]] and mc[x[0]][x[1]][0] == duration(ticks, tempo, tpb):
            mc[x[0]][x[1]] = [duration(ticks, tempo, tpb), mc[x[0]][x[1]][1] + 1]

        # if the note has not been transitioned to, add it to the dictionary with a count of 1
        else:
            mc[x[0]][x[1]] = [duration(ticks, tempo, tpb), 1]



# bucket to nearest 50ms
def duration(ticks, tempo, tpb):
    ms = (ticks / tpb * tempo) / 1000
    return int(ms - (ms % 50) + 50)


# convert a transition frequency matrix to a transition probability matrix
def to_probability_matrix(tfm):
    total = 0
    transitions = 0
    for keys in tfm:
        for inner_keys in tfm[keys]:
            total += tfm[keys][inner_keys][1]
            transitions += 1

    for keys in tfm:
        for inner_keys in tfm[keys]:
            tfm[keys][inner_keys][1] /= transitions


    return(tfm)


if __name__ == '__main__':
    parse('bachcontra1.mid')
    # permute_transitions(['a','b','c'], ['a', 'b', 'a'], 10, 10, 10)
    print(to_probability_matrix(mc))