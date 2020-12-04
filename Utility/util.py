import PySimpleGUI as sg
import os.path, time
import sqlite3
import shutil
import time
import os

conn=sqlite3.connect('.dircomp.db')

cursor= conn.cursor()

def CopyTree(src,dst):
	dirEle=os.listdir(src)
	for ele in dirEle:
		i=ele.find('.')
		if ele[i]!='.':
			os.mkdir(dst+'/'+ele)
			CopyTree(src+'/'+ele,dst+'/'+ele)
		else:
			shutil.copy(src+'/'+ele,dst+'/'+ele)
	
def Logs(src,dist,name):
	a=time.ctime()
	b=a.split()
	with open(src+'/Logs.txt','a') as arq:
		if name !=[]:
			arq.writelines('\n')
			arq.writelines('('+b[2]+'/'+b[1]+'/'+b[4]+'):\n')
		tex=sg.popup_get_text('Comentário', 'Tópico Trabalhado na nova versão')
		if tex:
			pass
		else:
			tex='Sem Comentários'
		for na in name:
			arq.writelines('	('+na.upper()+')=>['+tex+']\n')
		arq.writelines('\n')
		arq.writelines('\n')
		arq.close()	
		shutil.copyfile(src+'/Logs.txt', dist+'/Logs.txt')
	for ele in name:
		os.remove(dist+'/'+ele)
		shutil.copyfile(src+'/'+ele, dist+'/'+ele)

def compFont(src,dist):
	dirEle=os.listdir(src)
	changes=[]
	for ele in dirEle:
		i=ele.find('.')
		if ele[i]!='.':
			print('---------'+ele+'--------')
			compFont(src+'/'+ele,dist+'/'+ele)
			print('-------------------')
		elif ele=='Logs.txt':
			pass
		else:
			text1=open(src+'/'+ele,'rb')
			text2=open(dist+'/'+ele,'rb')
			doc1=[]
			doc2=[]
			num=0
			for line in text1:
				doc1.append(line)
			for line in text2:
				doc2.append(line)
			for i in range(0,len(doc1)):
				do1=doc1[i]
				do2=doc2[i]
				if do1!=do2:
					print('----------------------')
					print('# '+ele+' : Foi modificado')
					print('----------------------')
					changes.append(ele)
					break	
			text2.close()
			text1.close()
	if changes==[]:
		sg.popup('Aviso', 'Não ouve Alterações\n desde a ultima versão registrada!')
	else:
		Logs(src,dist,changes)	

def comparaProj(na,i,DirWay):
	cursor.execute('''SELECT dir from projcomp;''')
	Dire=[]
	for dires in cursor.fetchall():
		Dire.append(dires[0])
	dD=DirWay+na
	dF=Dire[i]
	compFont(dF,dD)