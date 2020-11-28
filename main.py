import PySimpleGUI as sg
import sqlite3
import os.path, time
import shutil
import time
import os

from Utility import util
from NewProj import create
from Show import visual

DirWay=''

sg.theme('Dark Amber')

layout=[
	[sg.Text('Novo Projeto                       ',font=(16)),sg.Button('Cria',font=(14))],
	[sg.Text('Ver projetos que já existem',font=(16)),sg.Button('Ver',font=(14))],]

if os.path.isfile('.dirP.txt'):
	arquivo=open('.dirP.txt','r')
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
		if event=='Cancelar' or event == sg.WIN_CLOSED:
			exit()
		if event=='Ok':
			if values['-dir-']=='':
				sg.popup_ok('Aviso','Por favor, click em "Browse"\n ou escreva um diretorio.') 
				exit()
			else:
				arquivo = open(".dirP.txt", "w")
				arquivo.write(values['-dir-']+"/DocNew/")
				os.mkdir(values['-dir-']+"/DocNew/") 
				DirWay=values['-dir-']+"/DocNew/"
				arquivo.close()
			break
	winNew.close()

conn=sqlite3.connect('.dircomp.db')

cursor= conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS projcomp (
    nome TEXT NOT NULL,
    dir TEXT NOT NULL
);
''')

window=sg.Window('Rafa',layout)		

while True:
	event, values = window.read()
	if event == sg.WIN_CLOSED:
		exit()
	if event == 'Cria':
		create.createNewProj(DirWay)
	if event == 'Ver':
		visual.showProjs(DirWay)

window.close()