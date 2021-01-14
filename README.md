# 学堂在线爬虫

本爬虫用于爬取学堂在线“3D游戏引擎架构设计基础”这门课程，并将课程视频下载到本地，若用于爬取其他课程，需要重新编程，以获取课程小节对应的<li>标签位置

## 运行环境

程序中所用到的各种库、Chrome浏览器、与Chrome浏览器版本对应的webdriver（并把路径添加到PATH环境变量）

## How To Use？

1. 先在Chrome浏览器用**账号密码**登录一次学堂在线，并在浏览器弹出的窗口中选择记住密码
2. 找到Chrome浏览器的User Data本地路径，例如：C:\Users\xxx\AppData\Local\Google\Chrome\User Data
3. 更改爬虫中的`chrome_locpath`变量为步骤2得到的路径

## 原理及过程

3DGameEngineCourse_Crawler.py程序将视频标题和视频链接爬取到本地，存储到3DGameEngineCourse_VideoInfo.json文件中，并使用request来检查爬取到的链接是否能正常访问，把无法正常访问的链接信息输出到3DGameEngineCourse_errLink.txt中

3DGameEngineCourse_Downloader.py程序将从该.json文件中读取视频的标题和视频链接，把视频下载到项目中的video文件夹下，视频文件名称将使用.json中的视频标题进行命名