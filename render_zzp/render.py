#encoding=utf-8
import random
import json

import numpy as np
from PIL import Image, ImageFont, ImageDraw
from wordcloud import WordCloud

from render_zzp.utils import require, normalized

img_dir = 'render_zzp/assets/images/'
font_dir = 'render_zzp/assets/fonts/'
courses_dir = 'render_zyh/assets/courses/'

@require(
    year='用户注册年份',
    month='用户注册月份',
    day='用户注册日期',
    n_hours='用户学习总时长',
    n_courses='用户学习的课程总数'
)
def render1(data):
    font_size = 80
    font_rgba = (102, 102, 102, 255)
    font = ImageFont.truetype(font=font_dir + 'ELEPHNT.TTF', size=font_size)

    img = Image.open(img_dir + 'template.png')
    drawer = ImageDraw.Draw(img)

    year, month, day = data['year'], data['month'], data['day']
    n_hours = data['n_hours']
    n_courses = data['n_courses']

    pos_x, pos_y = (699, 327)
    drawer.text((pos_x, pos_y), '%04d-%02d-%02d' % (year, month, day), font=font, fill=font_rgba)
    
    pos_x, pos_y = (1032, 483)
    drawer.text((pos_x, pos_y), '%3d' % n_hours, font=font, fill=font_rgba)

    pos_x, pos_y = (847, 637)
    drawer.text((pos_x, pos_y), '%2d' % n_courses, font=font, fill=font_rgba)

    img.save('out1.png')
    return img


@require(
    user_courses='用户选修过的所有课程，是一个列表，其中每个元素应具有`name`和`watch_time`两个字段',
    category_courses='用户选修最多的那个课程的一部分课程，用来占位，其中每个元素应当有`name`这个字段',
)
def render2(data):
    scale = 5
    max_courses = 100

    frequencies = { normalized(course['name']): course['watch_time'] for course in data['user_courses'] }
    for course in data['category_courses']:
        name = normalized(course['name'])
        if name not in frequencies:
            frequencies[name] = 1
            if len(frequencies) > max_courses: break

    mask = Image.open(img_dir + 'circle.png')
    width, height = mask.size
    mask = np.array(mask.resize((int(mask.size[0] / float(scale)), int(mask.size[1] / float(scale)))))
    wordcloud = WordCloud(scale=scale, background_color='white', width=int(width/float(scale)), height=int(width/float(scale)), margin=2, font_path=font_dir + 'msyhl.ttc', mask=mask) \
        .generate_from_frequencies(frequencies).to_image()

    l, t = 42, 594
    r, b = 1458, 2328
    wordcloud = wordcloud.crop((l, t, r, b))

    pos = l, t
    canvas = Image.open(img_dir + '2.png')
    canvas.paste(wordcloud, pos)

    pos = 800, 170
    font_rgba = (102, 102, 102, 255)
    font_size = 150
    font = ImageFont.truetype(font=font_dir + 'msyh.ttc', size=font_size)
    drawer = ImageDraw.Draw(canvas)
    drawer.text(pos, data['max_category'], font=font, fill=font_rgba)

    pos = 920, 400
    font_size = 120
    n_courses = len(data['user_courses'])
    font = ImageFont.truetype(font=font_dir + 'ELEPHNT.TTF', size=font_size)
    drawer = ImageDraw.Draw(canvas)
    drawer.text(pos, '%3d' % n_courses, font=font, fill=font_rgba)

    canvas.save('out2.png')
    return canvas


