from flask import Flask, Response
from render.render import *
from db.db import *
import time
app = Flask(__name__)

         
@app.route('/image/<userid>')
def index(userid):
    userjson = get_data2(str(userid))
    if userjson is None: return 'User Not Exist'
    filename = '/home/yuhui/xuetangxapi/buffer/' + str(time.time()) + '.png'
    render2(userjson, filename)
    image = file(filename)
    resp = Response(image, mimetype='image/jpeg')
    return resp

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8080)
    userjson = get_data2(str('473725'))
    render2(userjson, 'out.png')

    
