from Models.ConversacionWpModel import ConversacionWpModel
import os
import time

start = time.time()
files_dir = "D:\\Dama\\Informes\\Marz13_2021"
listConversacionWp = []
Generalfile = 'conversaciones.csv'
_lastFiledProcessedLog = 'lastFileProcessed.txt'
teacherNames = ['Dama Gallego', 'Damaris Gallego🙃']
_linesToIgnore = [
    'cifrados de extremo a extremo',
    'Este chat es con una cuenta de empresa',
    'Esta cuenta de empresa ahora se ha registrado como una cuenta estándar',
    'Creaste una lista de difusión con',
    'Se añadió a',
    'fueron añadidos a la lista'
    ]

def run():
    files = os.listdir(files_dir)
    for file in files:
        fnSaveLog(file)
        fnObtenerConversacionesPorArchivo(file)
        fnSaveFile()
    end = time.time()
    print(end - start)


def fnObtenerConversacionesPorArchivo(file):    
    with open(f'{files_dir}\\{file}', encoding='utf-8') as fileOpen:        
        for line in fileOpen:
            if(fnLineToIgnore(line)):
                continue                    
            alumnoName = fnGetAlumnoName(fileOpen)
            conversacionPart = line.split(' - ')
            if len(conversacionPart) == 1:
                fnAddMessageToLastPerson(conversacionPart[0])
            else:
                message = fnGetMessage(alumnoName, conversacionPart)
                ConversacionWp = ConversacionWpModel(conversacionPart[0], alumnoName, message)
                listConversacionWp.append(ConversacionWp)

def fnLineToIgnore(line):
    for word in _linesToIgnore:
        if word in line:
            return True
    return False

def fnGetAlumnoName(fileOpen):
    return fileOpen.name.split('con')[1][:-4].strip()

def fnAddMessageToLastPerson(conversacionPart):
    lastConversation = listConversacionWp[-1]
    lastConversation.mensaje = '{} {}'.format(lastConversation.mensaje.strip('\n'), conversacionPart.strip('\n'))
    listConversacionWp[-1] = lastConversation

def fnGetMessage(alumnoName, conversacionPart):
    personAndMessage = conversacionPart[1].split(': ')
    messagePrefix = 'Docente'
    message = personAndMessage[1].strip('\n')
    if personAndMessage[0].strip() not in teacherNames:
        messagePrefix = 'Alumno'    
    return f'{messagePrefix} : {message}'

def fnSaveFile():
    newFile = open(Generalfile,"w", encoding = "utf-8")
    for conversationWp in listConversacionWp:            
        newFile.write(f'{conversationWp.fecha}|{conversationWp.alumno}|{conversationWp.mensaje}\n')  

def fnSaveLog(line):
    newFile = open(_lastFiledProcessedLog,"w", encoding = "utf-8")
    newFile.write(line)

if __name__ == '__main__':
    run()