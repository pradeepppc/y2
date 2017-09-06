import requests
from bs4 import BeautifulSoup
import operator

def start(url):
    wordlist = []
    textdata = requests.get(url).text
    soup = BeautifulSoup(textdata)
    for line in soup.find_all('a',{'pg':'Author_Pos'}):
        content = line.get('title')
        print(content)
        words = content.lower().split()
        for eachword in words:
            wordlist.append(eachword)
    clean(wordlist)

def clean(wordlist):
    clean_wordlist = []
    for words in wordlist:
        symbols = "!@3$%^&*()_+{}[]|/?><./,*\'\"-+"
        for i in range(0,len(symbols)):
            words.replace(symbols[i],'')
        if len(words) > 0:
            clean_wordlist.append(words)
    create(clean_wordlist)

def create(clean_wordlist):
    wordcount = {}
    for word in clean_wordlist:
        if word in wordcount:
            wordcount[word] += 1
        else:
            wordcount[word] = 1
    for k,v in sorted(wordcount.items(),key=operator.itemgetter(1)):
        print(k,v)

start('http://blogs.timesofindia.indiatimes.com/')