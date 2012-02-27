import os, sys



CUR_PATH = os.path.dirname(__file__)

f = File(open(os.path.join(CUR_PATH, 'temp/img.jpg'),'r'))
i = Image()
i.image_field('temp',f.read())
