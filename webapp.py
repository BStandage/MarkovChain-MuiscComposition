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
        return jsonify(result=key)
    except Exception as e:
        return str(e)

@app.route('/', methods = ['POST', 'GET'])
def command():
    if request.method == 'POST':
        key = request.form
        print(key)
        print(9)
        render_template('musicapp.html', key=key)




if __name__ == '__main__':
    app.run()
