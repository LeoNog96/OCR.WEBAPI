from azure.storage.blob import BlockBlobService
import gzip
import io
import os
import variables

def getContainer(idCompany):
    
    return variables.predicate+"-"+str(idCompany)

def getBlock(idRevision):
    
    return str(idRevision)

def getBlob(idCompany,idRevision,out,files):
    
    variables.block_blob_service.get_blob_to_path(getContainer(idCompany), getBlock(idRevision), out)
    
    inF = gzip.GzipFile(out, 'rb')
    ouF = inF.read()
    inF.close()

    outF = open(files, 'wb')
    outF.write(ouF) 
    outF.close()
    os.remove(out)

#getBlob(64,1066928,'s','s')