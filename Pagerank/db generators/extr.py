import MySQLdb
import urllib2
import ssl
from bs4 import BeautifulSoup
import requests


db = MySQLdb.connect("127.0.0.1","root","yourpassword","engine")
x= db.cursor()
"""
comd="SELECT * FROM WORDS"
x.execute(comd)
data = x.fetchall()
for i in range(2825):
	comd = "INSERT INTO WORDBC VALUES ("+str(int(data[i][0]))+","+'"'+str(data[i][1])+'");'
	x.execute(comd)
	db.commit()
	print(i)
"""
comd="SELECT * FROM URLS"
x.execute(comd)
ulist = x.fetchall()
print(ulist)
comd = "SELECT COUNT(*) FROM WORDS"
x.execute(comd)
pres = int(x.fetchall()[0][0])
#print(wid)
pres+=1
for i in range(100):
	print(i)
	print(ulist[i][1])
	url = ulist[i][1]
	ind = url.find('/wiki/')
	des=ulist[i][1][ind+6:]
	#print(des)
	words = des.split('_')
	for word in words:
		comd = "SELECT * FROM WORDS WHERE WORD ="+'"'+word+'"'+";"
		x.execute(comd)
		data = x.fetchall()
		if(len(data) > 0):
			wid = int(data[0][0])
			comd = "INSERT INTO URLWORDS VALUES ("+str(i)+","+str(wid)+");"
			x.execute(comd)
			print(comd)
			db.commit()
		else:
			comd = "INSERT INTO WORDBC VALUES ("+str(pres)+","+"'"+str(word)+"'"+");"
			comd2 = "INSERT INTO URLWORDS VALUES ("+str(i)+","+str(pres)+");"
			print(comd)
			print(comd2)
			x.execute(comd)
			db.commit()
			x.execute(comd2)
			db.commit()		
			pres += 1
