# -*- coding: utf-8 -*-
# danzi.tn@20170117 gestione Consulenze e link Target
import urllib2,ssl
import json
import urllib
import logging
import collections
from hashlib import md5

log = logging.getLogger()

class VtigerCli:
    # Vtiger Parameters    
    dictEntities = collections.defaultdict(list)
    gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)

    def __init__(self,vtigerserver,username,accessKey):
        self.accessKey = accessKey
        self.vtigerserver = vtigerserver
        self.url = '%s/webservice.php' % self.vtigerserver
        self.username = username
        ### let's set up the session
        # get the token using 'getchallenge' operation
        values = {'operation':'getchallenge','username': self.username }
        data = urllib.urlencode(values)
        req = urllib2.Request('%s?%s' % (self.url,data))
        
        response = urllib2.urlopen(req,context=self.gcontext).read()
        
        token = json.loads(response)['result']['token']
        
        # use the token to + accesskey to create the tokenized accessKey
        key = md5(token + self.accessKey)
        tokenizedAccessKey = key.hexdigest()
        values['accessKey'] = tokenizedAccessKey
        
        # now that we have an accessKey tokenized, let's perform a login operation 
        values['operation']  = 'login'
        data = urllib.urlencode(values)
        req = urllib2.Request(self.url, data)
        response = urllib2.urlopen(req,context=self.gcontext)
        response = json.loads(response.read())
        print(  "######## login as {0} ".format(self.username) )
        if not response["success"]:
            print( "ERRORE: login failed" )
            exit(1)
        
        self.userId = response["result"]["userId"]
        print(  "\tuser id = {0} ".format(self.userId) )
        # set the sessionName
        self.sessionName = response['result']['sessionName']   


    def queryVtiger(self, sQuery):
        values = {}
        values['sessionName'] = self.sessionName
        values['operation'] = 'query'
        values['query'] =  sQuery
        data = urllib.urlencode(values)
        req = urllib2.Request("%s?%s" % (self.url,data))
        response = urllib2.urlopen(req,context=self.gcontext)
        json_data = {'success':False}
        try:
            json_data = json.loads(response.read())
        except ValueError, e:
            log.error("Error on decoding JSON data in queryVtiger sQuery={0}".format(sQuery) )
            json_data['error'] = '{0}'.format(e)
        return json_data
    
    
    def createVtiger(self, sElementType, elementDict):
        values = {}
        values['sessionName'] = self.sessionName
        values['operation'] = 'create'
        values['elementType'] =  sElementType
        values['element'] = json.dumps(elementDict)
        data = urllib.urlencode(values)
        req = urllib2.Request(self.url,data)
        response = urllib2.urlopen(req,context=self.gcontext)
        json_data = {'success':False}
        try:
            json_data = json.loads(response.read())
        except ValueError, e:
            log.error("Error on decoding JSON data in createVtiger: sElementType={1} - elementDict={0}".format(elementDict,sElementType) )
            json_data['error'] = '{0}'.format(e)
        return json_data
    
    def createLinks(self, elementListDict):
        values = {}
        values['sessionName'] = self.sessionName
        values['operation'] = 'link_entities'
        values['element'] = json.dumps(elementListDict)
        data = urllib.urlencode(values)
        req = urllib2.Request(self.url,data)
        response = urllib2.urlopen(req,context=self.gcontext)
        json_data = {'success':False}
        try:
            json_data = json.loads(response.read())
        except ValueError, e:
            log.error("Error on decoding JSON data in createLinks elementListDict={0}".format(elementListDict) )
            json_data['error'] = '{0}'.format(e)
        return json_data
        
    def updateVtiger(self, sElementType, elementDict):
        values = {}
        values['sessionName'] = self.sessionName
        values['operation'] = 'update'
        values['elementType'] =  sElementType
        values['element'] = json.dumps(elementDict)
        data = urllib.urlencode(values)
        req = urllib2.Request(self.url,data)
        response = urllib2.urlopen(req,context=self.gcontext)
        json_data = {'success':False}
        try:
            json_data = json.loads(response.read())
        except ValueError, e:
            log.error("Error on decoding JSON data in updateVtiger: sElementType={1} - elementDict={0}".format(elementDict,sElementType) )
            json_data['error'] = '{0}'.format(e)
        return json_data
        