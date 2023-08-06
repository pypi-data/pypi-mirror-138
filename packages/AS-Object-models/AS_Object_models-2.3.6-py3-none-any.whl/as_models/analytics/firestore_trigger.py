import traceback
from .. utils import FireStoreBase

class FirestoreChangeRec(object):
    '''
    Processing a trigger event
    https://cloud.google.com/functions/docs/calling/cloud-firestore#event_structure
    
    
    '''
    function_map = {"nullValue": 'getNone',
                    "booleanValue": 'getBool',
                    "integerValue": 'getInt',
                    "doubleValue": 'getFloat',
                    "timestampValue": 'getStr',
                    "stringValue": 'getStr',
                    "bytesValue": 'getStr',
                    "referenceValue": 'getStr',
                    "geoPointValue": 'getLatLong',
                    "arrayValue": 'getArrayValue',
                    "mapValue": 'getMapValue',
                    "fields": 'processFields'}
    
    def __init__(self, eventObject, ignoreFields=FireStoreBase.base_fields):
        self.event = eventObject
        self.changeDataSummary = {}
        self.ignore_fields = ignoreFields
        self.changeDataSummary['before'] = self.processUpdate('oldValue')
        self.changeDataSummary['after'] = self.processUpdate('value')
        
        self.changedFields = []
        if len(list(self.event['updateMask'].keys())) > 0:
            self.changedFields = self.event['updateMask']['fieldPaths']
            
        self.changeDataSummary['action'] = 'update'
        if self.changeDataSummary['before'] is None:
            self.changeDataSummary['action'] = 'create'
        
        if self.changeDataSummary['after'] is None:
            self.changeDataSummary['action'] = 'delete'
        
    def currentObject(self):
        if self.isDeleted:
            return self.changeDataSummary['before']
        return self.changeDataSummary['after']
    
    def priorObject(self):
        return self.changeDataSummary['before']
    
    def data(self,current=True):
        if current:
            return self.currentObject()['data']
        priorData = self.priorObject().get('data',{})
        if priorData is None:
            priorData = {}
        return priorData 
    
    @property
    def path(self):
        return self.currentObject()['path']
        
    @property
    def updateTime(self):
        return self.currentObject()['updateTime']
    
    @property
    def createTime(self):
        return self.currentObject()['createTime']
    
    @property
    def action(self):
        self.changeDataSummary['action']
        
    @property
    def isDeleted(self):
        return self.action == 'delete'
    
    @property
    def isAdded(self):
        return self.action == 'create'
    
    @property
    def isUpdated(self):
        return self.action == 'update'
            
    @property
    def didChange(self):
        changed = False
        for changedField in self.changedFields:
            if changedField not in self.ignore_fields:
                changed = True
            if changed:
                break
        return changed
        
    def processUpdate(self,processValue):
        try:
            return self._processUpdate(processValue)
        except Exception as e:
            print(f"Error processing the {processValue} in the event.")
            print(self.event[processValue])
            msg = traceback.format_exc()
            print(msg)
        
    def _processUpdate(self,processValue):
        updateDict = self.event[processValue]
        if len(list(updateDict)) == 0 or updateDict is None:
            return None
        
        parsedData = {}
        path = updateDict['name']
        srch = 'databases/(default)/documents/'
        path = path[(path.find(srch))+len(srch):]
        parsedData['path'] = path
        parsedData['updateTime'] = updateDict['updateTime']
        parsedData['createTime'] = updateDict['createTime']
        parsedData['data'] = self.processFields(updateDict)
        return parsedData
        
    def getBool(self,inValue):
        return bool(inValue)
    
    def getInt(self,inValue):
        return int(inValue)
    
    def getFloat(self,inValue):
        return float(inValue)
    
    def getStr(self,inValue):
        return str(inValue)
    
    def getNone(self,_):
        return None

    def getLatLong(self,inValue):
        return inValue

    def getArrayValue(self,inValue):
        arrEntries = inValue.get('values',[])
        fieldsArray = []
        for arrEntry in arrEntries:
            arrFirstEntry = list(arrEntry.items())[0]
            mapFuncStr = self.function_map[arrFirstEntry[0]]
            mapFunc = getattr(self,mapFuncStr)
            mapFuncResult = mapFunc(arrFirstEntry[1])
            fieldsArray.append(mapFuncResult)
        return fieldsArray

    def getMapValue(self,inValue):
        return self.processFields(inValue)

    def processFields(self,inValue):
        fieldNames = list(inValue['fields'].keys())
        fieldEntries = inValue['fields']
        fieldsDict = {}

        for fieldName in fieldNames:
            #print(f'processing: {fieldName}')
            entry = list(fieldEntries[fieldName].items())[0]
            funcStr = self.function_map[entry[0]]
            func = getattr(self,funcStr)
            fieldsDict[fieldName] = func(entry[1])

        return fieldsDict