from flask import Flask, Response
from synth.synth import synth, generate
import time
app = Flask(__name__)

         
@app.route('/image/<userid>')
def index(userid):
    result = synth(generate(userid))
    filename = '/home/yuhui/xuetangxapi/buffer/' + str(time.time()) + '.png'
    result.save(filename)
    image = file(filename)
    resp = Response(image, mimetype='image/jpeg')
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

    
