import PySimpleGUI as sg
import sqlite3
import os

from Utility import util

conn=sqlite3.connect('.dircomp.db')

cursor= conn.cursor()

def createNewProj(DirWay):
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
			if n!='' and d!='':
				createNewDir(n,d,DirWay)
			break

	win1.close()


def createNewDir(name,dire,DirWay):
	cursor.execute(f'''
        INSERT INTO projcomp (nome, dir)
        VALUES ('{name}','{dire}')
    ''')
	conn.commit()
	sg.popup('Aviso', '"'+name+'" foi registrado\n')
	os.mkdir(DirWay+name)
	util.CopyTree(dire,DirWay+name)
