import json
from collections import defaultdict
import codecs

import pymongo

client = pymongo.Connection()
db = client.xuetangx
category_stats = db.category_stats

category2courses = defaultdict(list)
course_info = json.load(open('course_info.json'))
course2image = json.load(open('course2image.json'))

for course_id, course in course_info.items():
    if course['category'] is None: continue
    categories = [x[1] for x in json.loads(course['category']).items()]
    for category in categories:
        category2courses[category].append({
            'course_id': course_id,
            'name': course['name'],
            'image': course2image.get(course_id, None)
        })

category_db = list()
for category, courses in category2courses.items():
    category_db.append({
        'category': category,
        'courses': courses
    })

with codecs.open('category.json', 'w', 'utf-8') as fout:
    json.dump(category2courses, fout, indent=2, ensure_ascii=False)
category_stats.drop()
category_stats.insert_many(category_db)
category_stats.create_index('category')