#coding=utf-8
import math
from PIL import ImageFont, ImageDraw

def require(**fields):
    def _decorator(func):
        def _wrapper(*args, **kwargs):
            data = args[0]
            for field, meaning in fields.items():
                if field not in data:
                    raise ValueError('<%s>\n\tMissing field `%s`\n\tMeaning: %s' % (func.__name__, field, meaning))
            return func(*args, **kwargs)
        return _wrapper
    return _decorator


def normalized(name):
    puncts = {u'(', u'（', u'—', u'-'}
    for punct in puncts:
        if punct in name:
            return name[:name.index(punct)]
    return name

def smartdraw(img, pos_start, pos_end, text, font, font_size, font_rgba, bold=True):
    text = SBC2DBC(text)
    font = ImageFont.truetype(font=font, size=font_size)
    drawer = ImageDraw.Draw(img)
    column = math.floor((pos_end[0] - pos_start[0]) / font_size)
    row = math.ceil(len(text) / column)
    for i in range(row):
        drawer.text((pos_start[0], pos_start[1] + font_size * i), text[i * column: (i + 1) * column], font=font, fill=font_rgba)
        if bold:
            drawer.text((pos_start[0], pos_start[1] + font_size * i + 1), text[i * column: (i + 1) * column], font=font, fill=font_rgba)
            drawer.text((pos_start[0] + 1, pos_start[1] + font_size * i), text[i * column: (i + 1) * column], font=font, fill=font_rgba)
            drawer.text((pos_start[0] + 1, pos_start[1] + font_size * i + 1), text[i * column: (i + 1) * column], font=font, fill=font_rgba)

def typewriter(img, pos_start, pos_end, text, font, font_size, font_rgba, line_space=1.5, bold=True):
    # text = SBC2DBC(text)
    font = ImageFont.truetype(font=font, size=font_size)
    drawer = ImageDraw.Draw(img)
    count = 0
    pos = list(pos_start)
    while count < len(text):
        drawer.text((pos[0], pos[1]), text[count], font=font, fill=font_rgba)
        if bold:
            drawer.text((pos[0], pos[1] + 1), text[count], font=font, fill=font_rgba)
            drawer.text((pos[0] + 1, pos[1]), text[count], font=font, fill=font_rgba)
            drawer.text((pos[0] + 1, pos[1] + 1), text[count], font=font, fill=font_rgba)
        if ord(text[count]) < 0x20:
            if text[count] == '\n' and pos[0] != pos_start[0]:
                pos[1] += int(font_size * line_space)
                pos[0] = pos_start[0]
        elif 0x20 <= ord(text[count]) <= 0x7e:
            pos[0] += int(font_size / 2)
        else:
            pos[0] += font_size
        if pos[0] > pos_end[0]:
            pos[1] += int(font_size * line_space)
            pos[0] = pos_start[0]
        if pos[1] > pos_end[1]: break
        count += 1

def SBC2DBC(ustring):
    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 0x0020:
            inside_code = 0x3000
        else:
            if not (0x0021 <= inside_code and inside_code <= 0x7e):
                rstring += uchar
                continue
        inside_code += 0xfee0
        rstring += chr(inside_code)
    return rstring