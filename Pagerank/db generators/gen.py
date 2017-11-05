from random import shuffle
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

f =open("links.txt","r")

urls = [line for line in f]

shuffle(urls)

found={}

db = MySQLdb.connect("127.0.0.1","root","yourpassword","engine")

for i in range(100):
	found[urls[i][:-1]]=1
	print(urls[i])
	x = db.cursor()
	comd = "INSERT INTO URLS VALUES ("+str(i)+","+'"'+urls[i][:-1]+'"'+");"
	print(comd)
	x.execute(comd)
	db.commit()


print(found)


linked={}

for i in urls[:100]:
	
	req=urllib2.Request(i,None,headers)
	page=urllib2.urlopen(req)
	cont=page.read()
	bsoup = BeautifulSoup(cont,"html.parser")
	anchor = bsoup('a')
	print(i + "ACTUAL")	
	for link in anchor:
		try:
			nurl = str(link.get('href',None))
		except:
			continue		
		#print(nurl)		
		"""print(nurl)
		if(nurl.find("/wiki/") != 0 or nurl.find("(") != -1 or nurl.find(":") != -1 or nurl.find("/wiki/IEEE") != -1 or nurl.find("/wiki/ISO") != -1):
			pass
		else:
			print(nurl)	
		ulink = "https://en.wikipedia.org" + str(nurl[:-3])
		"""		
		#if(nurl.find("/wiki/") != -1):		
		#	print(ulink)
		ulink= "https://en.wikipedia.org" + nurl
		
		if(ulink in found):
			comd="SELECT * FROM URLS WHERE URL ="+'"'+ulink+'"'+";"
			x = db.cursor()
			x.execute(comd)
			data = x.fetchall()
			id1 = data[0][0]
			comd="SELECT * FROM URLS WHERE URL ="+'"'+i[:-1]+'"'+";"
			x.execute(comd)
			data = x.fetchall()
			id2 = data[0][0]
			if(id1 != id2 and (id1,id2) not in linked):
				comd = "INSERT INTO LINKS VALUES ("+str(id1)+","+str(id2)+");"
				x.execute(comd)
				linked[(id1,id2)]=1
				print(comd)
				db.commit()
			

	




