#encoding=utf-8
from PIL import Image
from wordcloud import WordCloud
from utils import require, normalized, typewriter

img_dir = 'assets/images/'
font_dir = 'assets/fonts/'





data3 = [
    '其中你为____课程投入了___小时的时间，这是你学习最认真的课程。',
    '相信这门课会为你将来的成功打下坚实的基础！'
]

data4 = [
    '你总是喜欢在____的__汲取知识。',
    '你在这段时间内学习了___小时，占了你学习时间的__%。看得出来，你是个____！',
    '你喜欢利用__的时间学习。你每次平均学习__小时。',
    '还记得那天吗？____，你学了____足足____小时！'
]

data5 = [
    '你是个勤奋、自律、早睡早起、热爱生活、热爱思考、热爱文学...的人。'
    '学堂君猜测你或许还会喜欢：'
]



@require(
    name='用户名',
    year='用户注册年份',
    month='用户注册月份',
    day='用户注册日期',
    n_hours='用户学习总时长',
    n_courses='用户学习的课程总数',
    rank='超越百分比'
)
def render1(data):
    img = Image.open(img_dir + '2.png')
    typewriter(img, (160, 80), (605, 230), '亲爱的%s，\n学堂君从你%s年%s月注册那天，\n已经默默陪伴你%s天了。' % (data['name'], data['year'], data['month'], data['day']), font_dir + 'FZJL.TTF', 35, (255, 255, 255, 255))
    typewriter(img, (160, 330), (605, 480), '在这%s小时内，\n你学习了%s门课程，\n超过了全球%s%%的用户。' % (data['n_hours'], data['n_courses'], data['rank']), font_dir + 'FZJL.TTF', 35, (255, 255, 255, 255))
    img.save('out1.png')

data2 = [
    '在这卷帙浩繁的课程中，你最喜欢的课程类别是____。',
    '你在这里选修了___门课程。它们分别是：'
]

@require(
    category='课组名',
    user_courses='用户选修过的所有课程，是一个列表，其中每个元素应具有`name`和`watch_time`两个字段',
    category_courses='用户选修最多的那个课程的一部分课程，用来占位，其中每个元素应当有`name`这个字段',
)
def render2(data):
    img = Image.open(img_dir + '3.png')
    typewriter(img, (63, 80), (432, 280), '在这卷帙浩繁的课程中，\n你最喜欢的课程类别是\n%s。' % (data['category']), font_dir + 'FZJL.TTF', 35, (255, 255, 255, 255))
    typewriter(img, (63, 350), (539, 478), '你在这里选修了%s门课程。\n它们分别是：' % (len(data['user_courses'])), font_dir + 'FZJL.TTF', 35, (255, 255, 255, 255))
    img.save('out2.png')


@require(
    max_course_name='用户学习时间最长的课的名称',
    n_hours='用户学习时间最长的课的学习小时数',
    total_hours='用户学习的总小时数',
    image_file='用户学习时间最长的课的图片路径'
)
def render3(data):
    pass


@require(
    max_clock_interval='用户学习的最长时间区间', 
    max_clock_interval_hours='用户学习的最长时间区间的学习总时长', 
    total_hours='用户学习的总时长'
)
def render4(data):
    pass


if __name__ == '__main__':
    data = {
        'name': 'yuhui',
        'year': 97,
        'month': 4,
        'day': 13,
        'n_hours': 1000,
        'n_courses': 20,
        'rank': 95
    }
    render1(data)
    data = {
        'category': '计算机',
        'user_courses': {'计算机程序设计基础':100, '数据结构':80},
        'category_courses': {'操作系统', '大数据', '机器学习'}
    }
    render2(data) 
    
