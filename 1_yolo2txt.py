#! /usr/bin/env python
# coding=utf-8
# ================================================================
#
#   Author      : miemie2013
#   Created date: 2023-07-21 15:00:17
#   Description : YOLO格式注解 转换成 txt
#                 YOLO格式注解 转换成 txt。生成的txt注解文件在annotation_txt目录下。
#
# ================================================================
import os
import cv2
import json
import copy
import shutil


def convert(images_dir, annos_dir, save_path):
    images_path = os.listdir(images_dir)
    annos_path = os.listdir(annos_dir)
    assert len(images_path) == len(annos_path)
    ct = ''
    for anno_path in annos_path:
        assert anno_path.endswith('.txt')
        image_path = anno_path.replace('.txt', '.jpg')
        assert image_path in images_path
        img = cv2.imread(os.path.join(images_dir, image_path))
        h, w, c = img.shape
        ct_line = '%s' % image_path
        with open(os.path.join(annos_dir, anno_path), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                ss = line.split(' ')
                cid = int(ss[0])
                cx = float(ss[1]) * w
                cy = float(ss[2]) * h
                bbox_w = float(ss[3]) * w
                bbox_h = float(ss[4]) * h
                x0 = cx - 0.5 * bbox_w
                y0 = cy - 0.5 * bbox_h
                x1 = cx + 0.5 * bbox_w
                y1 = cy + 0.5 * bbox_h
                x0 = round(float(x0) * 10) / 10
                y0 = round(float(y0) * 10) / 10
                x1 = round(float(x1) * 10) / 10
                y1 = round(float(y1) * 10) / 10
                ct_line += ' %.1f,%.1f,%.1f,%.1f,%d' % (x0, y0, x1, y1, cid)
        ct += ct_line + '\n'
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(ct)
        f.close()


if __name__ == '__main__':
    # 自定义数据集的注解转换成coco的注解格式。只需改下面7个即可。文件夹下的子目录（子文件）用/隔开，而不能用\或\\。
    # train_path = 'annotation/voc2012_train.txt'
    # val_path = 'annotation/voc2012_val.txt'
    # test_path = None   # 如果没有测试集，填None；如果有测试集，填txt注解文件的路径。
    # classes_path = 'class_names/voc_classes.txt'
    # train_pre_path = '../VOCdevkit/VOC2012/JPEGImages/'   # 训练集图片相对路径
    # val_pre_path = '../VOCdevkit/VOC2012/JPEGImages/'     # 验证集图片相对路径
    # test_pre_path = '../VOCdevkit/VOC2012/JPEGImages/'    # 测试集图片相对路径


    # 自定义数据集的注解转换成coco的注解格式。只需改下面7个即可。文件夹下的子目录（子文件）用/隔开，而不能用\或\\。
    # train_path = 'annos_train.txt'
    # val_path = 'annos_val.txt'
    # test_path = None   # 如果没有测试集，填None；如果有测试集，填txt注解文件的路径。
    # classes_path = 'class_names/bh3_letu_classes.txt'
    # train_pre_path = 'E://bh3/letu/has_objs/'   # 训练集图片相对路径
    # val_pre_path = 'E://bh3/letu/has_objs/'     # 验证集图片相对路径
    # test_pre_path = 'E://bh3/letu/has_objs/'    # 测试集图片相对路径


    # 自定义数据集的注解转换成coco的注解格式。只需改下面7个即可。文件夹下的子目录（子文件）用/隔开，而不能用\或\\。
    train_images_dir = '../chache/train/images'
    train_annos_dir = '../chache/train/labels'
    val_images_dir = '../chache/test/images'
    val_annos_dir = '../chache/test/labels'

    # 创建json注解目录
    save_dir = 'annotation_txt/'
    if os.path.exists(save_dir): shutil.rmtree(save_dir)
    os.mkdir(save_dir)
    convert(train_images_dir, train_annos_dir, save_dir + 'train.txt')
    convert(val_images_dir, val_annos_dir, save_dir + 'val.txt')
    print('Done.')

