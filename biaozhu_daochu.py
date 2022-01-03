# -*- coding: utf-8 -*-
import os

# 生成的注解文件保存的目录
# annos_dir = 'E://letu/has_objs_txt/'
# annos_dir = 'E://bh3/weituo_txt/'
annos_dir = 'mydataset_txt/'


save_name = 'annos.txt'
txt_names = os.listdir(annos_dir)


content = ''
for fname in txt_names:
    with open(annos_dir + fname, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            content += line + '\n'
with open(save_name, 'w', encoding='utf-8') as f2:
    f2.write(content)
    f2.close()






