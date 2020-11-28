import PySimpleGUI as sg
import sqlite3

from Utility import util
from Delet import dell

conn=sqlite3.connect('.dircomp.db')

cursor= conn.cursor()

def showProjs(DirWay):
	cursor.execute('''SELECT nome from projcomp;''')
	newArr=[]

	for name in cursor.fetchall():
		newArr.append(name[0])
	ShowBox(newArr,DirWay)

def ShowBox(n,DirWay):
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
						i=sg.popup_yes_no('Você tem certeza que quer COMPARAR o projeto\n"'+n[j]+'"') 
						if i=='Yes':
							util.comparaProj(n[j],j,DirWay)
			if event == 'Deletar':
				for j in range(len(n)):
					if values[j]:
						i=sg.popup_yes_no('Você tem certeza que quer APAGAR o projeto\n"'+n[j]+'"') 
						if i=='Yes':
							dell.deletaProj(n[j],DirWay)
				break
				
		win3.close()
