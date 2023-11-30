# tx-image-search
使用腾讯向量数据库进行文本/图像相似搜索

# 环境
Python 3.10.*

# 计划
- 通过文本搜索图像--已完成
- 通过图像搜索图像--待完成
- 待优化

# 项目运行
`pip install -r requirements.txt`

`python image.py`

# 功能
## 上传集合数据
train为专门上传的图片示例，可以在任何文件夹下面。只需要修改csv文件保存的路径即可，也可以使用其他方式上传。
然后运行`python upsert_data.py`数据即可上传，目前只是文本信息
## 文本搜索图像
![img.png](img/img.png)

# 关于我
我的个人主页：https://link3.cc/studiousxiaoyu

我只是一名普通打工人,热衷分享技术和开发AI工具，如果你对Java、Python开发、AI人工智能有兴趣，欢迎关注我的【灵墨AI探索室】公众号。

![img.png](img/weixin.png)