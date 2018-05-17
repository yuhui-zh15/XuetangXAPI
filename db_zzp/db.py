import re
import json
import codecs
from collections import defaultdict

import pymongo


connection = pymongo.Connection()
db = connection.xuetangx
table_user = db.user_stats
table_category = db.category_stats


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


if __name__ == '__main__':
    # print get_data('473725')
    with codecs.open('data.json', 'w', 'utf-8') as fout:
        json.dump(get_data2('709907'), fout, indent=2, ensure_ascii=False)
