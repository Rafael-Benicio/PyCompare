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


# Escrever as modificações feitas no arquivo Logs.txt
def Logs(src,dist,name):
	a=time.ctime()
	b=a.split()
	# Abre arquivo Logs.txt
	with open(src+'/Logs.txt','a') as arq:
		# Se houver alguma modificação registra a data 
		if name !=[]:
			arq.writelines('\n')
			arq.writelines('('+b[2]+'/'+b[1]+'/'+b[4]+'):\n')
		# Escrever as modificações no Logs.txt
		for na in name:
			# Comentar as modificaçõess
			ne=na
			lay=[
				[sg.Text('Comente as modificações feitas em :')],
				[sg.Text(ne.upper())],
				[sg.InputText(key='-ke-',background_color='white',text_color='black')],
				[sg.Button('OK'),sg.Button('Cancelar')]
				]
			window=sg.Window('Comentário',lay)
			# Loop para visualizar janela de comentario
			while True:
				e,v=window.read()
				tex=''
				if e =='OK' and v['-ke-']!='': 
					tex=v['-ke-']
					break
				elif e=='Cancelar' or v['-ke-']=='' or e == sg.WIN_CLOSED:
					tex='Sem Comentários'
					break
			# fecha a janela
			window.close()
			# Escreve Comentario
			arq.writelines('	('+na.upper()+')=>['+tex+']\n')
		arq.writelines('\n')
		arq.writelines('\n')
		arq.close()	
		shutil.copyfile(src+'/Logs.txt', dist+'/Logs.txt')
	for ele in name:
		os.remove(dist+'/'+ele)
		shutil.copyfile(src+'/'+ele, dist+'/'+ele)

def compFont(src,dist):
	# Obtem o numero de arquivos na font
	dirEle=os.listdir(src)
	# Obtem o numero de arquivos no Backup
	dirDist=os.listdir(dist)
	# Lista que vai armazenar os arquivos modificados
	changes=[]
	# For para checar os elementos da font
	for ele in dirEle:
		# Identifica se elemento analisado é uma pasta
		i=ele.find('.')
		if i!=0 and ele[i]!='.':
			print('---------'+ele+'--------')
			compFont(src+'/'+ele,dist+'/'+ele)
			print('-------------------')
		elif ele=='Logs.txt':
			pass
		else:
			enc=dirDist
			if ele in dirDist:
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
			else:
				shutil.copyfile(src+'/'+ele, dist+'/'+ele)
				print('----------------------')
				print('# '+ele+' : Foi Criado')
				print('----------------------')
				changes.append(ele)
				

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