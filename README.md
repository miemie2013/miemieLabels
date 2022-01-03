# miemieLabels

## 概述

miemieLabels是女装大佬[咩酱](https://github.com/miemie2013) 自用的目标检测标注工具，现在开源给大家使用！支持将txt标注格式导出为COCO标注格式，可以给咩酱自研检测库[miemiedetection](https://github.com/miemie2013/miemiedetection) 或者其它大部分检测库使用。


## 安装依赖

```
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

Windows可用，PyQt5提供界面支持。

## 使用说明

举一个例子说明如何用miemieLabels标注自己的数据集。假设现在我收集了一个数据集，里面有5张图片（举例说明而已，实际上需要收集更多的图片才能做成一个好的目标检测数据集），放在mydataset文件夹里。假设我想检测的类别只有人、猫这两个类别而已。

打开biaozhu.py，在initUI(self)方法里，修改self.images_dir、self.annos_dir、self.classes为自己数据集的配置。self.images_dir表示的是待标注图片的目录，比如这个例子是'mydataset/'；self.annos_dir表示的是生成的txt注解文件保存的目录，比如这个例子设置为'mydataset_txt/'；self.classes表示的是数据集的类别名，比如这个例子是'person'、'cat'，按照append的先后顺序，'person'的类别id是0，'cat'的类别id是1。

```
        # 待标注图片的目录
        self.images_dir = 'mydataset/'
        # 生成的注解文件保存的目录
        self.annos_dir = 'mydataset_txt/'
        self.classes = []
        self.classes.append('person')
        self.classes.append('cat')
```

修改完这3个变量之后，运行biaozhu.py，显示界面如下图（ui.png）所示：


![](ui.png)


可以看到第一张图片只有一个人，鼠标对准人的gt框左上角，按住鼠标左键，拖动到人的gt框右下角，松开鼠标左键，就标注好一个gt框了！但是还没有确定类别id，修改gt框的类别id很简单，鼠标停留在gt框4个角点附近（此时gt框会变成虚线框）时，按下数字键（类别id大于9时按下字母键）即可修改该gt框的类别id。类别id键（类别id大于9时变成字母键，受限于这个机制目前只支持最多36个类别的数据集标注）和类别名的对应关系在界面右边有提示。删除一个gt框也很简单，鼠标停留在gt框4个角点附近（此时gt框会变成虚线框）时，按下空格键即可删除该gt框。标注完第一张图片后，点击“下一张”按钮，进入下一张图片的标注。标注完所有图片后，进入'mydataset_txt/'文件夹，发现保存了5个txt注解文件，打开txt文件查看，发现每个文件都只有一行内容，如下所示：


```
# 000000000785.txt
000000000785.jpg 279,43,495,391,0

# 000000033759.txt
000000033759.jpg 73,60,272,456,0

# 000000039769.txt
000000039769.jpg 4,54,315,474,1 345,25,639,371,1

# 000000050811.txt
000000050811.jpg 74,66,467,493,0

# 000000051008.txt
000000051008.jpg 3,129,403,478,1
```

第一张图片的txt注解文件的内容，“000000000785.jpg”表示的是图片名，注意，仅仅是文件名而不是文件的路径！后面的“ 279,43,495,391,0”表示的是一个gt框，5个数表示1个gt框，分别为“物体左上角x坐标,物体左上角y坐标,物体右下角x坐标,物体右下角y坐标,物体类别id”，假如有多个gt框，那么它们会用空格隔开，比如000000039769.jpg这张照片，刚才你标注了两只猫。


运行1_txt2json.py会在annotation_json目录下生成两个coco注解风格的json注解文件，这是train.py支持的注解文件格式。
在config/ppyolo_2x.py里修改train_path、val_path、classes_path、train_pre_path、val_pre_path、num_classes这6个变量（自带的voc2012数据集直接解除注释就ok了）,就可以开始训练自己的数据集了。
而且，直接加载ppyolo_2x.pt的权重（即配置文件里修改train_cfg的model_path为'ppyolo_2x.pt'）训练也是可以的，这时候也仅仅不加载3个输出卷积层的6个权重（因为类别数不同导致了输出通道数不同）。
如果需要跑demo.py、eval.py，与数据集有关的变量也需要修改一下，应该很容易看懂。


## 传送门
cv算法交流q群：645796480
但是关于仓库的疑问尽量在Issues上提，避免重复解答。

B站不定时女装: [_糖蜜](https://space.bilibili.com/646843384)

本人微信公众号：miemie_2013

技术博客：https://blog.csdn.net/qq_27311165

AIStudio主页：[asasasaaawws](https://aistudio.baidu.com/aistudio/personalcenter/thirdview/165135)

欢迎在GitHub或AIStudio上关注我（求粉）~
