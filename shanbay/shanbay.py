#!/usr/bin/env python3

'扇贝 程序员必学电脑计算机专业英语词汇1700词爬取'

import requests
from bs4 import BeautifulSoup
import random

items = [] # 需要下载的字段
links = [] # 要使用的地址

def get_user_agent():
	'''获取随机User-Agent'''
	user_agent_list = [
		"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
	]
	ua = random.choice(user_agent_list)
	return ua

def get_html(url):
	'''下载html页面'''
	headers = {
		'User-Agent': get_user_agent()
	}
	proxies = {
		'https': 'https://114.115.218.71'
	}
	# 此项目不需User-Agent和代理，但为了笔记的完整性写上了
	try:
		r = requests.get(url, headers=headers, proxies=proxies, timeout=5)
		r.raise_for_status()
		r.encoding = r.apparent_encoding
		return r.text
	except:
		return 'error'

def get_info(url):
	'''获取html页面信息'''
	html = get_html(url)
	soup = BeautifulSoup(html, 'lxml')
	table = soup.find_all('tr', class_='row')
	
	for td in table:
		item = {} # 定义一个字典存放字段
		item['word'] = td.find('td', class_='span2').find('strong').text
		item['translate'] = ''.join(td.find('td', class_='span10').text.split('\n'))
		items.append(item) # 添加到列表中

def get_links(url):
	'''获取所有要使用的链接'''
	html = get_html(url)
	soup = BeautifulSoup(html, 'lxml')
	td = soup.find_all('td', class_='wordbook-wordlist-name')
	for a in td:
		link = a.find('a')['href']
		for i in range(1,11):
			links.append('https://www.shanbay.com' + link + '?page=' + str(i))

	for link in links:
		get_info(link)

def down_info():
	'''下载到本地文本'''
	with open('./word.txt', 'w') as f:
		for item in items:
			f.write(item['word'] + '\n' + item['translate'] + '\n\n')
		print('Download finished!\n共{}个'.format(len(items)))

if __name__ == '__main__':
	url = 'https://www.shanbay.com/wordbook/104791/' # 项目主地址
	get_links(url)
	down_info()