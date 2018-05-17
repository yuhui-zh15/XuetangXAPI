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

import pymongo
client = pymongo.Connection()
# client = pymongo.MongoClient()
db = client.xuetangx # 数据库名字
user_stats = db.user_stats # 表名

def print_modifier(fun):
    def modifier(*var, **kvar):
        print 'in function %s' % fun.__name__
        return fun(*var, **kvar)
    return modifier

def load_user_profile(file_='user_profile.csv'):
    user_profile = {}
    with codecs.open(file_, encoding='utf-8') as fin:
        header = fin.readline().replace("uid", 'user_id')
        header = header.strip().split(',')
        for row in fin:
            record = dict(zip(header, row.strip().split(",")))
            user_id = record['user_id']
            user_profile[user_id] = record
    return user_profile

def load_enrollment(file_='course_enrollment.csv'):
    enrollment = {}
    with codecs.open(file_, encoding='utf-8') as fin:
        header = fin.readline().strip().split(',')
        for row in fin:
            record = dict(zip(header, row.strip().split(",")))
            user_id = record['user_id']
            if user_id not in enrollment:
                enrollment[user_id] = []
            enrollment[user_id].append(record)
    print len(enrollment)
    return enrollment

def load_course_info(file_='course_info.json'):
    course_info = {}
    with codecs.open(file_, encoding='utf-8') as fin:
        course_info = json.load(fin)

    course_ids = course_info.keys()
    for course_id in course_ids:
        category = course_info[course_id]['category']
        if not category:
            category = []
        else:
            category = json.loads(category).values()
        course_info[course_id]['category'] = category
    return course_info

def load_video_rate(file_='videorate.csv'):
    video_rate = {}
    with codecs.open(file_, encoding='utf-8') as fin:
        header = fin.readline().replace("tw_tr_datas_videorate_d.", "")
        header = header.strip().split(',')
        for row in fin:
            record = dict(zip(header, row.strip().split(",")))
            user_id = record['user_id']
            if user_id not in video_rate:
                video_rate[user_id] = []
            video_rate[user_id].append(record)

    video_watch_time = {}
    for user_id in video_rate:
        watch_time = {}
        for record in video_rate[user_id]:
            if record['course_id'] not in watch_time:
                watch_time[record['course_id']] = 0
            try:
                watch_time[record['course_id']] += float(record['study_rate']) * float(record['duration'])
            except ValueError:
                pass
        video_watch_time[user_id] = watch_time
    return video_rate, video_watch_time

def main():
    user_profile = load_user_profile()
    enrollment = load_enrollment()
    course_info = load_course_info()
    video_rate, video_watch_time = load_video_rate()
    table = []
    for user_id in user_profile:
        record = {}
        record['user_id'] = str(user_id)
        record['profile'] = user_profile[user_id]
        courses = []
        for enroll in enrollment[user_id]:
            course = {}
            course_id = enroll['course_id']
            current_course_info = course_info.get(course_id, {})
            if not current_course_info:
                continue
            course['enroll_time'] = enroll['created']
            course.update(current_course_info)
            course['watch_time'] = video_watch_time[user_id].get(course_id, 0)
            courses.append(course)
        record['courses'] = courses
        record['video'] = video_rate.get(user_id)
        table.append(record)
    return table

if __name__ == '__main__':
    if os.path.exists('table.json'):
        print 'load data'
        with codecs.open('table.json', encoding='utf-8') as fin:
            table = json.load(fin)
    else:
        table = main()
        with codecs.open('table.json', 'w', 'utf-8') as fout:
            json.dump(table, fout, indent=2, ensure_ascii=False)
    user_stats.drop()
    user_stats.insert_many(table)
    user_stats.create_index("user_id")
