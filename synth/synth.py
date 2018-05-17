from PIL import Image
import sys

'''
Synthesis multiple images into a long image
args:
@images_in: [filename1(str), filename2(str), ...]
@image_out: [filename(str)]
'''
def synth(images_in, image_out):
    images_in = [Image.open(filename) for filename in images_in]
    width, height = images_in[0].size
    result = Image.new(images_in[0].mode, (width, height * len(images_in)))
    for i, image in enumerate(images_in):
        result.paste(image, box=(0, i * height))
    result.save(image_out)


if __name__ == '__main__':
    synth(sys.argv[1:], 'result.png')