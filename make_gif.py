 #--------------------------------------------------------
 # import
 #--------------------------------------------------------
import os
import imghdr
import re
from PIL import Image


#--------------------------------------------------------
# define
#--------------------------------------------------------
CUR_DIR = os.path.join(os.path.dirname(__file__))
IMG_DIR = os.path.join(CUR_DIR, 'input')
OUT_PATH = CUR_DIR

#--------------------------------------------------------
# functions
#--------------------------------------------------------
class Gif:
    def __init__(self):
        self.init()

    def init(self):
        self.base_img = None
        self.imgs = []

    def add_img(self, img_path):
        if self.base_img is None:
            self.base_img = Image.open(img_path)
            self.imgs.append(self.base_img)
        else:
            self.imgs.append(Image.open(img_path))

    def add_imgs(self, img_paths):
        for img_path in img_paths:
            self.add_img(img_path)

    def save(self, out_path, duration=1, loop=0):
        self.base_img.save(out_path,
                           save_all=True,
                           append_images=self.imgs,
                           optimize=True,
                           duration=duration,
                           loop=loop)
        self.init()


def strnum_sort(list):
    return sorted(list, key=lambda x:int((re.search(r"[0-9]+", x)).group(0)))

def make_img_list(root_dir):
    img_paths = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            path = os.path.join(root, file)
            if imghdr.what(path):
                img_paths.append(path)
    return img_paths


def main():
    img_paths = strnum_sort(make_img_list(IMG_DIR))

    gif = Gif()
    gif.add_imgs(img_paths)
    out_path = os.path.join(OUT_PATH, 'test.gif')
    gif.save(out_path, duration=300)

#--------------------------------------------------------
# main
#--------------------------------------------------------
if __name__ == '__main__':
    main()
