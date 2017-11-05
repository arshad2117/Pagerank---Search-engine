import MySQLdb
import urllib2
import ssl
from bs4 import BeautifulSoup
import requests

db = MySQLdb.connect("127.0.0.1","root","yourpassword","engine")

comd = "SELECT * FROM URLS";
x = db.cursor()
x.execute(comd)
data = x.fetchall()

words = {}
ct = {}
wid = 0

def insertintodb(flist,urlid):
	global wid	
	pos = 0
	ct.clear()
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
							break
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
					comd="INSERT INTO WORD_POS VALUES("+str(urlid)+","+str(wordno)+","+str(pos)+")"
					#print(comd)
					table.execute(comd)
					db.commit()
					words.setdefault(word,0)	
					ct.setdefault(word,0)		
					ct[word]+=1		

for i in range(0,100):
	print(i)
	req = requests.get(data[i][1])
	bsoup = BeautifulSoup(req.content,"html.parser")

	lst = ["".join(s(text = True)) for s in bsoup('p')]

	wordlist = " ".join(lst)

	x = comd

	flist = wordlist.split()
	
	insertintodb(flist,i)
	print(wid)
	
