import MySQLdb
import urllib2
import ssl
from bs4 import BeautifulSoup
import os
import Queue
import requests
import re

#ignore ssl certification errors
ctx=ssl.create_default_context()
ctx.check_hostname=False
ctx.verify_mode=ssl.CERT_NONE

headers={'User-agent' : "Mozilla/5.0"}

found={}
words={}
ct={}

wid=0
urlid=0

f = open("links.txt","w")
linkx=0

def crawldfs(url):

	global linkno

	if(linkno > 200):
		return

	if(url == None):
		return

	if(("https://en.wikipedia.org"+url) in found ):
		print("YES")
		return

	if(url.find("/wiki/") != 0 or url.find("(") != -1 or url.find(":") != -1 or url.find("/wiki/IEEE") != -1 or url.find("/wiki/ISO") != -1):
		return


	try:
		url="https://en.wikipedia.org"+url
		
		req=urllib2.Request(url,None,headers)

		page=urllib2.urlopen(req)

		cont=page.read()

	except:

		return

	found[url]=1;

	print(url)

	linkno+=1
	
	f.write(url+"\n")

	bsoup = BeautifulSoup(cont,"html.parser")

	anchor = bsoup('a')
	
	pos = 0
	for link in anchor:
		pos += 1
		if(pos < 30):
			continue
		crawldfs(link.get('href',None))


def crawlbfs(urlbegin,db):

	global wid
	global urlid
	global linkx 

	q=Queue.Queue()
	
	q.put(urlbegin)

	while(not q.empty()):
		
		url=str(q.get())
		#print(url)

		if(type(url)!=type("HELLO")):
			print("HELLO")
			continue

		if(url == None or ("https://en.wikipedia.org"+ str(url)) in found ):
			continue

		if(url.find("/wiki/") != 0 or url.find("(") != -1 or url.find(":") != -1 or url.find("/wiki/IEEE") != -1 or url.find("/wiki/ISO") != -1):
			continue


		url="https://en.wikipedia.org"+url
		
		req=requests.get(url)
	
		if url not in found:
			urlid+=1
			comd="INSERT INTO URLS VALUES ("+str(urlid)+","+'"'+url+'"'+");"
			x=db.cursor()
			x.execute(comd)
			db.commit()
			#print(comd)
			print(urlid)

		found[url]=1;

		#print(url)

		linkx+=1
	
		#f.write(url+"\n")

		if(linkx > 1000):
			return

		bsoup = BeautifulSoup(req.content,"html.parser")

		anchor = bsoup('a')

		#lst = ["".join(s(text = True)) for s in bsoup('p')]

		#wordlist = " ".join(lst)

		
		#print(url+ "HELLO")

		linkno =0
		for link in anchor:
			linkno+=1
			if linkno<10:
				continue
			try:								
				q.put(str(link.get('href',None)))
				#print(link.get('href',None))			
			except:
				pass	

		"""
		flist = wordlist.split()
	
			#print(flist)
		pos = 0
		for word in flist:
			pos += 1
			if(pos< 30):
				continue
			if(pos>150):
				break
			if(word[-1]==',' or word[-1]=='.'):
				word=word[0:-1]

		
			if word.isalpha():		
					done=0
					if word not in words:
						try:			
							table = db.cursor()
							comd =  "INSERT INTO WORDS VALUES("+str(wid)+","+'"'+word+'"'+");"
							wid+=1
							if(wid % 1000 ==0):
								print(wid)
							if(wid > 10000):
								return
							#print(comd)
							#print(wid)							
							table.execute(comd)	
							db.commit()	
						except:
							done=1
							pass	
					if(done == 0):
						wordno=0
						table = db.cursor()
						comd="SELECT WORDID FROM WORDS WHERE WORD="+'"'+word+'"'+";"
						table.execute(comd)
						wordno=table.fetchall()[0][0]
						comd="INSERT INTO WORD_POS VALUES("+str(urlid-1)+","+str(wordno)+","+str(pos)+")"
						#print(comd)
						table.execute(comd)
						db.commit()
						words.setdefault(word,0)	
						ct.setdefault(word,0)		
						ct[word]+=1		
		for j in ct:
			wordno=0
			table = db.cursor()
			comd="SELECT WORDID FROM WORDS WHERE WORD="+'"'+j+'"'+";"
			table.execute(comd)
			wordno=table.fetchall()[0][0]
			comd="INSERT INTO WORD_LINK VALUES("+str(urlid-1)+","+str(wordno)+","+str(ct[j])+")"
			#print(comd)
			table.execute(comd)
			db.commit()
		"""
	print("DONE")

print("HERE")
getfirst = raw_input("ENTER STARTING URL: ")

x=raw_input("Breadth or depth(0/1): ")

starter = getfirst[24:]

print(starter)

db = MySQLdb.connect("127.0.0.1","root","yourpassword","engine")

#table.execute("CREATE TABLE WORD_COUNT(URLID INT,WORDID INT)")

wid = 0
urlid = 0


if(int(x)==1):
	crawldfs(starter)
else:
	crawlbfs(starter,db)
