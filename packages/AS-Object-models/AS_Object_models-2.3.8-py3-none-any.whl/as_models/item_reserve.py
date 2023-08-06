import re
from google.api_core.protobuf_helpers import get

from .storage_blob import StorageBlob
from .sales_inv_utils import SalesInvBase
from .item_week import ItemWeek
from . import FSDocument
from .inventory_active_items import InventoryTracking, InventoryLocation
from datetime import datetime
import logging

from . import GetInstance

class ItemReserve(SalesInvBase):
    """ This is the plant that is being reserved by a customer 
    {
            customer: {
                id: customer-79164,
                name: Test Customer,
                type: Legacy, ## Can be either legacy or item_tracking
                path: application_data/Color_Orchids/....
            },
            id: ProductReserve-459726,
            finish_week: 2019_49,
            num_reserved: 485,
            item: {
                id: Product-4791597, # Or in the future will be Cust_Plant_Item-2976,
                name: Bonita X Umbra,
                type: Legacy, ## can be either legacy or item_tracking
                path: application_data/Color_orchids/....
            },
            plants: [  # copied from ProductPlant or from now on from the Recipe
                {
                    plant: {
                        id: Plant-197111, ## in the future will be Recipe_Costing-4975
                        name: Bonita
                        type: Legacy, ## Can be either legacy or item_tracking
                        path: application_data/Color_Orchids/....
                    } ,
                    qty: 2   
                },
                {
                    plant: {
                        id: Plant-197411, ## in the future will be Recipe_Costing-4975
                        name: Mini Succulent,
                        type: Legacy, ## Can be either legacy or item_tracking
                        path: application_data/Color_Orchids/....
                    } ,
                    qty: 1
                }
            ]
        }
    
    """

    ext_fields = ['customer','location','inventory_location','inv_loc_override','finish_week', 'reserve_date',
                  'num_reserved','item','recipe_items','custom_plant_item','soft_delete','parent_path','path']
    
    COLLECTION_NAME = 'application_data'
    NAME = 'Reserves'

    def __init__(self, fsClient, **kwargs):
        self.soft_delete = kwargs.get('soft_delete',False)
        self.custom_plant_item = kwargs.get('custom_plant_item',False)
        self.customer = kwargs.get('customer',None) 
        self.location = kwargs.get('location',None)
        self._location_id = None
        if self.location is not None:
            self._location_id = self.location.get('id',None)
            
        self._inventory_location = kwargs.get('inventory_location',None)
        self._inv_loc_override = kwargs.get('inv_loc_override',False)
        self.finish_week = kwargs.get('finish_week','')
        self._reserve_date = kwargs.get('reserve_date','')
        self.num_reserved = kwargs.get('num_reserved','') 
        self.item = kwargs.get('item',None) 
        self._in_growWeekParent = kwargs.get('_growWeekParent',None)
        self.inventTracking = InventoryTracking.getInstance()
        self._inventoryItems = self.inventTracking.tracked_items
        #self._type_to_field = {'Plants':'Plants','Vase':'Vase_Style'}
        for itemType in self.inventTracking.tracked_items:
            setattr(self,itemType.replace(" ","_"),kwargs.get(itemType,None))
        self.recipe_items = kwargs.get('recipe_items',[])
        super(ItemReserve, self).__init__(fsClient, **kwargs)
        
    
    def base_path(self):
        return ItemReserve.basePath()
    
    @classmethod
    def basePath(cls):
        return ItemReserve.__basePath(ItemReserve.get_client())

    @classmethod
    def __basePath(cls,inClient):
        return cls.__growWeekBasePath+'/Reserves'

    @classmethod
    def __growWeekBasePath(cls):
        return ItemReserve.COLLECTION_NAME+'/'+ItemReserve.get_client().company+'/Sales_Inventory/Converted/GrowWeek'
    
    @classmethod
    def _getReservePath(cls,finishWeek,reserveId):
        return f"{cls.__growWeekBasePath()}/{finishWeek}/Reserves/{reserveId}"

    @property
    def _growWeekParent(self):
        if self._in_growWeekParent is None:
            gwParDoc = self.get_firestore_client().document(ItemReserve.__growWeekBasePath()+'/'+self.finish_week)
            self._in_growWeekParent = GetInstance("GrowWeek",gwParDoc)
        return self._in_growWeekParent
    
    @property
    def inventory_location(self):
        if self._inventory_location is None:
            self._inventory_location = InventoryLocation.getInstance().default_location
        return self._inventory_location
    
    @property
    def inv_loc_override(self):
        if self._inv_loc_override is None:
            self._inv_loc_override = False
        return self._inv_loc_override
        
    @property
    def parent_path(self):
        return self._growWeekParent.path

    @property
    def customer_id(self):
        return self.customer.get('id','No_Customer_Id')

    @property
    def location_id(self):
        if self._location_id is None:
            self._location_id = self.location.get('id',None)
        return self._location_id
    
    @property
    def product_id(self):
        return self.item.get('id','No_Product_Id')

    @property
    def reserve_date(self):
        '''
        If the reserve date is set.. use it.. otherwise default to monday of the GrowWeek
        '''
        if self._reserve_date is None or self._reserve_date == '':
            self._reserve_date = self._growWeekParent.week_monday
        if isinstance(self._reserve_date, datetime):
            self._reserve_date = self._reserve_date.isoformat()
        return self._reserve_date
    
    def update_inventory_location(self,invLoc):
        if self.isNotEmptyNull(invLoc):
            self._inventory_location = invLoc
        #  Inventory Location can be set from Reserve, Item and Location 10/26/2021
        #if self.location is not None:
        #    self.location['inventory_location'] = invLoc
    
    def set_location_id(self,inLocationId):
        self._location_id = inLocationId

    def getDefaultInventoryLocation(self):
        item_path = self.item['path']
        location_path = self.location['path']
        return ItemReserve.GetDefaultInventoryLocationByPath(item_path,location_path)
    
    @classmethod
    def GetDefaultInventoryLocationById(cls, item_id, location_id):
        def_inv_loc = ItemReserve.GetInvLocationFromSBObj(StorageBlob.getInstanceByDNL(item_id))
        if cls.IsEmptyNull(def_inv_loc):
            def_inv_loc = ItemReserve.GetInvLocationFromSBObj(StorageBlob.getInstanceByDNL(location_id))
            if cls.IsEmptyNull(def_inv_loc):
                def_inv_loc = InventoryLocation.getInstance().default_location
        return def_inv_loc

    @classmethod
    def GetDefaultInventoryLocationByPath(cls, item_path, location_path):
        def_inv_loc = ItemReserve.GetInvLocationFromSBObj(StorageBlob.getInstanceByPath(item_path))
        if cls.IsEmptyNull(def_inv_loc):
            def_inv_loc = ItemReserve.GetInvLocationFromSBObj(StorageBlob.getInstanceByPath(location_path))
            if cls.IsEmptyNull(def_inv_loc):
                def_inv_loc = InventoryLocation.getInstance().default_location
        return def_inv_loc

    @classmethod
    def GetInvLocationFromSBObj(cls, sbObj):
        return getattr(sbObj,'inventory_location',None)

    def refresh_inventory_location(self):
        if self._inv_loc_override == False:
            def_inv_loc = self.getDefaultInventoryLocation()
            if self.isNotEmptyNull(def_inv_loc):
                self.update_inventory_location(def_inv_loc)
    
    def duplicate_reserve(self, inv_loc=None):
        docRef = self._growWeekParent.get_reserve_reference() #gwParent.get_reserve_reference()
        if inv_loc is None:
            inv_loc = self.inventory_location
        return ItemReserve.create_reserve(docRef, self.customer_id, self.location_id, self.product_id, self.num_reserved, self.finish_week, self.reserve_date, inv_loc)

    @classmethod
    def getInstance(cls,fsDocument):
        ref,snap = ItemReserve.getDocuments(fsDocument)
        docDict = snap.to_dict() if snap.exists else {}
        docDict['fs_docSnap'] = snap
        docDict['fs_docRef'] = ref
        return ItemReserve(ItemReserve.get_firestore_client(),**docDict)

    @classmethod
    def getItemReserveInstance(cls,reserveId, growWeek=None):
        if growWeek is None:
            return ItemReserve.GetByDNL(reserveId,ItemReserve)
        return cls.getInstance(FSDocument.getInstance(cls._getReservePath(growWeek,reserveId)))
    
    @classmethod
    def getMatchingReservesByItem(cls,item_id, week_id=None):
        q = ItemReserve.get_firestore_client().collection_group('Reserves')
        q = q.where('item.id','==',item_id)
        if week_id is not None:
            q = q.where('finish_week','>=',week_id)
        docs = [doc for doc in q.stream()]
        return [ItemReserve.getInstance(doc) for doc in docs]

    @classmethod
    def get_active(cls):
        return ItemReserve.GetActive('Reserves',ItemReserve)

    def get_schema(self):
        schema = self.get_bq_schema()
        schema['fields'].append({'field_name':'customer_id','field_type':'int','field_required':True})
        schema['fields'].append({'field_name':'finish_week_id','field_type':'int','field_required':True})
        schema['fields'].append({'field_name':'product_id','field_type':'int','field_required':True})
        schema['fields'].append({'field_name':'num_reserved','field_type':'int'})
        #schema['fields'].append({'field_name':'shipped','field_type':'boolean'})
        ## Extra Fields from DB Stuff ##
        schema['fields'].append({'field_name':'plant_name','field_type':'string'}) ## saved as "plant"
        schema['fields'].append({'field_name':'vase_name','field_type':'string'}) ## saved as "plant"
        schema['fields'].append({'field_name':'product_name','field_type':'string'}) ## saved as "product"
        schema['fields'].append({'field_name':'customer_name','field_type':'string'}) ## saved as "customer"
        return schema

    def get_values_dict(self):
        values = self.get_dict()
        values['customer_id'] = self.customer
        values['finish_week_id'] = self.finish_week
        values['product_id'] = self.item
        values['num_reserved'] = self.num_reserved
        #values['shipped'] = self.shipped
        ## get db fields ##
        dbDict = self.get_db_reserve2()
        values['plant_name'] = dbDict['plant']
        values['vase_name'] = dbDict['vase']
        values['product_name'] = dbDict['product']
        values['customer_name'] = dbDict['customer']
        return values

    def get_reserved(self):
        if self.num_reserved:
            return self.num_reserved
        return 0

    @classmethod
    def get_db_reserve(cls, res_id):
        '''
        During conversion, we need to register the id in DataNumberLookup.... to avoid collection collisions.. prefix with "DNL"
        i.e. DNL_Plant_Item
        This will make finding things faster... which we will use to implement "Get By ID" methodology
        '''
        pr = SalesInvBase.GetByDNL(res_id,ItemReserve)
        if pr:
            return pr.get_db_reserve2()
        return None

    @classmethod
    def get_reserves_for_week(cls,argWeek):
        col = ItemReserve.get_firestore_client().collection(argWeek.path+'/'+ItemReserve.NAME)
        docRefs = col.list_documents()
        return [ItemReserve.getInstance(x) for x in docRefs]

    @classmethod
    def hardDelete(cls,argId):
        pr = SalesInvBase.GetByDNL(argId,ItemReserve)
        SalesInvBase.DeleteByDNL(pr.id)
        pr.delete_resp()
        return True

    @classmethod
    def delete(cls, argId):
        pr = SalesInvBase.GetByDNL(argId,ItemReserve)
        if pr:
            pr.soft_delete = True
            return pr.update_ndb()
        else:
            resp = {'status':'not applicable','msg':'Entity does not exist... nothing to delete'}
            return resp

    @classmethod
    def CreateCustomItem(cls,reserveId,itemId=None,growWeek=None):
        ir = ItemReserve.getItemReserveInstance(reserveId,growWeek)
        if ir is None:
            return None
        resp = {'reserve':ir,'item': ir._createCustomItem(itemId)}
        return resp
    
    def _createCustomItem(self,itemId=None):
        self.custom_plant_item = True
        
        if itemId is None:
            itemId = self.item['id']
            
        newItemObj = StorageBlob.createItemCopy(itemId,dnlExt=self.dnl)
        
        if newItemObj is None:
            raise Exception("Unable to copy an item that can't be found: "+itemId)
        self.item = ItemReserve.GetItemInfo(newItemObj)
        self.reference.update({"item":self.item, "custom_plant_item":True})
        return newItemObj.get_plant_item_data()

    @classmethod
    def GetItemSummary(cls,item_type,item):
        info = getattr(item,InventoryTracking.getInstance().type_to_field(item_type),None)
        
        sing = ItemWeek.CleanItemType(item_type)
        if info is not None:
            parts = str(info).split("|")
            #if StorageField().check_float(parts[0]) and str(parts[0]) != '':
            if ItemReserve.CheckFloat(parts[0]):
                info = [{sing:str(parts[0]),'qty':float(parts[0])}]
        else:
            return None

        ret = []
        if isinstance(info,list):
            # it's an array... so we can make some assumptions
            ret = []
            for i in info:
                qty = 1
                itemEntry = None
                if isinstance(i,dict):
                    #itemEntry = self._get_recipe_costing_item(item_type,i[sing])
                    itemEntry = cls.GetItemRecipe(item_type,i[sing])
                    qty = i.get('qty',1)
                    
                else:
                    #itemEntry = self._get_recipe_costing_item(item_type,i)
                    itemEntry = cls.GetItemRecipe(item_type,i)
                
                if itemEntry is not None:
                    itemEntry['qty'] = qty
                    ret.append(itemEntry)
        else:
            #ret = self._get_recipe_costing_item(item_type,info)
            itemEntry = cls.GetItemRecipe(item_type,info)
            if itemEntry is not None:
                itemEntry['qty'] = 1
                ret.append(itemEntry)
        return ret

    def _get_reserve_info(self, item_id):
        return ItemReserve.GetReserveInfo(item_id,location=self.location,customer=self.customer,item=self.item)

    @classmethod
    def GetReserveInfo(cls, item_id=None,location_id=None, location=None,customer=None,item=None):
        
        itemInfo = []
        locObj = None
        custObj = None
        itemObj = None

        if location is None:
            if location_id is not None:
                locObj = cls.GetSbByDNL(location_id)
                location = cls.GetLocInfo(locObj)
        
        if customer is None:
            if locObj is not None:
                custObj = cls.GetSbInstanceByPath(locObj.parent_doc_path)
                customer = cls.GetCustInfo(custObj)

        if item is not None:
            if item_id is None:
                item_id = item.get('id',None)
            
        itemObj = cls.GetSbByDNL(item_id)

        if itemObj is not None:
            itemInfo = cls.GetRecipeInfo(itemObj)
            #if item is None:
            item = cls.GetItemInfo(itemObj)

            if location is None:
                if itemObj.data_type != 'Copies':
                    locObj = cls.GetSbInstanceByPath(itemObj.parent_doc_path)
                    location = cls.GetLocInfo(locObj)
                else:
                    print("!! WARNING !! This is a custom item and the location is being pulled from original item path")
                    fsDoc = FSDocument.getInstance(itemObj.orig_path)
                    locObj = cls.GetSbInstanceByPath(fsDoc.location_path)
                    location = cls.GetLocInfo
                    
            if customer is None:
                if locObj is not None:
                    custObj = cls.GetSbInstanceByPath(locObj.parent_doc_path)
                    customer = cls.GetCustInfo(custObj)


        return {'customer':customer, 'location':location, 'item': item, 'recipe_items': itemInfo}
    
    @classmethod
    def GetRecipeInfo(cls,plantItemObj):
        itemInfo = []
        for itemType in InventoryTracking.getInstance().tracked_items:
            entry = {}
            entry['name'] = itemType
            info = cls.GetItemSummary(itemType,plantItemObj)
            if info is not None:
                entry['info'] = info
                itemInfo.append(entry)
        return itemInfo

    
    def _update_recipe_values(self,reserveInfo):
        self.recipe_items = ItemReserve.LoadRecipeValues(reserveInfo,self)

    @classmethod
    def GetRecipeValues(cls,rsvObj):
        rInfo = rsvObj._get_reserve_info(rsvObj.item.get('id',None))
        return cls.LoadRecipeValues(cls,rInfo,rsvObj)
    
    @classmethod
    def GetRecipeSummary(cls,item_id):
        reserveInfo = cls.GetReserveInfo(item_id)
        return cls.LoadRecipeValues(reserveInfo)

    @classmethod
    def LoadRecipeValues(cls,reserveInfo,rsvObj=None):
        recipe_arr = []
        for i in reserveInfo['recipe_items']:
            entry = i['info']
            # Replace spaces with underscore... helps for jmespath expressions
            if rsvObj is not None:
                setattr(rsvObj,i['name'].replace(" ","_"),entry)
                rsvObj._add_field(i['name'].replace(" ","_"))

            for d in entry:
                d['customer'] = reserveInfo['customer']['name']
                d['location'] = reserveInfo['location']['name']
                d['reserved_item'] = reserveInfo['item']['name']
                d['inventory_location'] = reserveInfo['location']['inventory_location']
                recipe_arr.append(d)

        return recipe_arr
    
    def _update_from_saved(self):
        logging.warning(f"Can not find the item, will be updating based on saved info in reserve: {self.id}, item: {self.item['id']}")
        saved_info = []
        if self.Plants is not None:
            saved_info.append({'name':'Plants','info':self.Plants})
        
        if self.Vase is not None:
            saved_info.append({'name':'Vase','info':self.Vase})
        
        savedUpdateInfo = {'customer':self.customer, 'location':self.location, 'item': self.item, 'recipe_items': self.saved_info}
        self._update_recipe_values(savedUpdateInfo)

        
    @classmethod
    def create_reserve(cls,docRef, customer_id, location_id, item_id, reserved, finish_week, reserveDate=None, inventory_location=None):
        ir = ItemReserve.getInstance(docRef)
        ir.set_location_id(location_id)
        ir.customer = ir._get_cust_info(ir._get_sb_by_dnl(customer_id))
        ir.location = ir._get_loc_info(ir._get_sb_by_dnl(location_id),InventoryLocation.getInstance().default_location)
        ir.item = ir._get_item_info(ir._get_sb_by_dnl(item_id))
        reserveInfo = ir._get_reserve_info(item_id)

        if reserveInfo['item'] is None:
            raise Exception('Unable to find item information... for item: '+item_id)

        ir.num_reserved = int(reserved)
        ir.finish_week = finish_week
        # if it was passed in... use it
        # Update 10/26/2021:  No matter if it was passed or not... go get it
        default_inv_location = ir.getDefaultInventoryLocation()

        if ItemReserve.IsEmptyNull(inventory_location):
            # if it wasn't passed in...grab get Default Value
            inventory_location = default_inv_location
        
        if default_inv_location != inventory_location:
            #
            # If the inventory was overridden... do not update on a refresh 10.26.2021
            #
            ir._inv_loc_override = True

        ir.update_inventory_location(inventory_location)

        ir._reserve_date = reserveDate if isinstance(reserveDate,str) else reserveDate.isoformat()
        ir._update_recipe_values(reserveInfo)
        ir.update_ndb(True)
        ir._insert_dnl(docRef)
        return ir

    def set_inventory_location(self,inventory_location):
        if self.isNotEmptyNull(inventory_location):
            self.update_inventory_location(inventory_location)
            self.update_ndb()

    def update_reserve(self, customer_id, location_id, item_id, reserved, gwParent, reserveDate=None, inventory_location=None):
        
        if gwParent.id != self.finish_week:
            self.delete_resp()
            docRef = gwParent.get_reserve_reference()
            newIr = ItemReserve.create_reserve(docRef, customer_id, location_id, item_id, reserved, gwParent.id, reserveDate, inventory_location)
            newIr.custom_plant_item = self.custom_plant_item   #Make sure to preserve the fact that the original had a custom item
            return newIr

        # if it was passed in... use it
        default_inv_location = self.getDefaultInventoryLocation()
        if self.isEmptyNull(inventory_location):
            # if it wasn't passed in...grab get Default Value
            inventory_location = default_inv_location
            self.update_inventory_location(inventory_location)
        else:          
            if self.inventory_location != inventory_location:
                # Rather than try to fix everything... delete and recreate
                self.delete_resp()
                docRef = gwParent.get_reserve_reference()
                newIr = ItemReserve.create_reserve(docRef, customer_id, location_id, item_id, reserved, gwParent.id, reserveDate, inventory_location)
                newIr.custom_plant_item = self.custom_plant_item #Make sure to preserve the fact that the original had a custom item
                return newIr
        
        if default_inv_location != inventory_location:
            #
            # If the inventory was overridden... do not update on a refresh 10.26.2021
            #
            self._inv_loc_override = True

        reserveInfo = self._get_reserve_info(item_id)

        if reserveInfo['item'] is None:
            self._update_from_saved()
        else:
            self._update_recipe_values(reserveInfo)

        customer = self._get_cust_info(self._get_sb_by_dnl(customer_id))
        self.num_reserved = int(reserved)
        

        self._reserve_date = reserveDate if isinstance(reserveDate,str) else reserveDate.isoformat()
        self.customer = customer

        if reserveInfo['location'] is not None:
            self.location = reserveInfo['location']
        
        self.item = reserveInfo['item']
        self.update_ndb()
        return self

    def refresh(self,refreshInvLoc=False):
        if refreshInvLoc:
            #self.location = self._get_loc_info(self._get_sb_by_dnl(self.location['id']),InventoryLocation.getInstance().default_location)
            if self.inv_loc_override == False:
                defInvLoc = self.getDefaultInventoryLocation()
                if defInvLoc != self.inventory_location:
                    #
                    # The inventory location changed... delete this one.. which will trigger updates and create a new one...which will trigger updates
                    #
                    logging.info(f"Reserve: {self.id} had an inventory location change, deleting and duplicating")
                    newLocRes = self.duplicate_reserve(inv_loc=defInvLoc)
                    logging.info(f"Reserve {self.id} was deleted and recreated under id: {newLocRes.id}, because of inventory location change")
                    self.delete_resp()
                    return newLocRes
                else:
                    self.update_inventory_location(defInvLoc)
                
        reserveInfo = self._get_reserve_info(self.item['id'])
        if reserveInfo['item'] is None:
            self._update_from_saved()
        else:
            self._update_recipe_values(reserveInfo)

        self.update_ndb()
        return self