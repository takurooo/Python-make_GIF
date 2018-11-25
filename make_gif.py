#--------------------------------------------------------
# import
#--------------------------------------------------------
import os
import imghdr
import re
import argparse
from PIL import Image

#--------------------------------------------------------
# define
#--------------------------------------------------------
CUR_DIR = os.path.join(os.path.dirname(__file__))
OUT_PATH = CUR_DIR

#--------------------------------------------------------
# functions
#--------------------------------------------------------


def get_args():
    parser = argparse.ArgumentParser(description="make gif.")
    parser.add_argument("in_dir", type=str, help="in_dir")
    parser.add_argument("-d", "--duration", type=int,
                        help="duration msec", default=300)
    return parser.parse_args()


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
                           save_all=True,  # appen_imagesを全て保存
                           append_images=self.imgs,
                           optimize=False,
                           duration=duration,  # gifの表示間隔(msec)
                           loop=loop  # 何回ループするか 0なら無限ループ
                           )


def key_sort_by_num(x):
    re_list = re.findall(r"[0-9]+", x)
    re_list = list(map(int, re_list))
    return re_list


def list_from_dir(dir, target_ext=None):
    data_list = []
    fnames = os.listdir(dir)
    fnames = sorted(fnames, key=key_sort_by_num)
    for fname in fnames:
        if target_ext is None:
            path = os.path.join(dir, fname)
            data_list.append(path)
        else:
            _, ext = os.path.splitext(fname)
            if ext.lower() in target_ext:
                path = os.path.join(dir, fname)
                data_list.append(path)
    return data_list


def main(args):
    in_dir = args.in_dir
    duration_msec = args.duration

    img_paths = list_from_dir(in_dir, target_ext=('.jpg', '.png', '.bmp'))

    gif = Gif()
    gif.add_imgs(img_paths)

    out_path = os.path.join(OUT_PATH, 'out.gif')
    gif.save(out_path, duration=duration_msec)


#--------------------------------------------------------
# main
#--------------------------------------------------------
if __name__ == '__main__':
    main(get_args())
