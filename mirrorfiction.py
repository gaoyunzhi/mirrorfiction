#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cached_url
from bs4 import BeautifulSoup
from telegram_util import compactText
import yaml

with open('cookie') as f:
	cookie = f.read()

def findLinks(url, soup):
	chapters = set()
	for item in soup.find_all('a'):
		href = item.get('href', '')
		if url in href and len(href) > len(url) + 3:
			chapters.add(int(href.strip('/').split('/')[-1]))
	chapters = list(chapters)
	chapters.sort()
	print(chapters)
	for chapter in chapters:
		yield 'https://mirrorfiction.com/api/chapter/%d?lang=zh-Hans' % chapter

def getSoup(url):
	return BeautifulSoup(cached_url.get(url, {'cookie': cookie}, force_cache = True), 'html.parser')

def getText(link):
	content = yaml.cached_url.get(link, force_cache = True, mode = 'b')
	content = yaml.load(content, Loader=yaml.FullLoader)
	content = content['content']
	return base64.b64decode(content)

def download(url):
	soup = getSoup(url)
	title = soup.find('v-book-list')['book-name']
	result = []
	for link in findLinks(url, soup):
		result.append(getText(link))
	# with open('download/%s.txt' % novel_name, 'w') as f:
	# 	f.write(compactText(''.join(result)))
	
if __name__ == "__main__":
	download('https://mirrorfiction.com/book/18330')