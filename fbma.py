from bs4 import BeautifulSoup

f = open("C:\\Users\\kevin\\Downloads\\facebook-vitamintK\\html\\messages.htm", 'r', encoding="UTF8")

from collections import defaultdict
words = defaultdict(int)

for line in f:
	for word in line.split():
		words[word] += 1


#f.read(1000)
