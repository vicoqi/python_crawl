# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt                          #数学绘图库  
from PIL import Image  
import numpy as np                                      #科学数值计算包，可用来存储和处理大型矩阵  
import jieba                                            #分词库  
from wordcloud import WordCloud, ImageColorGenerator   #词云库  
  
#1、读入txt文本数据  
text = open(r'E:\gtihubresposity-my\java_spider\java-crawl\java_spider\src\main\resources\file\aa.txt',encoding='utf-8').read()  
  
# 2、结巴分词:cut_all参数可选, True为全模式，False为精确模式,默认精确模式  
cut_text= jieba.cut(text,cut_all=False)  
result= "/".join(cut_text)#必须给个符号分隔开分词结果,否则不能绘制词云  
  
#3、初始化自定义背景图片  
image = Image.open(r'D:\pythonworkspace\word-cloud\back.jpg')  
graph = np.array(image)  
  
#4、产生词云图  
#有自定义背景图：生成词云图由自定义背景图像素大小决定  
wc = WordCloud(font_path=r"D:\Python\Python35-32\worl_cloud\Monaco Yahei.ttf",background_color='white',max_font_size=50,mask=graph)  
wc.generate(result)  
  
#5、绘制文字的颜色以背景图颜色为参考  
image_color = ImageColorGenerator(graph)#从背景图片生成颜色值  
wc.recolor(color_func=image_color)  
wc.to_file(r"D:\pythonworkspace\word-cloud\wordcloud2.png") #按照背景图大小保存绘制好的词云图，比下面程序显示更清晰  
  
# 6、显示图片  
plt.figure("词云图")   #指定所绘图名称  
plt.imshow(wc)         # 以图片的形式显示词云  
plt.axis("off")       # 关闭图像坐标系  
plt.show()  