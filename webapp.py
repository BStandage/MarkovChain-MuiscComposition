from flask import Flask, render_template, request, jsonify
from Track import Track

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('musicapp.html')

@app.route('/_background_process')
def _background_process():
    try:
        key = request.args.get('key')
        track1 = Track('voice 1', 'soprano', 100)
        track1.build_track()
        track_list = [track1]
        track1.write(track_list, 'testTrack1.2.mid')
        notes = []
        for i in track1.track[0]:
            notes.append(i)
        print()
        return jsonify(result=key)

        #return jsonify(result=key)
    except Exception as e:
        return str(e)




if __name__ == '__main__':
    app.run()
