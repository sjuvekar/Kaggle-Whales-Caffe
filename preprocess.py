# ----------------------------------------------------------------------------
# Copyright 2015 Nervana Systems Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ----------------------------------------------------------------------------
"""
Borrowed from Anil's code @
"""
import numpy as np
import sys
from PIL import Image
import glob
import math
import os
import errno
# import getopt
import argparse


def symlink_force(target, link_name):
    try:
        os.symlink(target, link_name)
    except OSError, e:
        if e.errno == errno.EEXIST:
            os.remove(link_name)
            os.symlink(target, link_name)
        else:
            raise e


def read_coord(filename):
    coord = {}

    with open(filename) as f:
        for line in f:
            impath, value = line.split()
            dir_path, imname = os.path.split(impath)
            coord[imname] = float(value)

    return coord


# Use coordinates of the images to create masks
def create_mask(imname, point_num=1):

    mask = np.zeros((imwidth, imwidth))

    width = imwidth/60  # TODO: WHY ?

    assert point_num is 1 or point_num is 2

    if point_num == 1:
        xc = int(round(point1_x[imname] * imwidth /imsize_[imname][0]))
        yc = int(round(point1_y[imname] * imwidth /imsize_[imname][1]))
    else:
        xc = int(round(point2_x[imname] * imwidth /imsize_[imname][0]))
        yc = int(round(point2_y[imname] * imwidth /imsize_[imname][1]))

    xstart = 0 if xc <= width else xc - width
    ystart = 0 if yc <= width else yc - width
    xend = imwidth if imwidth - xc <= width else xc + width + 1
    yend = imwidth if imwidth - yc <= width else yc + width + 1
    for x in range(xstart, xend):
        for y in range(ystart, yend):
            dist = math.hypot(xc - x, yc - y)
            if dist >= width:
                continue
            mask[x, y] = (1 - dist / width)

    return mask


# Resize the given images to (imwidth X imwidth) and create masks for train-set
def proc_imgs(imgdir=None, gen_mask=1):

    dst_dir = data_dir_prefix + "_" + str(imwidth) + "/" + imgdir

    mask1_dir = dst_dir + "_points1_mask"
    mask2_dir = dst_dir + "_points2_mask"

    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    if gen_mask:
        if not os.path.exists(mask1_dir):
            os.makedirs(mask1_dir)

        if not os.path.exists(mask2_dir):
            os.makedirs(mask2_dir)

    pattern = data_dir_prefix + "/" + imgdir + "/*.jpg"
    for file in glob.glob(pattern):
        src_path, fname = os.path.split(file)

        im = Image.open(file)

        scale_factor = imwidth / np.float32(min(im.size))
        imsize_[fname] = im.size

        filt = Image.BICUBIC if scale_factor > 1 else Image.ANTIALIAS
        im = im.resize((imwidth, imwidth), filt)

        dst_path = dst_dir + "/" + fname
        im.save(dst_path, "JPEG")

        if gen_mask:
            mask1 = create_mask(fname, point_num=1)
            mask2 = create_mask(fname, point_num=2)

            im_mask1 = Image.fromarray(np.uint8(mask1*255))
            im_mask2 = Image.fromarray(np.uint8(mask2*255))

            mask1_path = mask1_dir + "/" + fname
            mask2_path = mask2_dir + "/" + fname

            im_mask1.save(mask1_path, "JPEG")
            im_mask2.save(mask2_path, "JPEG")


# Create points.txt, mask1.txt and mask2.txt under images_384/
# These text files are used as "source" for data and labels
def create_source_files(imgdir, gen_mask=1):

    images_dir = images_dir_prefix + "_" + str(imwidth) + "/"

    if not os.path.exists(images_dir):
        os.makedirs(images_dir)

    if gen_mask:
        points_fname = images_dir + "train_points.txt"
        mask1_fname = images_dir + "mask_point1.txt"
        mask2_fname = images_dir + "mask_point2.txt"

        points_ = open(points_fname, 'w')
        mask1_ = open(mask1_fname, 'w')
        mask2_ = open(mask2_fname, 'w')
    else:
        points_fname = images_dir + "test_points.txt"
        points_ = open(points_fname, 'w')

    pattern = data_dir_prefix + "/" + imgdir + "/*.jpg"
    for file in glob.glob(pattern):

        dir_path, imname = os.path.split(file)

        new_dir_path = data_dir_prefix + "_" + str(imwidth) + "/"
        if gen_mask:
            points_.write(new_dir_path + "train/" + imname + " 0\n")

            mask1_.write(new_dir_path + "train_points1_mask/" + imname + " 0\n")
            mask2_.write(new_dir_path + "train_points2_mask/" + imname + " 0\n")
        else:
            points_.write(new_dir_path + "test/" + imname + " 0\n")

    points_.close()
    if gen_mask:
        mask1_.close()
        mask2_.close()

    # Create symbolic links
    symlink_force("../" + points_fname, images_dir_prefix + "/" + imgdir + "_points.txt")
    if gen_mask:
        symlink_force("../" + mask1_fname, images_dir_prefix + "/" + "mask_point1.txt")
        symlink_force("../" + mask2_fname, images_dir_prefix + "/" + "mask_point2.txt")


# Read command line args
parser = argparse.ArgumentParser()
parser.add_argument('--imwidth', type=int, default=384, help='Image width/height')
args = parser.parse_args()

# Resize images to IMWIDTH x IMWIDTH
imwidth = int(args.imwidth)

data_dir_prefix = "data"  # Directory containing train, test, traincrops
images_dir_prefix = "images"

# Create dictionaries of coordinates (of original sized train_images)
point1_x = read_coord("images/point1_x.txt")
point1_y = read_coord("images/point1_y.txt")
point2_x = read_coord("images/point2_x.txt")
point2_y = read_coord("images/point2_y.txt")

# Dictionary of {image->imsize} (list: width, height) of train & test - Original sized images
imsize_ = {}

proc_imgs("train", gen_mask=1)
proc_imgs("test", gen_mask=0)

create_source_files("train", gen_mask=1)
create_source_files("test", gen_mask=0)
