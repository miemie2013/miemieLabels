# -*- coding: utf-8 -*-
import sys
import cv2
import numpy as np
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter, QColor, QBrush, QPixmap, QFont
from PyQt5.QtCore import Qt
import colorsys


class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # 待标注图片的目录
        # self.images_dir = 'E://bh3/weituo/'
        # 生成的注解文件保存的目录
        # self.annos_dir = 'E://bh3/weituo_txt/'
        # self.classes = []
        # self.classes.append('锚点')

        # 待标注图片的目录
        # self.images_dir = 'E://bh3/letu/has_objs/'
        # 生成的注解文件保存的目录
        # self.annos_dir = 'E://bh3/letu/has_objs_txt/'
        # self.classes = []
        # self.classes.append('商店木屋')
        # self.classes.append('商店锚点')
        # self.classes.append('未开锚点')
        # self.classes.append('boss锚点')
        # self.classes.append('专属锚点')
        # self.classes.append('难以辨认的锚点')
        # self.classes.append('必杀')
        # self.classes.append('能量')
        # self.classes.append('低生命')
        # self.classes.append('连击')
        # self.classes.append('闪避')
        # self.classes.append('蛇')
        # self.classes.append('无伤')

        # 待标注图片的目录
        self.images_dir = 'mydataset/'
        # 生成的注解文件保存的目录
        self.annos_dir = 'mydataset_txt/'
        self.classes = []
        self.classes.append('person')
        self.classes.append('cat')


        # 暂时支持的最大类别数
        self.max_class_num = 36
        if len(self.classes) > self.max_class_num:
            print('超过支持的最大类别数！！！')


        self.resize = True
        self.resize = False
        self.scale = 1.0
        self.target_size = 800
        self.max_size = 1333
        self.h = 0
        self.w = 0


        if not os.path.exists(self.annos_dir): os.mkdir(self.annos_dir)

        self.img_names = []
        self.txt_names = []
        file_names = os.listdir(self.images_dir)
        for fname in file_names:
            if '.png' in fname:
                self.img_names.append(fname)
            elif '.jpg' in fname:
                self.img_names.append(fname)
            elif '.jpeg' in fname:
                self.img_names.append(fname)
        txt_names = os.listdir(self.annos_dir)
        for fname in txt_names:
            if '.txt' in fname:
                self.txt_names.append(fname)

        self.img_index = 0
        self.img_num = len(self.img_names)

        # 当前图片的gt框
        self.img_objs = []
        # 当前图片的注解
        self.img_anno = ''



        self.index_label = QLabel('第%d/%d张图片'%(self.img_index+1, self.img_num), self)
        self.index_label.setStyleSheet('font:20px; width:200px; height:30px;')
        self.index_label.adjustSize()
        self.index_label.move(680, 10)


        self.prebtn = QToolButton(self)
        self.prebtn.setText("上一张")
        self.prebtn.setStyleSheet('width:100px; height:30px;')
        self.prebtn.move(600, 50)
        self.prebtn.clicked[bool].connect(self.pre_img)

        self.nextbtn = QToolButton(self)
        self.nextbtn.setText("下一张")
        self.nextbtn.setStyleSheet('width:100px; height:30px;')
        self.nextbtn.move(780, 50)
        self.nextbtn.clicked[bool].connect(self.next_img)


        self.classes_label = QLabel('', self)
        classes_msg = '类别id：\n'
        for i, cl in enumerate(self.classes):
            if i < 10:
                classes_msg += '%d-%s\n'%(i, cl)
            else:
                ch = 97 + i - 10
                classes_msg += '%s-%s\n'%(chr(ch), cl)
        self.classes_label.setText(classes_msg)
        self.classes_label.setStyleSheet('font:20px; width:200px; height:30px;')
        self.classes_label.move(1350, 100)


        # 自己设置跟踪鼠标
        self.setMouseTracking(True)
        self.tuodong_ing = False
        self.cur_x = 0
        self.cur_y = 0
        self.cur_x_label = QLabel('', self)
        self.cur_y_label = QLabel('', self)
        self.cur_x_label.setStyleSheet('font:16px; width:200px; height:25px;')
        self.cur_y_label.setStyleSheet('font:16px; width:200px; height:25px;')
        self.cur_x_label.move(1500, 20)
        self.cur_y_label.move(1500, 50)

        self.grabKeyboard()  # 控件开始捕获键盘

        self.start_x = 0
        self.start_y = 0
        self.end_x = 0
        self.end_y = 0

        # 定义颜色
        self.color_num = 20
        hsv_tuples = [(1.0 * x / self.color_num, 1., 1.) for x in range(self.color_num)]
        colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
        colors = list(map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)), colors))
        self.colors = colors

        # 图片偏移
        self.image_x = 20
        self.image_y = 100

        # 上一次标注的cid
        self.last_cid = 0


        # 使用说明
        self.intro_label = QLabel('使用说明：鼠标停留在gt框4个角点附近（此时gt框会变成虚线框）时，\n按下空格键即可删除该gt框；鼠标停留在gt框4个角点附近时，按下数字\n键（类别id大于9时按下字母键）即可修改该gt框的类别id。', self)
        self.intro_label.setStyleSheet('font:16px; height:25px;')
        self.intro_label.adjustSize()
        self.intro_label.move(self.image_x, 10)
        self.D = 50         # 距离小于这个值判定为附近
        self.box_i = -111    # 在第几个gt框附近


        self.update_ui(self.img_index)

        # 设置这个窗口的位置与大小，单位是像素。
        self.frame_h = 900
        self.frame_w = 1800
        self.setGeometry(0, 30, self.frame_w, self.frame_h)
        self.setWindowTitle('目标检测标注工具')
        self.show()

    def keyPressEvent(self, e):
        # 所有键码见https://blog.csdn.net/hongsong673150343/article/details/90143896
        if e.key() == Qt.Key_0: self.change_cid(0)
        if e.key() == Qt.Key_1: self.change_cid(1)
        if e.key() == Qt.Key_2: self.change_cid(2)
        if e.key() == Qt.Key_3: self.change_cid(3)
        if e.key() == Qt.Key_4: self.change_cid(4)
        if e.key() == Qt.Key_5: self.change_cid(5)
        if e.key() == Qt.Key_6: self.change_cid(6)
        if e.key() == Qt.Key_7: self.change_cid(7)
        if e.key() == Qt.Key_8: self.change_cid(8)
        if e.key() == Qt.Key_9: self.change_cid(9)
        if e.key() == Qt.Key_A: self.change_cid(10)
        if e.key() == Qt.Key_B: self.change_cid(11)
        if e.key() == Qt.Key_C: self.change_cid(12)
        if e.key() == Qt.Key_D: self.change_cid(13)
        if e.key() == Qt.Key_E: self.change_cid(14)
        if e.key() == Qt.Key_F: self.change_cid(15)
        if e.key() == Qt.Key_G: self.change_cid(16)
        if e.key() == Qt.Key_H: self.change_cid(17)
        if e.key() == Qt.Key_I: self.change_cid(18)
        if e.key() == Qt.Key_J: self.change_cid(19)
        if e.key() == Qt.Key_K: self.change_cid(20)
        if e.key() == Qt.Key_L: self.change_cid(21)
        if e.key() == Qt.Key_M: self.change_cid(22)
        if e.key() == Qt.Key_N: self.change_cid(23)
        if e.key() == Qt.Key_O: self.change_cid(24)
        if e.key() == Qt.Key_P: self.change_cid(25)
        if e.key() == Qt.Key_Q: self.change_cid(26)
        if e.key() == Qt.Key_R: self.change_cid(27)
        if e.key() == Qt.Key_S: self.change_cid(28)
        if e.key() == Qt.Key_T: self.change_cid(29)
        if e.key() == Qt.Key_U: self.change_cid(30)
        if e.key() == Qt.Key_V: self.change_cid(31)
        if e.key() == Qt.Key_W: self.change_cid(32)
        if e.key() == Qt.Key_X: self.change_cid(33)
        if e.key() == Qt.Key_Y: self.change_cid(34)
        if e.key() == Qt.Key_Z: self.change_cid(35)

        if e.key() == Qt.Key_Space:  # 按下空格键删除gt框
            if self.box_i > -1:
                self.cur_txtname = self.img_names[self.img_index].split('.')[0]
                self.cur_txtname += '.txt'
                with open(self.annos_dir + self.cur_txtname, 'r', encoding='utf-8') as f:
                    for line in f:
                        self.img_anno = line.strip()
                ss = self.img_anno.split(' ')
                annos = ss[0]
                for j in range(1, len(ss), 1):
                    if (j-1) != self.box_i:
                        annos += ' ' + ss[j]
                self.img_anno = annos
                with open(self.annos_dir + self.cur_txtname, 'w', encoding='utf-8') as f2:
                    f2.write(self.img_anno)
                    f2.close()
            self.update_ui(self.img_index)
            # 一定要加这句实时画图，调用paintEvent()
            self.update()

    def change_cid(self, cid):
        if self.box_i > -1 and cid < len(self.classes):
            self.cur_txtname = self.img_names[self.img_index].split('.')[0]
            self.cur_txtname += '.txt'
            with open(self.annos_dir + self.cur_txtname, 'r', encoding='utf-8') as f:
                for line in f:
                    self.img_anno = line.strip()
            ss = self.img_anno.split(' ')
            annos = ss[0]
            for j in range(1, len(ss), 1):
                if (j-1) != self.box_i:
                    annos += ' ' + ss[j]
                elif (j-1) == self.box_i:
                    sss = ss[j].split(',')
                    x1 = sss[0]
                    y1 = sss[1]
                    x2 = sss[2]
                    y2 = sss[3]
                    annos += ' %s,%s,%s,%s,%d'%(x1, y1, x2, y2, cid)
                    self.last_cid = cid
            self.img_anno = annos
            with open(self.annos_dir + self.cur_txtname, 'w', encoding='utf-8') as f2:
                f2.write(self.img_anno)
                f2.close()
        self.update_ui(self.img_index)
        # 一定要加这句实时画图，调用paintEvent()
        self.update()

    def update_ui(self, index):
        self.index_label.setText('第%d/%d张图片'%(self.img_index+1, self.img_num))
        self.index_label.adjustSize()

        # 找txt注解文件
        self.cur_txtname = self.img_names[self.img_index].split('.')[0]
        self.cur_txtname += '.txt'
        if self.cur_txtname not in self.txt_names:  # 找不到就创建
            self.img_anno = '%s' % self.img_names[self.img_index]
            with open(self.annos_dir + self.cur_txtname, 'w', encoding='utf-8') as f:
                f.write(self.img_anno)
                f.close()
        # 更新self.txt_names
        self.txt_names = []
        txt_names = os.listdir(self.annos_dir)
        for fname in txt_names:
            if '.txt' in fname:
                self.txt_names.append(fname)
        # 读txt注解文件。反正只有一行。
        with open(self.annos_dir + self.cur_txtname, 'r', encoding='utf-8') as f:
            for line in f:
                self.img_anno = line.strip()

        # 更新当前图片的gt框
        self.img_objs = []
        boxes = self.img_anno.split(' ')
        if len(boxes) > 0:
            for j in range(1, len(boxes), 1):
                box = boxes[j]
                bb = box.split(',')
                x1 = int(bb[0])
                y1 = int(bb[1])
                x2 = int(bb[2])
                y2 = int(bb[3])
                cid = int(bb[4])
                tup = (x1, y1, x2, y2, cid)
                self.img_objs.append(tup)


    def pre_img(self, e):
        i = self.img_index
        if i == 0:
            self.img_index = self.img_num - 1
        else:
            self.img_index = self.img_index - 1
        self.update_ui(self.img_index)
        self.update()

    def next_img(self, e):
        i = self.img_index
        if i == self.img_num - 1:
            self.img_index = 0
        else:
            self.img_index = self.img_index + 1
        self.update_ui(self.img_index)
        self.update()

    def mouseMoveEvent(self, e):
        pos = e.windowPos()
        self.cur_x = pos.x()
        self.cur_y = pos.y()
        cx = self.cur_x - self.image_x
        cy = self.cur_y - self.image_y
        self.cur_x_label.setText('当前x：%f' %(cx))
        self.cur_y_label.setText('当前y：%f' %(cy))
        self.cur_x_label.adjustSize()
        self.cur_y_label.adjustSize()
        # 判断在第几个gt框附近
        self.box_i = -111
        min_i = 0
        min_d = 99999.0
        for j in range(0, len(self.img_objs), 1):
            box = self.img_objs[j]
            x1 = box[0]
            y1 = box[1]
            x2 = box[2]
            y2 = box[3]
            d1 = (cx - x1) ** 2 + (cy - y1) ** 2
            d2 = (cx - x2) ** 2 + (cy - y2) ** 2
            d3 = (cx - x1) ** 2 + (cy - y2) ** 2
            d4 = (cx - x2) ** 2 + (cy - y1) ** 2
            d = min(d1, d2, d3, d4)
            d = np.sqrt(d)
            if d < min_d:
                min_d = d
                min_i = j
        if min_d < self.D:
            self.box_i = min_i
        # 一定要加这句实时画图，调用paintEvent()
        self.update()

    def mousePressEvent(self, e):
        # print("mouse press")
        self.tuodong_ing = True
        pos = e.windowPos()
        self.start_x = pos.x()
        self.start_y = pos.y()
        # 一定要加这句实时画图，调用paintEvent()
        self.update()

    def mouseReleaseEvent(self, e):
        # print("mouse release")
        self.tuodong_ing = False
        pos = e.windowPos()
        self.end_x = pos.x()
        self.end_y = pos.y()
        # 写入txt注解文件
        x1 = self.start_x - self.image_x
        y1 = self.start_y - self.image_y
        x2 = self.end_x - self.image_x
        y2 = self.end_y - self.image_y
        x1 = int(x1)
        y1 = int(y1)
        x2 = int(x2)
        y2 = int(y2)
        cond1 = 0 <= x1 and x1 < self.w and 0 <= y1 and y1 < self.h
        cond2 = 0 <= x2 and x2 < self.w and 0 <= y2 and y2 < self.h
        cond3 = x1 < x2 and y1 < y2
        cond = cond1 and cond2 and cond3
        if cond:
            self.cur_txtname = self.img_names[self.img_index].split('.')[0]
            self.cur_txtname += '.txt'
            with open(self.annos_dir + self.cur_txtname, 'r', encoding='utf-8') as f:
                for line in f:
                    self.img_anno = line.strip()
            self.img_anno += ' %d,%d,%d,%d,%d'%(x1, y1, x2, y2, self.last_cid)
            with open(self.annos_dir + self.cur_txtname, 'w', encoding='utf-8') as f2:
                f2.write(self.img_anno)
                f2.close()
        self.update_ui(self.img_index)
        # 一定要加这句实时画图，调用paintEvent()
        self.update()

    def draw_rect(self, qp, color_rgb, x1, y1, x2, y2):
        col = QColor(color_rgb[0], color_rgb[1], color_rgb[2])
        qp.setPen(col)
        qp.drawLine(x1, y1, x1, y2)
        qp.drawLine(x1, y1, x2, y1)
        qp.drawLine(x2, y1, x2, y2)
        qp.drawLine(x1, y2, x2, y2)

    def draw_xuxian_rect(self, qp, color_rgb, x1, y1, x2, y2):
        col = QColor(color_rgb[0], color_rgb[1], color_rgb[2])
        qp.setPen(col)
        dy = y2 - y1
        dx = x2 - x1
        dd = min(dx, dy)
        l = dd // 9   # 虚线长度
        if dd < 10:
            l = 1

        # 画竖的虚线
        ty1 = y1
        ty2 = y1 + l
        while ty2 < y2:
            qp.drawLine(x1, ty1, x1, ty2)
            qp.drawLine(x2, ty1, x2, ty2)
            ty1 += 2*l
            ty2 += 2*l

        # 画横的虚线
        tx1 = x1
        tx2 = x1 + l
        while tx2 < x2:
            qp.drawLine(tx1, y1, tx2, y1)
            qp.drawLine(tx1, y2, tx2, y2)
            tx1 += 2*l
            tx2 += 2*l

    def draw_font(self, qp, color_rgb, x1, y1, size, text):
        col = QColor(color_rgb[0], color_rgb[1], color_rgb[2])
        qp.setPen(col)
        qp.setFont(QFont('Decorative', size))
        qp.drawText(x1, y1, text)


    def draw_line(self, qp, color_rgb, x1, y1, x2, y2):
        col = QColor(color_rgb[0], color_rgb[1], color_rgb[2])
        qp.setPen(col)
        qp.drawLine(x1, y1, x2, y2)

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)

        cur_image_path = self.img_names[self.img_index]
        cur_image_path = self.images_dir + cur_image_path

        img = cv2.imread(cur_image_path)
        self.h, self.w, _ = img.shape
        if self.resize:
            pass
        else:
            pixmap = QPixmap(cur_image_path)
            qp.drawPixmap(self.image_x, self.image_y, pixmap)
        if self.tuodong_ing:
            self.draw_rect(qp, (255, 0, 255), self.start_x, self.start_y, self.cur_x, self.cur_y)
        # 画准心
        cx = self.cur_x
        cy = self.cur_y
        self.image_x2 = self.image_x + self.w
        self.image_y2 = self.image_y + self.h
        if self.image_x < cx and cx < self.image_x2 and self.image_y < cy and cy < self.image_y2:
            self.draw_rect(qp, (0, 0, 0), cx, cy, self.image_x, cy)
            self.draw_rect(qp, (0, 0, 0), cx, cy, self.image_x2, cy)
            self.draw_rect(qp, (0, 0, 0), cx, cy, cx, self.image_y)
            self.draw_rect(qp, (0, 0, 0), cx, cy, cx, self.image_y2)
        # 画当前图片的gt框
        for j in range(0, len(self.img_objs), 1):
            box = self.img_objs[j]
            x1 = box[0]
            y1 = box[1]
            x2 = box[2]
            y2 = box[3]
            cid = box[4]
            if self.box_i == j:   # 鼠标在该gt框4个角点附近时，画虚线框
                self.draw_xuxian_rect(qp, self.colors[cid%self.color_num], self.image_x+x1, self.image_y+y1, self.image_x+x2, self.image_y+y2)
            else:
                self.draw_rect(qp, self.colors[cid%self.color_num], self.image_x+x1, self.image_y+y1, self.image_x+x2, self.image_y+y2)
            self.draw_font(qp, self.colors[cid%self.color_num], self.image_x+x1, self.image_y+y1, 18, self.classes[cid])
        qp.end()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())