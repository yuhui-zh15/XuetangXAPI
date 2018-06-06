from flask import Flask, Response
from synth.synth import synth, generate
import time
import os
app = Flask(__name__)

         
@app.route('/image/<userid>')
def index(userid):
    filename = '/home/yuhui/api/XuetangXAPI/buffer/%s.png' % (userid)
    if os.path.isfile(filename) == False:
        result = synth(generate(userid))
        result.save(filename)
        #print('Drawing')
    image = open(filename, 'rb')
    resp = Response(image, mimetype='image/jpeg')
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

    
