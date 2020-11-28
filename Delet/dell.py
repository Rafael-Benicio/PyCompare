import sqlite3
import shutil

conn=sqlite3.connect('.dircomp.db')

cursor= conn.cursor()

def deletaProj(na,DirWay):
	c=cursor.execute('DELETE FROM projcomp WHERE nome="'+na+'"')
	conn.commit()
	shutil.rmtree(DirWay+na)
	