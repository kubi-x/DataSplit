#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Oct 04, 2019

@author: kubilaykarapinar

"""
import os
import shutil
import argparse
import utils as u
import sys
import parsers as p

"""
            python3 merge_folders.py -s /Users/kubi-x/downloads/phone_aug_dataset/validation /Users/kubi-x/desktop/otheraug/validation  \
    -d /Users/kubi-x/desktop/phone_aug/validation


"""
parser = argparse.ArgumentParser(description='Split dataset into training, validation and test set')
parser._action_groups.pop()
required = parser.add_argument_group('required arguments')
optional = parser.add_argument_group('optional arguments')
required.add_argument('-s', '--source_list', nargs='+', type=str, required=True,
                      help='source directories')
required.add_argument('-d', '--destination', type=str, required=True,
                      help='source directory')
args = parser.parse_args()

source_list = args.source_list
destination = args.destination

if os.path.exists(destination):
    user_input = input('\nThis directory will be removed with what is inside and will be recreated'
                       '\nTo continue type "Yes"'
                       '\nOtherwise program will abort: ')
    if user_input != 'Yes':
        sys.exit('Abort! You entered: ' + user_input)

counter = 0
dest_img_directory = os.path.join(destination, 'images/')
dest_ann_directory = os.path.join(destination, 'annotations/')

u.re_create_folder(dest_img_directory)
u.re_create_folder(dest_ann_directory)

parser = p.PascalVocAnnParser()


def copy_2_destination(source):
    global counter
    img_directory = os.path.join(source, 'images/')
    ann_directory = os.path.join(source, 'annotations/')


    for filename in u.insensitive_glob(img_directory + '*.jpg'):
        img_name = os.path.split(filename.split('.')[0])[-1]
        new_img_name = img_name.split('_')[0]

        shutil.copy2(os.path.join(img_directory, img_name + '.jpg'),
                     os.path.join(dest_img_directory, new_img_name + '_' + str(counter) + '.jpg'))

        xml_target = os.path.join(dest_ann_directory, new_img_name + '_' + str(counter) + '.xml')
        shutil.copy2(os.path.join(ann_directory, img_name + '.xml'),
                     xml_target)

        parser.fix_image_name_in_ann(xml_target, new_img_name + '_' + str(counter) + '.jpg')

        print(counter)
        counter += 1


for s in source_list:
    print(s)
    copy_2_destination(s)
