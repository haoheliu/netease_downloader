# 网易云音乐下载器

网易云网页改版了，网页版如果没有登陆的话就不能获取完整的列表，登陆以后也只有自己创建的歌单才可以获得完整的列表。为了在这种恶劣的情况下继续我们的爬虫行为，可以分以下几步做：

1. 创建一个歌单，将想要下载的歌曲放进去（可以打开别人的歌单，然后在客户端可以批量选中后收藏到自己的歌单）。
2. 打开网易云音乐网页版，登陆，点进去这个歌单，右键，inspect，然后在最终的html中找到class="n-songtb"的div，将这一块复制下来到一个文件a。
3. 将文件a的路径填入config.json，然后python main.py就可以下载了

用之前记得装这几个包：
pip install lxml
pip install bs4

也不知道这个方法多久会过期，看网易云音乐网页版什么时候改版吧。



由于网易云音乐改版，以下内容于2020.03作废：

---

 ## 下载方法：

1. 在config.json中配置保存路径，以及要下载的歌单URL
   1. 歌单URL通过访问网易云网页版获得，如 https://music.163.com/#/playlist?id=2956036607
2. 运行 python main.py 即可开始下载



## 备注

- 如果出现下载错误，是因为这首歌需要VIP才能下载
- 使用多线程下载，多个URL并行下载
