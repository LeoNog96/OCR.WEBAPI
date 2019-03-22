# -*- coding: utf-8 -*-
import os
import shutil 
import textract
import time
import datetime
import storage
import json
from libs.customEncoder import CustomEncoder 
from bd import Bd
import multiprocessing
import subprocess
from elastic import Elastic
import removeAc
import xml_parser


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

        print("começo do lote N-PDF, será processados "+str(len(queue))+" arquivos")
        print("-------------------------------------------------------------")

        try:
                        
            cron = datetime.datetime.now()
            id = 1
            f = open(str(os.getcwd())+'/queue/'str(id)+'.txt', 'w+b')
            binary_format = bytearray(files)
            f.write(binary_format)
            f.close()
            
            print("N-PDF - Processando o arquivo: "+ queue[item]+" às "+cron.strftime("%d-%m-%y-%H:%M:%S")+"\n")
            
            #processamento do Arquivo
                    
            if ".pdf" in str(queue[item]):
                
                text = textract.process((str(os.getcwd())+'/queue/'+str(queue[item])), method='tesseract' ,language=languages)
                return removeAc.remover_acentos(str(text.decode('utf8')+""))

            elif ".msg" in str(queue[item]):

                text = textract.process((str(os.getcwd())+'/queue/'+str(queue[item])), method='msg-extractor',language=languages)
                removeAc.remover_acentos(str(text.decode('utf8')+""))
            
            elif ".xml" in str(queue[item]):

                text = xml_parser.xmlParser(str(os.getcwd())+'/queue/'+str(queue[item]))
                return removeAc.remover_acentos(text)

            else:

                text = textract.process((str(os.getcwd())+'/queue/'+str(queue[item])),language=languages)
                return removeAc.remover_acentos(str(text.decode('utf8')+""))
                
            
            os.remove(str(os.getcwd())+'/queue/'+str(queue[item]))
        
            print("N-PDF Terminou o arquivo: "+ queue[item]+" às "+ datetime.datetime.now().strftime("%d-%m-%y-%H:%M:%S")+ " demorou = "+str(datetime.datetime.now() - cron))
            print("----------------\n")
            
            arquivos +=1
            queue = os.listdir(str(os.getcwd())+'/queue/')
        
        except textract.exceptions.ShellError:

            print("Erro ao ler .doc, exportando para PDF")                      
            
            t = os.system("libreoffice --headless --convert-to pdf:writer_pdf_Export --outdir "+str(os.getcwd())+'/queuePDF/ '+str(os.getcwd())+'/queue/'+str(queue[item]))
            os.remove(str(os.getcwd())+'/queue/'+str(queue[item]))
            queue = os.listdir(str(os.getcwd())+'/queue/')
            
            print("Exportação Finalizada com sucesso\n")
            
        except Exception as identifier:
            print(identifier) 
            print("---Não foi possivel processar o arquivo: " + queue[item]+"---\n")
            #print(identifier)
            os.remove(str(os.getcwd())+'/queue/'+str(queue[item]))
            
            return None     