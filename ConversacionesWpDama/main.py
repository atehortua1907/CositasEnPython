from Models.ConversacionWp import ConversacionWp
import os

files_dir = "D:\\David A\\Dama\\Conversaciones\\SeptiembreSemana3"
listConversacionWp = []
Generalfile = 'conversaciones.csv'

def run():
    files = os.listdir(files_dir)
    for file in files:
        fnObtenerConversacionesPorArchivo(file)
        fnSaveFile()

def fnObtenerConversacionesPorArchivo(file):    
    with open(f'{files_dir}\\{file}', encoding='utf-8') as fileOpen:        
        for line in fileOpen:
            if "cifrados de extremo a extremo" in line:
                continue            
            alumnoName = fnGetAlumnoName(fileOpen)
            conversacionPart = line.split(' - ')
            if len(conversacionPart) == 1:
                fnAddMessageToLastPerson(conversacionPart[0])
            else:
                ConversacionWp = fnObtenerConversacionWp(conversacionPart, alumnoName)
                listConversacionWp.append(ConversacionWp)

def fnGetAlumnoName(fileOpen):
    return fileOpen.name.split('con')[1][:-4].strip()

def fnAddMessageToLastPerson(conversacionPart):
    lastConversation = listConversacionWp[-1]
    if lastConversation.respuesta == '':
        lastConversation.mensaje = '{} {}'.format(lastConversation.mensaje.rstrip('\n'), conversacionPart.rstrip('\n'))
    else:
        lastConversation.respuesta = '{} {}'.format(lastConversation.respuesta.rstrip('\n'), conversacionPart.rstrip('\n'))
    
    listConversacionWp[-1] = lastConversation

def fnObtenerConversacionWp(conversacionPart, alumnoName):
    message, teacherMessage = fnGetMessages(alumnoName, conversacionPart)
    return ConversacionWp(conversacionPart[0], alumnoName, message, teacherMessage)


def fnGetMessages(alumnoName, conversacionPart):
    personAndMessage = conversacionPart[1].split(':')
    alumnoMessage = ''
    teacherMessage = ''    
    if personAndMessage[0].strip() == 'Dama Gallego':
        teacherMessage = personAndMessage[1]
    else:
        alumnoMessage = personAndMessage[1]
    
    return alumnoMessage.rstrip('\n'), teacherMessage.rstrip('\n')

def fnSaveFile():
    newFile = open(Generalfile,"w", encoding = "utf-8")
    for conversationWp in listConversacionWp:            
        newFile.write(f'{conversationWp.fecha}|{conversationWp.alumno}|{conversationWp.mensaje}|{conversationWp.respuesta}'+'\n')  


if __name__ == '__main__':
    run()