@require(
    max_course_name='用户学习时间最长的课的名称',
    n_hours='用户学习时间最长的课的学习小时数',
    total_hours='用户学习的总小时数',
    image_file='用户学习时间最长的课的图片路径'
)
def render3(data):
    # title
    canvas = Image.open(img_dir + '3.png')
    font_rgba = (102, 102, 102, 255)
    font_size = 150
    pos = (1260, 80)
    font = ImageFont.truetype(font=font_dir + 'msyhl.ttc', size=font_size)
    drawer = ImageDraw.Draw(canvas)
    title = u'\n'.join(u'︽' + normalized(data['max_course_name']) + u'︾')
    title_length = drawer.textsize(title, font=font)[1]
    scale = 0.9 * 2400 / title_length
    if scale < 1.0:
        font_size = int(font_size * scale)
        font = ImageFont.truetype(font=font_dir + 'msyhl.ttc', size=font_size)
    drawer.text(pos, title, font=font, fill=font_rgba)

    # hours
    pos = (636, 555)
    font_size = 120
    font = ImageFont.truetype(font=font_dir + 'ELEPHNT.TTF', size=font_size)
    drawer = ImageDraw.Draw(canvas)
    drawer.text(pos, '%4d' % data['n_hours'], font=font, fill=font_rgba)

    # percent
    pos = (960, 735)
    font_size = 70
    font = ImageFont.truetype(font=font_dir + 'ELEPHNT.TTF', size=font_size)
    drawer = ImageDraw.Draw(canvas)
    percent = int(100 * data['n_hours'] / float(data['total_hours']))
    if percent == 100: percent = 99
    drawer.text(pos, '%d%%' % percent, font=font, fill=font_rgba)

    # profile
    profile = Image.open(courses_dir + data['image_file'])
    pos = (96, 940)
    diameter = 1068
    width, height = profile.size
    scale = diameter / float(height)
    profile = profile.resize((int(scale * width), int(scale * height)), Image.ANTIALIAS)

    width, height = profile.size
    radius = height / 2
    box = (width / 2 - radius, 0, width / 2 + radius, height)
    profile = profile.crop(box)
    mask = Image.new('L', profile.size, 0)
    drawer = ImageDraw.Draw(mask)
    drawer.ellipse((0, 0, height, height), fill=255)
    profile.putalpha(mask) 
    canvas.paste(profile, pos, mask=mask)

    # play icon
    play = Image.open(img_dir + 'play.png')
    canvas.paste(play, (360, 1190), mask=play)
    canvas.save('out3.png')
    return canvas

@require(
    max_clock_interval='用户学习的最长时间区间', 
    max_clock_interval_hours='用户学习的最长时间区间的学习总时长', 
    total_hours='用户学习的总时长'
)
def render4(data):
    clock_image_dir = img_dir + 'clocks/'
    clock_intervals = ['0-3', '3-6', '6-9', '9-12', '12-15', '15-18', '18-21', '21-24']
    clock_interval_names = dict(zip(
        clock_intervals,
        [u'深夜', u'凌晨', u'清晨', u'上午', u'午后', u'下午', u'傍晚', u'晚上']
    ))
    clock_interval_comments = dict(zip(
        clock_intervals,
        [
            u'——看来你喜欢在深夜中寻找灵感',
            u'——学习虽好，记得保重身体',
            u'——看来你喜欢清晨的阳光',
            u'——看来你是位作息规律的好少年',
            u'——看来你喜欢午后的时光',
            u'——看来你习惯在下午汲取知识',
            u'——看来你习惯在傍晚汲取知识',
            u'——看来你习惯在晚上汲取知识'
        ]
    ))
    clock_interval_image_files = {
        k: clock_image_dir + k + '.png' for k in clock_intervals
    }

    # title
    canvas = Image.open(img_dir + '4.png')
    font_rgba = (102, 102, 102, 255)
    font_size = 150
    pos = (858, 126)
    font = ImageFont.truetype(font=font_dir + 'msyh.ttc', size=font_size)
    drawer = ImageDraw.Draw(canvas)
    drawer.text(pos, clock_interval_names[data['max_clock_interval']], font=font, fill=font_rgba)

    # comment
    font_size = 60
    pos = (456, 560)
    font = ImageFont.truetype(font=font_dir + 'msyh.ttc', size=font_size)
    drawer.text(pos, clock_interval_comments[data['max_clock_interval']], font=font, fill=font_rgba)

    # percent
    font_size = 100
    pos = (1164, 370)
    font = ImageFont.truetype(font=font_dir + 'ELEPHNT.TTF', size=font_size)
    percent = int(100 * data['max_clock_interval_hours'] / float(data['total_hours']))
    if percent == 1.0: percent = 99
    drawer.text(pos, '%d%%' % percent, font=font, fill=font_rgba)

    # clock
    pos = (110, 780)
    clock = Image.open(clock_interval_image_files[data['max_clock_interval']]) \
        .resize((1300, 1300), Image.ANTIALIAS)
    canvas.paste(clock, pos)

    canvas.save('out4.png')
    return canvas


