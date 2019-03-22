import json


class Revision:

    Id = None
    IdAuthor = None
    IdFolder = None   
    IdDocumentType = None    
    IdStatus  = None 
    IdCompany = None
    IdTrashUser = None
    RevisionStatus = None
    Code = None
    Date  = None
    Title = None
    Description  = None
    Keywords = None
    NumberOfPages = None
    Removed = None
    Extension = None
    Size = None
    RevisionNumber = None
    RevisionMaxNumber = None
    NextRevisionDate = None
    RevisionNotificationDate = None
    NotificationDays = None
    TrashDate = None
    ContentIndexed = None
    PropertiesIndexed = None
    Notified = None
    IsPublic = None
    IsSigned = None
    RowGuid = None
    AdditionalFields = None
    Content = None

    def __init__(self, lists):

        self.Id = lists[0]      
        self.IdFolder = lists[1]   
        self.IdDocumentType = lists[2] 
        self.IdAuthor = lists[3]  
        self.IdCompany = lists[4]
        self.IdStatus  = lists[5]
        self.Code = lists[6]
        self.Title = lists[7]
        self.Description  = lists[8]
        self.Keywords = lists[9]
        self.Date = str(lists[10])
        self.NumberOfPages = lists[11]
        self.Extension = lists[12]
        self.Size = lists[13] 
        self.RevisionNumber = lists[14]
        self.RevisionMaxNumber = lists[15]
        self.Removed = lists[16]
        self.TrashDate = lists[17]
        self.IdTrashUser = lists[18]
        self.NextRevisionDate = lists[19]
        self.RevisionNotificationDate = lists[20]
        self.ContentIndexed = lists[21]
        self.NotificationDays = lists[22]
        self.PropertiesIndexed = lists[23]
        self.RowGuid = lists[24]
        self.Notified = lists[25]
        self.IsPublic = lists[26]
        self.IsSigned = lists[27]
        self.RevisionStatus = lists[28]

    def js (self):
        
        json = {}
        json['_source'] = {'id':self.Id, 'code': self.Code, 'additionalFields':self.AdditionalFields, 'title': self.Title, 'author': self.IdAuthor, 'documentType': self.IdDocumentType, 'revisionDate': self.Date, 'description': self.Description, 'extension': self.Extension, 'keyWords': self.Keywords, 'folder': self.IdFolder, 'content':self.Content }

        return json

       
