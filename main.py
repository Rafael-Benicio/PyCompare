import PySimpleGUI as sg
import sqlite3
import os.path

conn=sqlite3.connect('dircomp.db')

sg.theme('Dark Amber')

layout=[
	[sg.Text('Novo Projeto                       ',font=(16)),sg.Button('Cria',font=(14))],
	[sg.Text('Ver projetos que já existem',font=(16)),sg.Button('Ver',font=(14))],]

if os.path.isdir('/home/rafael/Documentos/DocBackup'):
	print('exist')
else:
	os.mkdir('/home/rafael/Documentos/DocBackup')

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
			createNewDir(n)
			break

	win1.close()	

def createNewDir(name):
	os.mkdir('/home/rafael/Documentos/DocBackup/'+name)

def showProjs():
	sg.theme('Dark Amber')

while True:
	event, values = window.read()
	if event == sg.WIN_CLOSED:
		exit()
	if event == 'Cria':
		createNewProj()
	if event == 'Ver':
		showProjs()

window.close()