def printer(img, pos, text, font_name, font_size, max_x=0):
    font_rgba = (102, 102, 102, 255)
    font = ImageFont.truetype(font=font_dir + font_name, size=font_size)
    drawer = ImageDraw.Draw(img)

    margin = 5
    cursor = [pos[0], pos[1]]
    text_width, text_height = 0, 0

    for char in text:
        text_size = drawer.textsize(char, font=font)
        if max_x > 0 and cursor[0] + text_size[0] > max_x:
            cursor = [pos[0], cursor[1] + text_size[1] + margin]
        drawer.text(cursor, char, font=font, fill=font_rgba)
        cursor[0] += text_size[0]
        text_width = max(text_width, cursor[0]) - pos[0]
        text_height = max(text_height, cursor[1] + text_size[1]) - pos[1]

    return text_width, text_height


def circlemask(img, canvas, pos, radius):
    diameter = 2 * radius
    width, height = img.size
    scale = max(diameter / float(width), diameter / float(height))
    img = img.resize((int(scale * width), int(scale * height)), Image.ANTIALIAS)
    width, height = img.size
    box = (width / 2 - radius, 0, width / 2 + radius, diameter)
    img = img.crop(box)
    mask = Image.new('L', img.size, 0)
    drawer = ImageDraw.Draw(mask)
    drawer.ellipse((0, 0, diameter, diameter), fill=255)
    img.putalpha(mask) 
    canvas.paste(img, pos, mask=mask)
    

@require(
    study_adjective='零碎/连续',
    average_hours='平均每次学习时间',
)
def render5(data):
    canvas = Image.open(img_dir + '5.png')
    printer(canvas, (870, 242), data['study_adjective'], 'msyhl.ttc', 150)
    pos = (948, 462)
    margin = 20
    text_width, text_height = printer(canvas, pos, str(int(60*data['average_hours'])), 'ELEPHNT.TTF', 85)
    printer(canvas, (pos[0] + text_width + margin, pos[1]), '分钟', 'msyhl.ttc', 85)
    canvas.save('out5.png')
    return canvas


@require(
    recommend_courses_image_file='推荐的课的图片路径',
    recommend_courses_names='推荐的课的名称'
)
def render6(data):
    canvas = Image.open(img_dir + '6.png')
    course_img0 = Image.open(courses_dir + data['recommend_courses_image_file'][0]).resize((620, 420))
    course_img1 = Image.open(courses_dir + data['recommend_courses_image_file'][1]).resize((620, 420))
    course_img2 = Image.open(courses_dir + data['recommend_courses_image_file'][2]).resize((620, 420))
    course_img3 = Image.open(courses_dir + data['recommend_courses_image_file'][3]).resize((620, 420))
    circlemask(course_img0, canvas, (180, 496), 172)
    circlemask(course_img1, canvas, (180, 905), 172)
    circlemask(course_img2, canvas, (180, 1317), 172)
    circlemask(course_img3, canvas, (180, 1728), 172)
    printer(canvas, (546, 588), data['recommend_courses_names'][0], 'msyhl.ttc', 50, max_x=1284)
    printer(canvas, (546, 996), data['recommend_courses_names'][1], 'msyhl.ttc', 50, max_x=1284)
    printer(canvas, (546, 1405), data['recommend_courses_names'][2], 'msyhl.ttc', 50, max_x=1284)
    printer(canvas, (546, 1820), data['recommend_courses_names'][3], 'msyhl.ttc', 50, max_x=1284)
    canvas.save('out6.png')
    return canvas


if __name__ == '__main__':
    pass
