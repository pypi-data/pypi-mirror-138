from copy import deepcopy
from .. utils import FSDocument, FirestoreClient

class QuickBooksData():
    '''
    Class that will get any quick books data that is loaded into the Firestore database
    '''
    
    def __init__(self, qbType):
        self.fClient = FirestoreClient.getInstance()
        self.qb_type = qbType
        
    def getClient(self):
        return self.fClient
    
    def getBasePath(self):
        return f"application_data/{self.fClient.company}/QuickBooks/Data/{self.qb_type}"
    
    def getSchemaPath(self):
        return f"application_data/{self.fClient.company}/QuickBooks/Schemas/{self.qb_type}"
    
    def getSchema(self):
        '''
        Get a Document that has two fields
        base:  How it is parsed
        flattend: The attempt to flatten the structure a bit
        
        The schema will represent only the highest levels and will represent the following under each field
        1. Name:  What the basic name is.. flattend will be <parent_name>__<name>
        2. Label: Logic that will add Spaces around camel case and then spell out shortened strings
        3. Order: The order that the fields should be shown
        4. Type:  The data type:  Date, String, Boolean, Number
        '''
        collRef = self.fClient.fsClient.collection(self.getSchemaPath())
        docs = [FSDocument(x,True) for x in collRef.list_documents()]
        data = {x.id:x.snap.to_dict() for x in docs}
        return data
        

    def getDocuments(self):
        collRef = self.fClient.fsClient.collection(self.getBasePath())
        docs = [FSDocument(x,True) for x in collRef.list_documents()]
        return docs      
    
    def getJSON(self):
        resp = None
        resp = [x.snap.get("flattened") for x in self.getDocuments()]
        
        return resp
    
    @classmethod
    def GetData(cls,qbType):
        return QuickBooksData(qbType).getJSON()
    
    @classmethod
    def getDocs(cls,qbType):
        return QuickBooksData(qbType).getDocuments()
    
    @classmethod
    def GetSchema(cls,qbType):
        return QuickBooksData(qbType).getSchema()
    

    
class QuickBooksTypes():
    '''
    Class that will get any quick books data that is loaded into the Firestore database
    '''
    exclude_coll = ['Sessions','Schema']
    
    def __init__(self):
        self.fClient = FirestoreClient.getInstance()
        self.fsDoc = FSDocument.getInstance(self.getBasePath())
        
    def getBasePath(self):
        return f"application_data/{self.fClient.company}/QuickBooks/Data"
    
    def getCollections(self):
        collList = self.fsDoc.ref.collections()
        return [x.id for x in collList if x.id not in self.exclude_coll]
    
    @classmethod
    def getQBTypes(cls):
        qbt = QuickBooksTypes()
        return qbt.getCollections()
        