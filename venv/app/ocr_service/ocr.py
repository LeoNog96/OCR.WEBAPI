# -*- coding: utf-8 -*-
import os
import shutil 
import textract
import time
import datetime
import json
import multiprocessing
import subprocess
from .removeAc import *
from .xml_parser import * 


class Ocr:

    dbv4 = None
    es = None
  
    
    # def __init__(self):

    #     #self.dbv4 = Bd()
    #     #self.es = Elastic()

    def Pdf(self,languages):
        
        #busca as revisions no banco
        revisionsPDF = self.dbv4.getRevisionsPDF()
        revisions = self.dbv4.getRevisions()
        
        #lista os arquivos que existem no diretorio queue
        queue = os.listdir(str(os.getcwd())+'/queuePDF/')
        #se for = a zero ele realiza uma nova busca
        if len(queue) == 0:
           
            #se não tiver novos arquivos ele fecha o serviço
            if len(revisionsPDF) == 0:
                print("Parabéns vc zerou os DOCS,  aguardamos mais DOCS")
                return False
            j= 0
            timer = datetime.datetime.now()
            print("Buscando arquivos no storage")
            for x in revisionsPDF:
                #shutil.copy2('/home/leonardo/Documentos/testes/'+str(x), str(os.getcwd())+'/queue/')
                try:
                    files = str(os.getcwd())+'/queuePDF/'+str(x.Id)+'.'+x.Extension
                    
                    storage.getBlob(x.IdCompany, x.Id,"1",files)
                    j+=1
                    print("Download concluido do arquivo: "+ str(x.Id))
                except Exception as erro:
                    print("---Erro ao buscar arquivo no storage: "+ str(x.Id)+"---")
                
            queue = os.listdir(str(os.getcwd())+'/queuePDF/')

            print("Fim da busca de arquivos no storage, a busca levou : "+str(datetime.datetime.now()-timer))

        cron = None
        timer = datetime.datetime.now()
        arquivos = 0
        erro = 0
        print("### começo do lote PDF-TIFF, será processados "+str(len(queue))+" arquivos")
        #print("-------------------------------------------------------------")
        item = 0 

        while len(queue) != 0:

            try:
                                
                cron = datetime.datetime.now()
                
                print("PDF-TIFF - Processando o arquivo: "+ queue[item]+" às "+cron.strftime("%d-%m-%y-%H:%M:%S")+"\n")
                
                #processamento do Arquivo
                     
                if ".pdf" in str(queue[item]):
                    text = textract.process((str(os.getcwd())+'/queuePDF/'+str(queue[item])), method='tesseract' ,language=languages)
                else:
                    text = textract.process((str(os.getcwd())+'/queuePDF/'+str(queue[item])), method='tesseract',language=languages)

                revision = [rev for rev in revisionsPDF if str(rev.Id)+'.'+rev.Extension == queue[item] or str(rev.Id)+'.pdf' == queue[item]][0]
                
                #salvar o resultado em um arquivo
                files = open(str(os.getcwd())+"/resultPDF/"+str(revision.Id)+"-"+str(revision.IdCompany),"w",encoding='utf-8')
                files.write(removeAc.remover_acentos(str(text.decode('utf8')+"")))
                files.close()
                os.remove(str(os.getcwd())+'/queuePDF/'+str(queue[item]))
            
                print("PDF-TIFF Terminou o arquivo: "+ queue[item]+" às "+ datetime.datetime.now().strftime("%d-%m-%y-%H:%M:%S")+ " demorou = "+str(datetime.datetime.now() - cron))
                print("----------------\n")
                
                arquivos +=1
                queue = os.listdir(str(os.getcwd())+'/queuePDF/')
            except IndexError:
                
                revision = [rev for rev in revisions if str(rev.Id)+'.'+rev.Extension == queue[item] or str(rev.Id)+'.pdf' == queue[item]][0]
                
                #salvar o resultado em um arquivo
                files = open(str(os.getcwd())+"/resultPDF/"+str(revision.Id)+"-"+str(revision.IdCompany),"w",encoding='utf-8')
                files.write(removeAc.remover_acentos(str(text.decode('utf8')+"")))
                files.close()
                os.remove(str(os.getcwd())+'/queuePDF/'+str(queue[item]))
            
                print("PDF-TIFF Terminou o arquivo: "+ queue[item]+" às "+ datetime.datetime.now().strftime("%d-%m-%y-%H:%M:%S")+ " demorou = "+str(datetime.datetime.now() - cron))
                print("----------------\n")
                
                arquivos +=1
                queue = os.listdir(str(os.getcwd())+'/queuePDF/')

            except Exception as identifier:
                print(identifier) 
                print("---Não foi possivel processar o arquivo: " + queue[item]+"---\n")
                #print(identifier)
                os.remove(str(os.getcwd())+'/queuePDF/'+str(queue[item]))
                
                erro += 1
                queue = os.listdir(str(os.getcwd())+'/queuePDF/')       

        print("Fim do lote PDF-TIFF, foram processados "+str(arquivos)+" em "+str(datetime.datetime.now() - timer)+" Outros "+str(erro)+" arquivos não foram processados")
        print("\n")

        self.es.sendElasticSearchPDF()
        self.dbv4.savePDF()
        removeAc.removePDF()
        return True

    def Npdf (self,files):

        languages = 'por'

        print("Nova Requisição")
        print("-------------------------------------------------------------")

        try:                    
            extension = '.doc'          
            arquivo = open('/home/leonardo/Roteiro de instalação elasticSearch.doc','rb')            
            files = arquivo.read()
            arquivo.close()
            path = str(os.getcwd())+'/app/ocr_service/queue/'

            cron = datetime.datetime.now()
            item = str("cron")+extension
            out = open(path+item,'wb')
            out.write(files)
            out.close()

        
            print("N-PDF - Processando o arquivo: "+item+" às "+cron.strftime("%d-%m-%y-%H:%M:%S")+"\n")
            
            #processamento do Arquivo
                    
            if ".pdf" in item:
                
                text = textract.process(path+item, method='tesseract' ,language=languages)
                os.remove(path+item)
                print("N-PDF Terminou o arquivo: "+ item+" às "+ datetime.datetime.now().strftime("%d-%m-%y-%H:%M:%S")+ " demorou = "+str(datetime.datetime.now() - cron))
                print("----------------\n")
                return remover_acentos(str(text.decode('utf8')+""))

            elif ".msg" in item:

                text = textract.process(path+item, method='msg-extractor',language=languages)
                os.remove(path+item)
                print("N-PDF Terminou o arquivo: "+ item+" às "+ datetime.datetime.now().strftime("%d-%m-%y-%H:%M:%S")+ " demorou = "+str(datetime.datetime.now() - cron))
                print("----------------\n")
                return remover_acentos(str(text.decode('utf8')+""))
            
            elif ".xml" in item:

                text = xml_parser.xmlParser(path+item)
                os.remove(path+item)
                print("N-PDF Terminou o arquivo: "+ item+" às "+ datetime.datetime.now().strftime("%d-%m-%y-%H:%M:%S")+ " demorou = "+str(datetime.datetime.now() - cron))
                print("----------------\n")
                return remover_acentos(text)

            else:
                print("foi "+item)
                text = textract.process(path+item,language=languages)
                os.remove(path+item)
                print("N-PDF Terminou o arquivo: "+ item+" às "+ datetime.datetime.now().strftime("%d-%m-%y-%H:%M:%S")+ " demorou = "+str(datetime.datetime.now() - cron))
                print("----------------\n")
                return remover_acentos(str(text.decode('utf8')+""))
                
            
            
        
            
            
            arquivos +=1
            queue = os.listdir(str(os.getcwd())+'/queue/')
        
        except textract.exceptions.ShellError:

            print("Erro ao ler .doc, exportando para PDF")                      
            
            t = os.system("libreoffice --headless --convert-to pdf:writer_pdf_Export --outdir "+path+'/export.pdf')
            os.remove(path+item)
            
            print("Exportação Finalizada com sucesso\n")

            text = textract.process(path+'export.pdf', method='tesseract' ,language=languages)
            return removeAc.remover_acentos(str(text.decode('utf8')+""))
            
        except Exception as identifier:
            print(identifier) 
            #print("---Não foi possivel processar o arquivo: " + queue[item]+"---\n")
            #print(identifier)
            #os.remove(str(os.getcwd())+'/queue/'+str(queue[item]))
            
            return None     