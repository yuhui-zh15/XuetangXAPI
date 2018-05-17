#encoding=utf-8
from PIL import Image
from wordcloud import WordCloud
from render_zyh.utils import require, typewriter, normalized
import matplotlib.pyplot as plt
import random

img_dir = 'render_zyh/assets/images/'
font_dir = 'render_zyh/assets/fonts/'

def render1():
    img = Image.open(img_dir + '1.png')
    return img


@require(
    name='用户名',
    year='用户注册年份',
    month='用户注册月份',
    day='用户注册日期',
    n_days='注册至今时间',
    n_hours='用户学习总时长',
    n_courses='用户学习的课程总数',
    rank='超越百分比'
)
def render2(data):
    img = Image.open(img_dir + '2.png')
    typewriter(img, (160, 80), (605, 230), '亲爱的%s，\n学堂君从%s-%s-%s那天起，\n已经默默陪伴你%s天了。' % (data['name'], data['year'], data['month'], data['day'], data['n_days']), font_dir + 'FZJL.TTF', 35, (255, 255, 255, 255))
    typewriter(img, (160, 310), (605, 510), '在这%s天里，\n你投入了%s小时，\n学习了%s门课程，\n超过了全球%s%%的用户。' % (data['n_days'], data['n_hours'], data['n_courses'], data['rank']), font_dir + 'FZJL.TTF', 35, (255, 255, 255, 255))
    return img


@require(
    max_category='课组名',
    max_cnt='课组选课数',
    user_courses='用户选修过的所有课程，是一个列表，其中每个元素应具有`name`和`watch_time`两个字段',
    category_courses='用户选修最多的那个课程的一部分课程，用来占位，其中每个元素应当有`name`这个字段',
)
def render3(data):
    def white_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        return "rgb(255,255,255)"
    img = Image.open(img_dir + '3.png')
    typewriter(img, (63, 80), (432, 280), '在这卷帙浩繁的课程中，\n你最喜欢的课程类别是\n%s。' % (data['max_category']), font_dir + 'FZJL.TTF', 35, (255, 255, 255, 255))
    typewriter(img, (63, 350), (539, 478), '你在这里选修了%s门课程。\n它们分别是：' % (data['max_cnt']), font_dir + 'FZJL.TTF', 35, (255, 255, 255, 255))
    max_courses = 20
    frequencies = {}
    
    for course in data['user_courses']:
        if len(frequencies) > max_courses: break
        name = normalized(course['name'])
        for category in course['category']:
            if category == data['max_category']:
                frequencies[name] = course['watch_time'] / 3600 + 1
                break
        
    for course in data['category_courses']:
        if len(frequencies) > max_courses: break
        name = normalized(course['name'])
        if name not in frequencies: frequencies[name] = 1
        

    wordcloud = WordCloud(scale=1, mode='RGBA', background_color=None, width=395, height=270, font_path=font_dir + 'HT.otf') \
        .generate_from_frequencies(frequencies).recolor(color_func=white_color_func).to_image()
    img.paste(wordcloud, (120, 570), wordcloud)
    return img


@require(
    max_course_name='用户学习时间最长的课的名称',
    max_course_description='用户学习时间最长的课的课程简介',
    n_hours='用户学习时间最长的课的学习小时数',
    total_hours='用户学习的总小时数',
    image_file='用户学习时间最长的课的图片路径'
)
def render4(data):
    img = Image.open(img_dir + '4.png')
    typewriter(img, (175, 75), (560, 275), '其中你为%s课程投入了%s小时的时间，这是你学习最认真的课程。' % (data['max_course_name'], data['n_hours']), font_dir + 'FZJL.TTF', 35, (255, 255, 255, 255))
    typewriter(img, (90, 570), (550, 750), data['max_course_description'], font_dir + 'HT.otf', 14, (255, 255, 255, 255), bold=False)
    typewriter(img, (60, 765), (560, 885), '相信这门课会为你将来的成功打下坚实的基础！', font_dir + 'FZJL.TTF', 35, (255, 255, 255, 255))
    return img


@require(
    period_adjective='时间段形容词',
    period='用户学习时间段',
    n_hours='该时间段学习时间',
    total_hours='用户总共学习时间',
    comment='针对用户学习时间的评价',
    study_adjective='零碎/连续',
    average_hours='平均每次学习时间',
    max_date='单次学习最长日期',
    max_course='单次学习最长课程',
    max_hours='单次学习最长时间'
)
def render5(data):
    img = Image.open(img_dir + '5.png')
    typewriter(img, (120, 90), (560, 220), '你总是喜欢在%s的%s汲取知识。' % (data['period_adjective'], data['period']), font_dir + 'FZJL.TTF', 35, (255, 255, 255, 255))
    typewriter(img, (50, 260), (590, 470), '你在这段时间内学习了%.0f小时，\n占了你学习时间的%.0f%%。\n%s！' % (data['n_hours'], int(100 * data['n_hours'] / data['total_hours']), data['comment']), font_dir + 'FZJL.TTF', 35, (255, 255, 255, 255))
    typewriter(img, (50, 500), (500, 630), '你喜欢利用%s的时间学习。\n你平均每天学习%.0f分钟。' % (data['study_adjective'], 60 * data['average_hours']), font_dir + 'FZJL.TTF', 35, (255, 255, 255, 255))
    typewriter(img, (50, 680), (590, 900), '还记得那天吗？\n%s，\n你学了%s足足%.0f分钟！' % (data['max_date'], data['max_course'], 60 * data['max_hours']), font_dir + 'FZJL.TTF', 35, (255, 255, 255, 255))    
    return img


@require(
    characteristic='用户品质',
    recommend_courses_image_file='推荐的课的图片路径'
)
def render6(data):
    img = Image.open(img_dir + '6.png')
    typewriter(img, (75, 155), (560, 400), '你是个%s的人~' % ('、'.join(data['characteristic'])), font_dir + 'FZJL.TTF', 35, (255, 255, 255, 255))
    typewriter(img, (75, 415), (560, 480), '学堂君猜测你或许还会喜欢：', font_dir + 'FZJL.TTF', 35, (255, 255, 255, 255))
    return img


def render7():
    img = Image.open(img_dir + '7.png')
    return img
    

if __name__ == '__main__':
    pass
    # data = {
    #     'name': 'yuhui',
    #     'year': 97,
    #     'month': 4,
    #     'day': 13,
    #     'n_hours': 1000,
    #     'n_courses': 20,
    #     'rank': 95
    # }
    # render1(data)
    # data = {
    #     'category': '计算机',
    #     'user_courses': {'计算机程序设计基础':100, '数据结构':80},
    #     'category_courses': {'操作系统', '大数据', '机器学习'}
    # }
    # render2(data) 
    # data = {
    #     'max_course_name': '毛泽东思想与中国特色社会主义理论体系',
    #     'n_hours': 100,
    #     'total_hours': 200,
    #     'image_file': 'os.png'
    # }
    # render3(data) 
    # data = {
    #     'period_adjective': '阳光明媚',
    #     'period': '清晨',
    #     'n_hours': 100,
    #     'total_hours': 200,
    #     'comment': '早起的鸟儿有虫吃',
    #     'study_adjective': '零碎',
    #     'average_hours': 1.5,
    #     'max_date': '2018年4月13日',
    #     'max_course': '操作系统',
    #     'max_hours': 10
    # }
    # render4(data)
    # data = {
    #     'characteristic': ['勤奋','自律','早睡早起','热爱生活','热爱思考','热爱文学'],
    #     'recommend_courses_image_file': ['os.png', 'ds.png', 'os.png', 'ds.png']
    # }
    # render5(data)
    
