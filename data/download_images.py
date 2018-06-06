import urllib.request
import urllib.parse
import requests
import json
import codecs
import os
import traceback

course_id2url = json.load(open('course2url.json'))


def timeout(func, args=(), kwargs={}, timeout_duration=1, default=None):
    import signal

    class TimeoutError(Exception):
        pass

    def handler(signum, frame):
        raise TimeoutError()

    # set the timeout handler
    signal.signal(signal.SIGALRM, handler) 
    signal.alarm(timeout_duration)
    try:
        result = func(*args, **kwargs)
    except TimeoutError as exc:
        print('Timeout')
        result = default
    finally:
        signal.alarm(0)

    return result


def get_image(course_id, image_url, image_filename, fout):
    try:
        if 'https://' in image_url:
            image_url = 'https://' + urllib.parse.quote(image_url.replace('https://', ''))
        elif 'http://' in image_url:
            image_url = 'http://' + urllib.parse.quote(image_url.replace('http://', ''))
        head = {}
        head['User-Agent'] = 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19'
        req = urllib.request.Request(image_url, headers=head)
        with urllib.request.urlopen(req) as resp, open('course_images/' + image_filename, 'wb') as fimage:
            fimage.write(resp.read())
        fout.write('%s\t%s\n' % (course_id, image_filename))
        fout.flush()
        return 0
    except Exception as e:
        print(e)
        return -1

cnt = 0
with open('error.txt', 'w', encoding='utf-8') as ferr, open('course2image.txt', 'w', encoding='utf-8') as fout:
    for i, (course_id, image_url) in enumerate(course_id2url.items()):
        if i % 10 == 0: print(i, '/', len(course_id2url))
        image_url = image_url
        file_ext = image_url[image_url.rfind('.'):]
        image_id = cnt
        cnt += 1
        image_filename = '%s%s' % (image_id, file_ext)
        errcode = timeout(get_image, args=(course_id, image_url, image_filename, fout), timeout_duration=5, default=-1)
        # errcode = get_image(course_id, image_url, image_filename, fout)
        if errcode == -1:
            errinfo = '%d\t%s\t%s\n' % (image_id, course_id, image_url)
            ferr.write(errinfo)
            ferr.flush()
            print(errinfo)
        