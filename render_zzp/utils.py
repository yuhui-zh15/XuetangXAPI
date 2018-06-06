#encoding=utf-8
from PIL import ImageDraw, ImageFont


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