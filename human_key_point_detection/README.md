# 基于Tkinter和百度Aip的人体关键点检测



## :paperclip:  ​项目简介

​       本文通过调用百度开放的人体关键点检测API，实现关键点检测并将其在Python的轻量级GUI库Tkinter绘制出来。当然最直接的方法是直接用opencv显示出来，但是我们更多的时候需要进行交互，因此使用Tkinter。



## :paperclip:  功能介绍

- 可以检测单张图片的关键点（测试用）

- 可以对视频进行关键点检测（TKinter界面）

  

## :paperclip:  使用说明

1. 在[百度智能云](https://login.bce.baidu.com/?account=)上注册账号，然后创建应用，获取对应的 APP_ID、API_KEY、SECRET_KEY
2. 在python环境中下载baidu-aip，指令如下

```
pip install baidu-aip
```

3. 把获取的 APP_ID、API_KEY、SECRET_KEY，配置到config.py中。
4. 调整图片路径，运行aip_bodyanalysis.py，可以得到单张图的关键点检测图

<img src='./data/test_ok.jpg'>

5.调整视频路径，运行tkinter_body.py，可以在tkinter界面展示。



## :paperclip:  主要参考

[1] <http://www.chenjianqu.com/show-104.html>



## :paperclip:  此外

喜欢的朋友请点点 star，关注我的[CSDN](https://mp.csdn.net/console/article)博客，关注我的[哔哩哔哩](https://space.bilibili.com/424394389?spm_id_from=333.788.b_765f7570696e666f.1)，关注我的公众号CV伴读社

<div align=center><img src="https://github.com/xiaoxuebajie/LeetCode/raw/master/solution_python/images/qrcode.jpg" style='zoom:100%'>

