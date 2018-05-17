import json
from collections import defaultdict
import codecs

import pymongo


client = pymongo.Connection()
db = client.xuetangx
course_stats = db.course_stats

course_info = json.load(open('course_info.json'))
course2image = json.load(open('course2image.json'))

course_db = list()
for courseid, course in course_info.items():
    course_db.append({
        'id': courseid,
        'name': course['name'],
        'about': course['about'],
        'category': course['category'],
        'image': course2image.get(courseid, None)
    })

course_stats.drop()
course_stats.insert_many(course_db)
course_stats.create_index('id')
course_stats.create_index('name')