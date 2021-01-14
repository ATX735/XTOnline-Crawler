import json
import requests

videoinfo_locpath = '3DGameEngineCourse_VideoInfo.json'  # 包含视频src和title的文件的路径
videostorage_locpath = 'video\\'  # 下载到的视频的存储路径

# 读取爬虫爬取到的数据
with open(videoinfo_locpath, 'r') as f:
	vinfodata = json.load(f)
	vtitle = vinfodata[0]  # 视频标题
	vsrc = vinfodata[1]  # 视频link


# 下载视频并保存到本地
for title, src in zip(vtitle, vsrc):
	rq = requests.get(src)
	# 显示进度
	if rq.status_code!=200:  # 若请求不成功，则放弃并继续
		print(title+'\tstatus code:{}\t'.format(rq.status_code)+src)
		continue
	else:
		print(title+'\tdownload complete')

	# 把视频存储到本地
	with open(videostorage_locpath + title + '.mp4', 'wb') as f:
		f.write(rq.content)

