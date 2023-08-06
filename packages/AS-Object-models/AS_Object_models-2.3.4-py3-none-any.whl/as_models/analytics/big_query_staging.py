from google.cloud import bigquery
import pandas as pd
import jmespath, os, logging
from datetime import datetime,date, timedelta


logger = logging.getLogger('ColorOrchids_DataStaging')

class DataStaging(object):
    '''
    The purpose of this class is to take an object that represents a json object
    and call the following functions
    
    1. clean: prep the data for loading
    2. flatten: will flatten the object and return a dict flattened
    3. get_schema: returns the schema used for this object
    
    This will prep the data to be loaded into BigQuery
    '''
    
    BIGQUERY_FIELDS = {'timestamp':{'field_type':'DATETIME','name': 'added_dt','description':'The date/time that the object was created'},
                    'up_timestamp':{'field_type':'DATETIME','name': 'updated_dt','description':'The date/time that the object was last updated'},
                    'data_type':{'field_type':'STRING','description':'The data type that identifies this data row'},
                    'id':{'field_type':'STRING','description':'Unique identifier for this element in the collection'},
                    'collection':{'field_type':'STRING','description':'The collection name where this object was housed'},
                    'parent_id':{'field_type':'STRING','description':'the unique identifier of the parent object'},
                    'parent_collection':{'field_type':'STRING','description':'the parent collection where the parent object is housed'},
                    'added_by':{'field_type':'STRING','description':'The name of the individual that added this object'},
                    'updated_by':{'field_type':'STRING','description':'The name of the individual that updated this object last'},
                    'added_dt':{'field_type':'DATETIME','description':'The date/time that the object was created'},
                    'updated_dt':{'field_type':'DATETIME','description':'The date/time that the object was last updated'},
                    'path':{'field_type':'STRING','description':'String representation of where this object is located on the database'}}

    def __init__(self):
        pass