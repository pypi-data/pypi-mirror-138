from .utils import FireStoreBase
from datetime import datetime

class DebugApplication(object):
    
    DEBUG_DOC_ID = 'DebuggingApplication'
    
    def __init__(self, applicationName):
        self.appName = applicationName
        self.quickStorage = QuickStorage.GetQuickStorage(DebugApplication.DEBUG_DOC_ID,application='all')
        if self.quickStorage is None:
            self.quickStorage = QuickStorage.quickSet(DebugApplication.DEBUG_DOC_ID,{"debug":{applicationName:False}})
        
        self.debugMap = self.quickStorage.qsValue.get('debug',{})
        if self.debugMap.get(self.appName,None) is None:
            self.setDebugOff()
        
    @property
    def doDebug(self):
        return self.debugMap.get(self.appName,False)
    
    def setDebugOn(self):
        self.debugUpdate(True)
    
    def setDebugOff(self):
        self.debugUpdate(False)
    
    def debugUpdate(self,onOffValue):
        self.debugMap[self.appName] = onOffValue
        QuickStorage.quickUpdate(DebugApplication.DEBUG_DOC_ID,f"debug.{self.appName}",onOffValue)
    
    @classmethod
    def DoDebug(cls,applicationName):
        return DebugApplication(applicationName).doDebug

class QuickStorage(FireStoreBase):
    '''
    Found there are limitations to memcache... so we're creating a quickstorage... basically..
    if we want to return a lot of data... that exists in multiple places.. we'll store it here as a key/value pair
    '''
    COLLECTION_NAME = 'quick_storage'
    ext_fields = ['qsKey','qsValue','qsMinsAlive','qsTimeSet','qsNeverExpire']
    
    def __init__(self,fsClient, **kwargs):
        self.qsKey = kwargs.get('qsKey','--nokey--') #ndb.StringProperty()
        self.qsValue = kwargs.get('qsValue','') #ndb.BlobProperty()
        self.qsMinsAlive = kwargs.get('qsMinsAlive',60)
        self.qsMinsAlive = int(self.qsMinsAlive)
        self.qsTimeSet = kwargs.get('qsTimeSet',datetime.now().isoformat())
        self.qsNeverExpire = kwargs.get('qsNeverExpire',False)
        super(QuickStorage,self).__init__(fsClient,**kwargs)

    def base_path(self):
        return QuickStorage.__basePath(self._fsClient)

    @classmethod
    def get_application_path(cls,application_name=None):
        if application_name is None:
            return cls.basePath()
        else:
            client = cls.get_client()
            return f'{cls.COLLECTION_NAME}/{client.company}/{application_name}'


    @classmethod
    def basePath(cls):
        return cls.__basePath(cls.get_client())

    @classmethod
    def __basePath(cls,inClient):
        return cls.COLLECTION_NAME+'/'+inClient.company+'/'+inClient.application

    @classmethod
    def getInstance(cls,fsDocument):
        ref,snap = cls.getDocuments(fsDocument)
        docDict = cls.snapToDict(snap)
        docDict['fs_docSnap'] = snap
        docDict['fs_docRef'] = ref
        return cls(cls.get_client(),**docDict)
    
    @classmethod
    def GetQuickStorage(cls,inKey,application):
        return cls.__get_qs(inKey,application)

    @classmethod
    def __get_qs(cls,inKey, application=None):
        qs = cls.getInstance(cls.get_firestore_client().document(cls.get_application_path(application_name=application)+'/'+inKey))
        if qs.exists:
            setTime = datetime.fromisoformat(qs.qsTimeSet)
            diffMins = (datetime.now() - setTime).total_seconds() / 60.0
            if diffMins > qs.qsMinsAlive and not qs.qsNeverExpire:
                qs.reference.delete()
                return None
            else:
                return qs
        return None

    @classmethod
    def getValue(cls,inKey, application=None):
        '''
        :param inKey: string value
        :return: string value
        '''
        qs = cls.__get_qs(inKey,application=application)
        if qs:
            return qs.qsValue
        return None

    @classmethod
    def deleteValue(cls,inKey,application=None):
        '''
        :param inKey: string value
        '''
        qs = cls.getInstance(cls.get_firestore_client().document(cls.get_application_path(application_name=application)+'/'+inKey))
        if qs.exists:
            qs.reference.delete()
    
    @classmethod
    def quickSet(cls,inKey,inValue):
        '''
        Quick Set is used to set a forever value really quickly... using direct, will default to be stored under "all"

        :param inKey: Stored by this value
        :param inValue:  the value to be set
        '''
        docRef = cls.get_firestore_client().document(cls.get_application_path(application_name="all")+'/'+inKey)
        qsValue = {
            "dnl":inKey,
            "qsKey":inKey,
            "qsMinsAlive":0,
            "qsNeverExpire":True,
            "qsTimeSet": datetime.now().isoformat(),
            "qsValue":inValue
        }
        docRef.set(qsValue)

    @classmethod
    def quickUpdate(cls,inKey,updateKey,updateValue):
        ''''
        Quick update is used to update a forever value really quickly... using direct, and will use "all" as the default
        :param inKey: Stored by this value
        :param updateValue:  The update path of the value
        '''
        docRef = cls.get_firestore_client().document(cls.get_application_path(application_name="all")+'/'+inKey)
        qsUpdateValue = {
            f"qsValue.{updateKey}":updateValue,
            "qsTimeSet": datetime.now().isoformat(),
        }
        docRef.update(qsUpdateValue)

    @classmethod
    def setValue(cls,inKey, inValue, expireMins=None, neverExpire=False,application=None):
        '''
        :param inKey: string value...
        :param inValue: should be of type dict... it will be converted to a string
        :param expireMins:  how long should this value be stored (default is 60 mins)
        :return:  nada
        '''
        qs = cls.__get_qs(inKey,application=application)
        if qs:
            qs.qsValue = inValue
            qs.qsNeverExpire = neverExpire
            if expireMins:
                qs.qsMinsAlive = expireMins
        else:
            data = {}
            clt = cls.get_client()
            data['qsKey'] = inKey
            data['qsValue'] = inValue
            data['qsNeverExpire'] = neverExpire
            if expireMins:
                data['qsMinsAlive'] = expireMins
            data['fs_docRef'] = clt.fsClient.document(cls.get_application_path(application_name=application)+'/'+inKey)
            qs = QuickStorage(clt.fsClient,**data)

        qs.update_ndb()