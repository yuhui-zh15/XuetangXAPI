from flask import Flask, Response
from synth.synth import synth, generate
import synth.synth2 as synth2
import time
import os
app = Flask(__name__)

         
@app.route('/image/<userid>')
def index(userid):
    filename = '/home/yuhui/api/XuetangXAPI/buffer/%s.jpg' % (userid)
    if os.path.isfile(filename) == False:
        result = synth(generate(userid))
        result.save(filename)
    image = open(filename, 'rb')
    resp = Response(image, mimetype='image/jpeg')
    return resp

@app.route('/image/white/<userid>')
def white(userid):
    filename = '/home/yuhui/api/XuetangXAPI/buffer/white/%s.jpg' % (userid)
    if os.path.isfile(filename) == False:
        result = synth2.synth(synth2.generate(userid))
        result.save(filename)
    image = open(filename, 'rb')
    resp = Response(image, mimetype='image/jpeg')
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

    
