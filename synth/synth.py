from PIL import Image
from render_zyh.render import *
from db_zyh.db import *
import sys

'''
Synthesis multiple images into a long image
args:
@images_in: [filename1(str), filename2(str), ...]
@image_out: [filename(str)]
'''
def synth(images):
    width, height = images[0].size
    result = Image.new(images[0].mode, (width, height * len(images)))
    for i, image in enumerate(images):
        result.paste(image, box=(0, i * height))
    return result


def generate(userid):
    image1 = render1()
    data2 = get_data2(userid)
    image2 = render2(data2)
    data3 = get_data3(userid)
    image3 = render3(data3)
    data4 = get_data4(userid)
    image4 = render4(data4) 
    data5 = get_data5(userid)
    image5 = render5(data5)
    data6 = get_data6(userid)
    image6 = render6(data6)
    image7 = render7()
    return image1, image2, image3, image4, image5, image6, image7


if __name__ == '__main__':
    images = generate('473725')
    result = synth(images)
    result.save('result.png')

