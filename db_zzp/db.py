#encoding=utf-8
import re
import json
import codecs
from collections import defaultdict
try:
    from HTMLParser import HTMLParser   # PY2
except:
    from html.parser import HTMLParser  # PY3

import pymongo


connection = pymongo.Connection()
db = connection.xuetangx
table_user = db.user_stats
table_category = db.category_stats
table_course = db.course_stats
html_parser = HTMLParser()


def get_data1(user_id):
    record = table_user.find_one({'user_id': user_id})
    if record is None: return None

    date_joined = record['profile']['date_joined']
    year, month, day = re.findall(u'(\d{4})-(\d{2})-(\d{2}).*', date_joined)[0]

    courses = record['courses']
    n_hours = int(sum([course['watch_time'] for course in courses]) / 3600)
    n_courses = len(courses)

    return {
        'year': int(year), 'month': int(month), 'day': int(day),
        'n_hours': n_hours, 'n_courses': n_courses
    }


def get_data2(user_id):
    record = table_user.find_one({'user_id': user_id})
    if record is None: return None

    user_courses = []
    category2cnt = defaultdict(int)
    for course in record['courses']:
        user_courses.append({'name': course['name'], 'watch_time': course['watch_time'], 'category': course['category']})
        for category in course['category']:
            category2cnt[category] += 1

    if len(category2cnt) == 0:
        return { 'user_courses': user_courses, 'category_courses': [], 'max_category': None }

    max_category, max_cnt = None, 0
    for category, cnt in category2cnt.iteritems():
        if cnt > max_cnt:
            max_category = category
            max_cnt = cnt

    record = table_category.find_one({'category': max_category.encode('utf-8')})
    if record is None:
        return { 'user_courses': user_courses, 'category_courses': [], 'max_category': max_category }

    return {'user_courses': user_courses, 'category_courses': record['courses'], 'max_category': max_category}


def get_data3(user_id):
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

    max_course_description = html_parser.unescape(max_course_description)
    max_course_description = re.sub(r'</?\w+[^>]*>', '', max_course_description)
    max_course_description = re.sub('\s', '', max_course_description)
    
    record = table_course.find_one({'name': max_course_name})
    if record is None: image_file = None
    else: image_file = record['image']
    
    max_course_name = re.sub(r'\(.*?\)', '', max_course_name)
    max_course_name = re.sub(r'（.*?）', '', max_course_name)
    return { 'max_course_name': max_course_name, 'max_course_description': max_course_description, 
        'n_hours': n_hours, 'total_hours': total_hours, 'image_file': image_file }


def get_data4(user_id):
    record = table_user.find_one({'user_id': user_id})
    if record is None: return None

    n_hours = [0, 0, 0, 0, 0, 0, 0, 0]
    periods = ['0-3', '3-6', '6-9', '9-12', '12-15', '15-18', '18-21', '21-24']
    total_hours = 0
   
    dateinfo = {}
    for video in record['video']:
        date, time = video['last_access'].split(' ')
        course_id = video['course_id']
        duration = float(video['duration'])
        total_hours += duration
        hour = int(time.split(':')[0])
        if 0 <= hour < 3: n_hours[0] += duration
        elif 3 <= hour < 6: n_hours[1] += duration
        elif 6 <= hour < 9: n_hours[2] += duration
        elif 9 <= hour <= 12: n_hours[3] += duration
        elif 12 <= hour <= 15: n_hours[4] += duration
        elif 15 <= hour <= 18: n_hours[5] += duration
        elif 18 <= hour <= 21: n_hours[6] += duration
        elif 21 <= hour <= 24: n_hours[7] += duration
        if date not in dateinfo: dateinfo[date] = {}
        if course_id not in dateinfo[date]: dateinfo[date][course_id] = 0
        dateinfo[date][course_id] += duration

    n_hours = [x / 3600 for x in n_hours]
    total_hours = total_hours / 3600
    idx_period = n_hours.index(max(n_hours))

    return {
        'max_clock_interval': periods[idx_period],
        'max_clock_interval_hours': n_hours[idx_period],
        'total_hours': total_hours,
        'dateinfo': dateinfo
    }


def get_data5(user_id):
    record = table_user.find_one({'user_id': user_id})
    if record is None: return None

    data = get_data4(user_id)
    total_hours = data['total_hours']
    dateinfo = data['dateinfo']

    average_hours = total_hours / len(dateinfo)
    idx_study = 0 if average_hours < 1.0 else 1
    study_adjective = ['零碎', '连续']

    return {
        'study_adjective': study_adjective[idx_study],
        'average_hours': average_hours
    }


def get_data6(user_id):
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

    # <TODO> better course recommendation
    recommend_courses_image_file = [course['image'] for course in category_courses]
    recommend_courses_names = [course['name'] for course in category_courses]

    return {
        'recommend_courses_image_file': recommend_courses_image_file,
        'recommend_courses_names': recommend_courses_names
    }


if __name__ == '__main__':
    # print get_data('473725')
    with codecs.open('data.json', 'w', 'utf-8') as fout:
        json.dump(get_data2('709907'), fout, indent=2, ensure_ascii=False)
