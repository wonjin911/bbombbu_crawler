import os, sys
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import konlpy
import nltk
from konlpy.tag import *
from collections import Counter

bbombbu_event_url = 'http://www.ppomppu.co.kr/zboard/zboard.php?id=event&page=1&divpage=12'
root_url = 'http://www.ppomppu.co.kr/zboard/zboard.php?id=event&page='
root_url2 = '&divpage=12'

def get_url(num):
    return root_url + str(num) + root_url2

cnt = Counter()

for i in range(1, 100):
    bbombbu_event_url = get_url(i)

    with urllib.request.urlopen(bbombbu_event_url) as response:
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')

        list0 = soup.findAll("tr", {"class": "list0"}, recursive=False)
        list1 = soup.findAll("tr", {"class": "list1"}, recursive=False)
        
        final = list0 + list1

    def get_title_and_viewcnt(x):
        tmp = x.findAll('td')[3]
        tmp2 = tmp.findAll('td')
        
        return tmp.get_text(), int(tmp2[2].get_text())

    def get_nouns(sentence):
        # POS tag a sentence
        #sentence = u'만 6세 이하의 초등학교 취학 전 자녀를 양육하기 위해서는'
        words = konlpy.tag.Twitter().nouns(sentence)
        return words


    for f in final:
        title, view_cnt = get_title_and_viewcnt(f)
        items = get_nouns(title)
        print(items, view_cnt)

        for item in items:
            cnt[item] += view_cnt

print(cnt)
