from selenium import webdriver
import requests
import json

# data
url = 'https://www.xuetangx.com/learn/SCUT00001001532/SCUT00001001532/5882928/video/9158919'  # 课程链接
chrome_locpath = r'C:\Users\填你的电脑用户名\AppData\Local\Google\Chrome\User Data'  # 本地chrome浏览器user data路径
videosrc_list = []  # 视频link列表
videotitle_list = []  # 视频标题列表

# 配置浏览器
chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument(r"user-data-dir=" + chrome_locpath)  # 把电脑原浏览器的数据传入driver
chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])  # 防止网站发现我们使用模拟器
bs = webdriver.Chrome(options=chromeOptions)
bs.get(url)
bs.implicitly_wait(20)

# 1、ul标签为单元目录；2、li标签为单元下各个小节课程标签；3、ul；4、第2个li为点击跳转视频
unit_list = bs.find_elements_by_xpath('html/body//div[@class="listScroll"]/ul')  # 单元标签列表

# 遍历每个单元
for unit in unit_list:
	bs.execute_script("arguments[0].scrollIntoView();", unit)  # 页面列表滚动到单元标签处
	if unit.get_attribute('class') == 'first':  # 若单元视频列表未被展开，则点开
		unit.click()

	# 若用于爬取其他课程，需要重新编程，以获取课程小节对应的li标签位置
	li_list = unit.find_elements_by_xpath('li')  # li标签列表
	li_num = len(li_list)  # li标签的个数
	licourse_index = 1
	xpath_span = 'ul//span'
	section_list = []  # 实际单元小节的li标签列表索引位置
	# 给不同的单元计算不同的课程小节位置
	if unit == unit_list[0]:  # 第1单元
		section_list = range(2, li_num - 1)
	elif unit == unit_list[-1] or unit == unit_list[-2]:  # 倒数第1第2单元
		section_list = range(1, li_num)
		licourse_index = 0
		xpath_span = 'span'
	else:  # 其他单元
		section_list = range(1, li_num - 1)

	# 遍历单元中的课程小节
	for secid in section_list:
		sectag = li_list[secid].find_elements_by_xpath('ul/li')[licourse_index]  # 单元下的课程小节的标签
		bs.execute_script("arguments[0].scrollIntoView();", sectag)  # 页面列表滚动到课程小节标签处

		# 获取视频标题
		title = sectag.find_element_by_xpath(xpath_span).get_attribute('innerHTML')
		title = '{}.{} '.format(unit_list.index(unit) + 1, section_list.index(secid) + 1) + title  # 重命名为“单元.小节 名称”
		videotitle_list.append(title)

		sectag.click()  # 打开该课程小节
		# bs.implicitly_wait(10)

		# 获取课程小节的视频下载链接，并加入到videosrc_list
		vtag = bs.find_element_by_xpath('html/body//video')  # 视频组件
		vsrc = vtag.get_attribute('src')
		vsrc = vsrc.split('-10.mp')[0] + '-20.mp4'  # 更改为高清视频
		videosrc_list.append(vsrc)
		print(videotitle_list)
		print(videosrc_list)

# 把videotitle_list，videosrc_list存储到本地
with open('3DGameEngineCourse_VideoInfo.json', 'w') as f:
	dpfile = [videotitle_list, videosrc_list]
	json.dump(dpfile, f, indent=4)

# 把异常link信息存储到本地
with open('3DGameEngineCourse_errLink.txt', 'w') as f:
	# 逐条检测link
	for srcurl in videosrc_list:
		rq = requests.get(srcurl)
		index = videosrc_list.index(srcurl)
		if rq.status_code != 200:  # 处理异常link
			message = videotitle_list[index] + '\tstatus code:{}\t'.format(rq.status_code) + srcurl
			print(message)
			f.write(message + '\n')
		else:  # 打印正常的link信息
			print(videotitle_list[index])
