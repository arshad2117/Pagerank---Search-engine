import MySQLdb

db = MySQLdb.connect("127.0.0.1","root","yourpassword","engine")

x=db.cursor()
comd="SELECT * FROM URLS"
f = open("links.txt","w")
x.execute(comd)
lst=x.fetchall()[0:1000]
for i in range(1000):
	f.write(str(lst[i][1]) + "\n")	
