import PySimpleGUI as sg
import sqlite3
import os.path

conn=sqlite3.connect('dircomp.db')

cursor= conn.cursor()

DirWay=''

sg.theme('Dark Amber')


cursor.execute('''
CREATE TABLE IF NOT EXISTS projcomp (
    nome TEXT NOT NULL,
    dir TEXT NOT NULL
);
''')

layout=[
	[sg.Text('Novo Projeto                       ',font=(16)),sg.Button('Cria',font=(14))],
	[sg.Text('Ver projetos que já existem',font=(16)),sg.Button('Ver',font=(14))],]

if os.path.isfile('./dirP.txt'):
	arquivo=open('./dirP.txt','r')
	DirWay=arquivo.readline()
else:
	layNew=[
		[sg.Text('Indique o diretório em que você quer Salvar seus backup')],
		[sg.InputText('',background_color='white',text_color='black',key='-dir-'),sg.FolderBrowse()],
		[sg.Button('Ok'),sg.Button('Cancelar')]
	]
	winNew=sg.Window('DirNew',layNew)
	while True:
		event, values=winNew.read()
		if event=='Cancelar':
			exit()
		if event=='Ok':
			if values['-dir-']=='':
				sg.popup_ok('Aviso','Por favor, click em "Browse"\n ou escreva um diretorio.') 
				exit()
			else:
				arquivo = open("dirP.txt", "w")
				arquivo.write(values['-dir-']+"/DocNew/")
				os.mkdir(values['-dir-']+"/DocNew/") 
				DirWay=values['-dir-']+"/DocNew/"
				arquivo.close()
			break
	winNew.close()

window=sg.Window('Rafa',layout)

def createNewProj():
	sg.theme('Dark Amber')

	lay1=[
		[sg.Text('Nome do Projeto')],
		[sg.InputText('',background_color='white',text_color='black',key='-nom-')],
		[sg.Text('Diretório do Projeto')],
		[sg.InputText('',background_color='white',text_color='black',key='-dir-'),sg.FolderBrowse()],
		[sg.Button('Registrar')]]

	win1=sg.Window('Novo Projeto',lay1)

	while True:
		event,values =win1.read()
		if event == sg.WIN_CLOSED:
			break
		if event == 'Registrar':
			n=values['-nom-']
			d=values['-dir-']
			createNewDir(n,d)
			break

	win1.close()	

def createNewDir(name,dire):
	cursor.execute(f'''
        INSERT INTO projcomp (nome, dir)
        VALUES ('{name}','{dire}')
    ''')
	conn.commit()
	sg.popup('Aviso', '"'+name+'" foi registrado\n')
	os.mkdir(DirWay+name)

def showProjs():
	cursor.execute('''SELECT nome from projcomp;''')
	newArr=[]

	for name in cursor.fetchall():
		newArr.append(name[0])
	ShowBox(newArr)

def ShowBox(n):
	if n ==[]:
		sg.popup('Atenção!!!', 'Não existe Registros\n',font=(18))
	else:
		arr=[]
		for i in range(len(n)):			
			arr.append([sg.Radio(n[i], "RADIO1", default=False, font=(18))])
		arr.append([sg.Button('Comparar'),sg.Button('Deletar')])
		win3=sg.Window('Lista de Comparação',arr)

		while True:
			event,values=win3.read()
			if event == sg.WIN_CLOSED:
				break
			if event == 'Comparar':
				for j in range(len(n)):
					if values[j]:
						print(j)
			if event == 'Deletar':
				for j in range(len(n)):
					if values[j]:
						i=sg.popup_yes_no('Você tem certeza que quer apagar o projeto\n"'+n[j]+'"') 
						if i=='Yes':
							deletaProj(n[j])
				break
				
		win3.close()

def deletaProj(na):
	c=cursor.execute('DELETE FROM projcomp WHERE nome="'+na+'"')
	conn.commit()
	

while True:
	event, values = window.read()
	if event == sg.WIN_CLOSED:
		exit()
	if event == 'Cria':
		createNewProj()
	if event == 'Ver':
		showProjs()

window.close()

