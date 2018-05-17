import re
import json
import datetime
import codecs
from collections import defaultdict

import pymongo


connection = pymongo.Connection()
db = connection.xuetangx
table_user = db.user_stats
table_category = db.category_stats
table_course = db.course_stats

def get_data2(user_id):
    record = table_user.find_one({'user_id': user_id})
    if record is None: return None

    name = record['profile']['uname']
    date_joined = record['profile']['date_joined']
    year, month, day = re.findall(u'(\d{4})-(\d{2})-(\d{2}).*', date_joined)[0]
    year, month, day = int(year), int(month), int(day)
    n_days = (datetime.datetime.now() - datetime.datetime(year, month, day)).days
    courses = record['courses']
    n_hours = int(sum([course['watch_time'] for course in courses]) / 3600)
    n_courses = len(courses)

    # Need better solution
    if n_hours > 1000: rank = 90
    elif n_hours > 500: rank = 80
    elif n_hours > 200: rank = 70
    elif n_hours > 150: rank = 60
    elif n_hours > 100: rank = 50
    elif n_hours > 50: rank = 40
    elif n_hours > 20: rank = 30
    elif n_hours > 10: rank = 20
    else: rank = 10

    return {
        'year': year, 'month': month, 'day': day,
        'n_hours': n_hours, 'n_courses': n_courses, 'name': name, 
        'n_days': n_days, 'rank': rank, 
    }


def get_data3(user_id):
    record = table_user.find_one({'user_id': user_id})
    if record is None: return None

    user_courses = []
    category2cnt = defaultdict(int)
    for course in record['courses']:
        user_courses.append({'name': course['name'], 'watch_time': course['watch_time'], 'category': course['category']})
        for category in course['category']:
            category2cnt[category] += 1

    max_category, max_cnt = None, 0
    for category, cnt in category2cnt.items():
        if cnt > max_cnt:
            max_category = category
            max_cnt = cnt

    record = table_category.find_one({'category': max_category})
    if record is None: category_courses = []
    else: category_courses = record['courses']

    return {'user_courses': user_courses, 'category_courses': category_courses, 'max_category': max_category, 'max_cnt': max_cnt }


def get_data4(user_id):
    record = table_user.find_one({'user_id': user_id})
    if record is None: return None

    max_course_name, max_course_description, n_hours, total_hours = None, None, 0, 0
    for course in record['courses']:
        total_hours += course['watch_time']
        if course['watch_time'] > n_hours:
            n_hours = course['watch_time']
            max_course_name = course['name']
            max_course_description = course['about']
    n_hours = int(n_hours / 3600)
    total_hours = int(total_hours / 3600)
    max_course_description = re.sub(r'</?\w+[^>]*>', '', max_course_description)

    record = table_course.find_one({'name': max_course_name})
    if record is None: image_file = None
    else: image_file = record['image']
    print(image_file)
    
    return { 'max_course_name': max_course_name, 'max_course_description': max_course_description, 
        'n_hours': n_hours, 'total_hours': total_hours, 'image_file': image_file }


def get_data5(user_id):
    record = table_user.find_one({'user_id': user_id})
    if record is None: return None

    # 0-6深夜 6-12上午 12-18下午 18-24夜晚
    period_adjective = ['万籁俱寂', '阳光明媚', '阳光正暖', '宁静闲适']
    period = ['深夜', '上午', '下午', '夜晚']
    comment = ['学习的同时也要注意身体呀', '早起的鸟儿有虫吃', '阳光下你认真思考的样子特别可爱', '在安静时思考更容易得到灵感']

    n_hours = [0, 0, 0, 0]
    total_hours = 0
   
    dateinfo = {}
    for video in record['video']:
        date, time = video['last_access'].split(' ')
        course_id = video['course_id']
        duration = float(video['duration'])
        total_hours += duration
        hour = int(time.split(':')[0])
        if 0 <= hour < 6: n_hours[0] += duration
        elif 6 <= hour < 12: n_hours[1] += duration
        elif 12 <= hour < 18: n_hours[2] += duration
        elif 18 <= hour <= 24: n_hours[3] += duration
        if date not in dateinfo: dateinfo[date] = {}
        if course_id not in dateinfo[date]: dateinfo[date][course_id] = 0
        dateinfo[date][course_id] += duration

    n_hours = [n_hours[0] / 3600, n_hours[1] / 3600, n_hours[2] / 3600, n_hours[3] / 3600]
    total_hours = total_hours / 3600

    study_adjective = ['零碎', '连续']
    
    max_date, max_course, max_hours = None, None, 0
    for date in dateinfo:
        for course in dateinfo[date]:
            if dateinfo[date][course] > max_hours:
                max_date = date
                max_course = course
                max_hours = dateinfo[date][course]
    max_hours = max_hours / 3600

    average_hours = total_hours / len(dateinfo)
    
    idx_period = n_hours.index(max(n_hours))
    idx_study = 0 if average_hours < 1.0 else 1

    record = table_course.find_one({'id': max_course})
    if record is not None: max_course = record['name']

    return { 'period_adjective': period_adjective[idx_period], 'period': period[idx_period], 'n_hours': n_hours[idx_period],
        'total_hours': total_hours, 'comment': comment[idx_period], 'study_adjective': study_adjective[idx_study],
        'average_hours': average_hours, 'max_date': max_date, 'max_course': max_course,
        'max_hours': max_hours
    }


def get_data6(user_id):
    record = table_user.find_one({'user_id': user_id})
    if record is None: return None

    # <TODO> better user tagging
    characteristic = ['聪明勤奋','严于律己','热爱思考','热爱文学','热爱艺术']

    user_courses = []
    category2cnt = defaultdict(int)
    for course in record['courses']:
        user_courses.append({'name': course['name'], 'watch_time': course['watch_time'], 'category': course['category']})
        for category in course['category']:
            category2cnt[category] += 1

    max_category, max_cnt = None, 0
    for category, cnt in category2cnt.items():
        if cnt > max_cnt:
            max_category = category
            max_cnt = cnt

    record = table_category.find_one({'category': max_category})
    if record is None: category_courses = []
    else: category_courses = record['courses']

    # <TODO> better course recommendation
    recommend_courses_image_file = [course['image'] for course in category_courses]

    return {
        'characteristic': characteristic,
        'recommend_courses_image_file': recommend_courses_image_file
    }


if __name__ == '__main__':
    pass