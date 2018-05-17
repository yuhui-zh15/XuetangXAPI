# -*- encoding: utf-8 -*-

import codecs
import json
import os
import pickle
import random
import sys
import time

reload(sys)
sys.setdefaultencoding('utf8')

import pyhive

# https://github.com/dropbox/PyHive
from pyhive import hive
db = hive.connect(host='10.0.2.140',port=10000, database='default')

with open("uids.json") as fin:
    uids = map(lambda s: '"%s"' % s, json.load(fin))

uids = ','.join(uids)

def print_modifier(fun):
    def modifier(*var, **kvar):
        print 'in function %s' % fun.__name__
        return fun(*var, **kvar)
    return modifier

@print_modifier
def get_video():
    cursor = db.cursor()
    headers = "user_id course_id video_id study_rate duration last_access".split()
    sql = '''
        SELECT user_id
        FROM tw_tr_datas_videorate_d
        WHERE user_id IN ("473725", "6438995")
    '''
    cursor.execute(sql)
    video_rate = {}
    for record in cursor.fetchall():
        record_d = dict(zip(headers, record))
        user_id = record_d['user_id']
        del record_d['user_id']
        if user_id not in video_rate:
            video_rate[user_id] = []
        video_rate[user_id].append(record_d)

    video_watch_time = {}
    for user_id in video_rate:
        watch_time = 0
        for record in video_rate[user_id]:
            watch_time += float(record['study_rate']) * float(record['duration'])
        video_rate[user_id] = watch_time
    
    with codecs.open("video_rate.json", "w", "utf-8") as fout:
        json.dump(video_rate, fout, indent=2, ensure_ascii=False)
    
    with codecs.open("video_watch_time.json", "w", "utf-8") as fout:
        json.dump(video_watch_time, fout, indent=2, ensure_ascii=False)

@print_modifier
def get_user_info():
    cursor = db.cursor()
    headers = "uid uname gender education birth date_joined city country province city".split()
    cursor.execute('''
        SELECT %s
        FROM tw_ms_userinfo_d
        WHERE uid IN (%s)
    ''' % (','.join(headers), uids))
    user_info = {}

    for record in cursor.fetchall():
        record_d = dict(zip(headers, record))
        user_id = record_d['uid']
        del record_d['uid']
        user_info[user_id] = record_d

    with codecs.open("user_info.json", "w", "utf-8") as fout:
        json.dump(user_info, fout, indent=2, ensure_ascii=False)

@print_modifier
def get_user_enrollment():
    cursor = db.cursor()
    headers = "uid cid time".split()
    cursor.execute('''
        SELECT %s
        FROM tw_tr_datas_enrollment_d
        WHERE uid IN (%s)
    ''' % (','.join(headers), uids))
    #''' % (','.join(headers)))

    cid_index = headers.index("cid")
    headers[cid_index] = 'course_id'
    user_enrollment = {}
    for record in cursor.fetchall():
        record_d = dict(zip(headers, record))
        user_id = record_d['uid']
        del record_d['uid']
        if user_id not in user_enrollment:
            user_enrollment[user_id] = []
        user_enrollment[user_id].append(record_d)

    with codecs.open("user_enrollment.json", "w", "utf-8") as fout:
        json.dump(user_enrollment, fout, indent=2, ensure_ascii=False)

@print_modifier
def get_course_info():
    cursor = db.cursor()
    headers = "course_id name about category".split()
    cursor.execute('''
        SELECT %s
        FROM tw_ms_courseinfo_d 
    ''' % ','.join(headers))

    course_info = {}
    for record in cursor.fetchall():
        record_d = dict(zip(headers, record))
        course_id = record_d['course_id']
        del record_d['course_id']
        course_info[course_id] = record_d

    with codecs.open("course_info.json", "w", "utf-8") as fout:
        json.dump(course_info, fout, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    get_course_info()
    get_video()
    get_user_enrollment()
    get_user_info()
