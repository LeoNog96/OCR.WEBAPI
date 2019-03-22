from unicodedata import normalize
import os

def remover_acentos(txt):
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')

def remove():

    result = os.listdir(str(os.getcwd())+'/result/')

    for j in result:
        os.remove(str(os.getcwd())+'/result/'+j)

def removePDF():

    resultPDF = os.listdir(str(os.getcwd())+'/resultPDF/')
    
    for i in resultPDF:
        os.remove(str(os.getcwd())+'/resultPDF/'+i)