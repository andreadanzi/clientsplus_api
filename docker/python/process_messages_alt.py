# -*- coding: utf-8 -*-
# danzi.tn@20170117 gestione Consulenze e link Target
import os
import MySQLdb
import urllib2,ssl
import json
import urllib
import collections
import datetime
from hashlib import md5
import logging
import logging.handlers


log = logging.getLogger()
log.setLevel(logging.DEBUG)
if not os.path.exists("logs"):
    os.makedirs("logs")
file_handler = logging.handlers.RotatingFileHandler(os.path.join("logs","{0}.log".format(os.path.basename(__file__).split(".")[0])), maxBytes=5000000,backupCount=5)
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
file_handler.setFormatter(formatter)
log.addHandler(file_handler)
print("started on {0}".format( os.getcwd()) )
log.debug("started on {0}".format( os.getcwd()))
# "email":"pippo@pippo.com", "lastname":"bello", "firstname":"pippo", "newsletter_permission":1, "company":"example", "assigned_user_id":userId}
# {u'city': u'Roma', u'first_name': u'Mario', u'last_name': u'Rossi', u'tel': u'+391234567890', u'zip': u'12345', u'language': u'IT', u'country': u'IT', u'company': u'Mario Rossi Engineering', u'job': u'engineer', u'address': u'Piazza del Popolo 11', u'region': u'IT-62'}
keySubjects = {
                "registration":"WEB Registration for {0}",
                "newsletter_subscribe":"WEB Newsletter Subscrition for {0}",
                "newsletter_unsubscribe":"WEB Newsletter Unsubscrition for {0}",
                "consulting":"WEB consulting request for {0}",
                "download":"WEB download request for {0}",
                "new_course":"WEB new course publishing for {0}",
                "course_subscribe":"WEB Course Subscrition for {0}"
}
# target_type = "Iscrizione Corso"
# target_state = "Pronto"
# 
# cf_1225 codice fatturazione corso
# cf_1226 data inizio corso
# cf_1468 Fine Corso
# cf_1469 Lingua Corso
# cf_1470 ID Corso
# cf_1471 Titolo
# cf_1546 Message Log ID
keyTargetNames = {
                "registration":"WEB Registration",
                "newsletter_subscribe":"WEB Newsletter Subscrition",
                "newsletter_unsubscribe":"WEB Newsletter Unsubscrition",
                "consulting":"WEB Consulting Requests",
                "download":"WEB Download request for {0}",                
                "course_subscribe":"WEB Course Subscrition for {0}"
}
"""
<select id="txtbox_Scelta pernotto" name="overnight_option" class="detailedViewTextBox">
value="---" selected="">---</option>
value="Notte precedente al corso">Notte precedente al corso</option>
value="Notte del primo giorno di corso">Notte del primo giorno di corso</option>
value="Altro">Altro</option>
												</select>
            
            
            
<select id="txtbox_Modalità di partecipazione" name="cf_732" class="detailedViewTextBox">
<option value="--Nessuno--" selected="">--Nessuno--</option>
					<option value="Corso">Corso</option>
					<option value="Corso + cena">Corso + cena</option>
					<option value="Corso + cena + pernottamento">Corso + cena + pernottamento</option>
					<option value="Corso + pernottamento">Corso + pernottamento</option>
					<option value="Corso + cena + 2 pernottamenti">Corso + cena + 2 pernottamenti</option>
					<option value="Corso + 3 pernottamenti">Corso + 3 pernottamenti</option>
					<option value="Corso + 3 cene + 3 pernottamenti">Corso + 3 cene + 3 pernottamenti</option>
					<option value="Corso + 2 cene">Corso + 2 cene</option>
					<option value="Corso + 2 cene + 3 pernottamenti">Corso + 2 cene + 3 pernottamenti</option>
					<option value="Corso + 2 cene + 2 pernottamenti">Corso + 2 cene + 2 pernottamenti</option>
					<option value="Corso + 2 pernottamenti">Corso + 2 pernottamenti</option>
					<option value="Corso + 2 pranzi + 3 cene + 2 pernottamenti + transfer">Corso + 2 pranzi + 3 cene + 2 pernottamenti + transfer</option>
					<option value="Corso + 2 pranzi + 3 cene + 3 pernottamenti + transfer">Corso + 2 pranzi + 3 cene + 3 pernottamenti + transfer</option>
					<option value="Corso + 4 cene + 4 pernottamenti">Corso + 4 cene + 4 pernottamenti</option>
</select>
"""
keyLeadMapping = {"registration": {
                                    "email":"email",
                                    "first_name":"firstname",
                                    "last_name":"lastname",
                                    "city":"city",
                                    "zip":"code",
                                    "region":"state",
                                    "address":"lane",
                                    "telephone":"phone",
                                    "company":"company",
                                    "country":"country"
                                    },
                    "consulting": {
                                    "email":"email",
                                    "first_name":"firstname",
                                    "last_name":"lastname",
                                    "city":"city",
                                    "zip":"code",
                                    "region":"state",
                                    "address":"lane",
                                    "telephone":"phone",
                                    "company":"company",
                                    "country":"country"
                                    },
                    "course_subscribe": {
                                    "email":"email",
                                    "course_id":"cf_747",
                                    "plan":"cf_732",
                                    "intolerances":"cf_1396",
                                    "overnight_stay":"overnight_option"
                                    },
                     "new_course": {
                                    "email":"email",
                                    "id":"company",
                                    "language":"firstname",
                                    "name":"lastname"
                                    },
                     "download": {
                                    "description":"description"
                                    }
                  }

                  
                  
keyAccountMapping = {
                    "msg":"acc",
                    "msg":"acc",
                    "msg":"acc",
                    "msg":"acc",
                    "msg":"acc",
                    "msg":"acc",
                    }
                    
keyContactMapping = {
                    "msg":"acc",
                    "msg":"acc",
                    "msg":"acc",
                    "msg":"acc",
                    "msg":"acc",
                    "msg":"acc",
                    }

SiteMessage = collections.namedtuple('SiteMessage', ['idmessage_log','timestamp','idevent_types','type_event','idemail','email','email_import_status'] )

sHost = '10.88.102.73'
sPort = '3386'
sUser = 'root'
sPass = 'root'
sDB = 'clientsplus'



def queryVtiger(sURL,gContext, sSessionName, sQuery):
    values = {}
    values['sessionName'] = sSessionName
    values['operation'] = 'query'
    values['query'] =  sQuery
    data = urllib.urlencode(values)
    req = urllib2.Request("%s?%s" % (sURL,data))
    response = urllib2.urlopen(req,context=gContext)
    return json.loads(response.read())


def createVtiger(sURL,gContext, sSessionName, sElementType, elementDict):
    values = {}
    values['sessionName'] = sSessionName
    values['operation'] = 'create'
    values['elementType'] =  sElementType
    values['element'] = json.dumps(elementDict)
    data = urllib.urlencode(values)
    req = urllib2.Request(sURL,data)
    response = urllib2.urlopen(req,context=gContext)
    return json.loads(response.read())

def updateVtiger(sURL,gContext, sSessionName, sElementType, elementDict):
    values = {}
    values['sessionName'] = sSessionName
    values['operation'] = 'update'
    values['elementType'] =  sElementType
    values['element'] = json.dumps(elementDict)
    data = urllib.urlencode(values)
    req = urllib2.Request(sURL,data)
    response = urllib2.urlopen(req,context=gContext)
    return json.loads(response.read())
    
def setMessageLogStatus(host,port, user,password, database,idmessage_log,status):
    cnx = MySQLdb.connect(user=user, passwd=password,port=int(port),
                                  host=host,
                                  db=database)
    cursor = cnx.cursor()
    query = """UPDATE message_log
                SET import_status = {1}
                WHERE
                idmessage_log = {0}
                """.format(idmessage_log,status)
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()



def getCourseById(host,port, user,password, database,id_course):
    cnx = MySQLdb.connect(user=user, passwd=password,port=int(port),
                                  host=host,
                                  db=database)
    cursor = cnx.cursor()
    query = """SELECT 
                message.datastructure_name,
                CASE
                    WHEN message.datastructure_name in ("begins_at","ends_at") THEN from_unixtime(message.datastructure_value)
                    ELSE message.datastructure_value
                END AS datastructure_my_value ,
                event_types.event_type_code,
                datastructure.*
                FROM message, datastructure, event_types, message as message_index
                WHERE
		message_index.datastructure_name = 'id'
		AND event_types.event_type_code = 'new_course'
		AND message_index.datastructure_value = '{0}'
                AND message.message_log_idmessage_log = message_index.message_log_idmessage_log
                AND datastructure.iddatastructure = message.datastructure_iddatastructure
		AND event_types.idevent_types = datastructure.event_types_idevent_types""".format(id_course)
    cursor.execute(query)
    retDict = {}
    for row in cursor:
        retDict[row[0]] = row[1]
    cursor.close()
    cnx.close()
    return retDict

def getMessage(host,port, user,password, database,idmessage_log):
    cnx = MySQLdb.connect(user=user, passwd=password,port=int(port),
                                  host=host,
                                  db=database)
    cursor = cnx.cursor()
    query = """SELECT 
                message.datastructure_name,
                CASE
                    WHEN message.datastructure_name in ("begins_at","ends_at") THEN from_unixtime(message.datastructure_value)
                    ELSE message.datastructure_value
                END AS datastructure_my_value ,
                event_types.event_type_code,
                datastructure.*
                FROM message, datastructure, event_types
                WHERE
                message.message_log_idmessage_log = {0}
                AND datastructure.iddatastructure = message.datastructure_iddatastructure
		AND event_types.idevent_types = datastructure.event_types_idevent_types""".format(idmessage_log)
    cursor.execute(query)
    retDict = {}
    eventTypeCode = ""
    for row in cursor:
        retDict[row[0]] = row[1]
        eventTypeCode = row[2]
    cursor.close()
    cnx.close()
    return retDict, eventTypeCode

def getLastEventByType(host,port, user,password, database,type_event,by_email):
    cnx = MySQLdb.connect(user=user, passwd=password,port=int(port),
                                  host=host,
                                  db=database)
    cursor = cnx.cursor()
    query = """SELECT
                        max(message_log.idmessage_log),
                        max(message_log.timestamp),
                        message.datastructure_name,
                        CASE
                            WHEN message.datastructure_name in ("begins_at","ends_at") THEN from_unixtime(message.datastructure_value)
                            ELSE message.datastructure_value
                        END AS datastructure_my_value ,
                        event_types.event_type_code,
                        email.email_address
                FROM
                        message_log,
                        message,
                        datastructure,
                        event_types,
                        email
                WHERE
                        message_log.type_event = '{1}'
                	AND message_log.by_email = '{0}'
                	AND message.message_log_idmessage_log = message_log.idmessage_log
                	AND email.idemail = message.email_idemail
                	AND event_types.idevent_types=datastructure.event_types_idevent_types
                	AND datastructure.iddatastructure=message.datastructure_iddatastructure
                GROUP BY 
                        message.datastructure_name,
                        datastructure_my_value,
                        event_types.event_type_code,
                	email.email_address
                ORDER BY max(message.idmessage)""".format(by_email,type_event) 
    cursor.execute(query)
    retDict = {}
    idmessage_log = None
    timestamp = None
    eventTypeCode = None
    for row in cursor:
        idmessage_log = row[0]
        timestamp = row[1]
        retDict[row[2]] = row[3]
        eventTypeCode = row[4]
    cursor.close()
    cnx.close()
    return retDict, idmessage_log, timestamp, eventTypeCode




class MyVtiger:
    # Vtiger Parameters
    accessKey = 'BLmHQc0IvDXC665o'
    vtigerserver = 'https://crm.rothoblaas.com'
    #vtigerserver = 'http://10.88.102.73/vte'
    url = '%s/webservice.php' % vtigerserver
    username = 'webweb'
    
    dictTargets = {}
    dictEntities = collections.defaultdict(list)
    gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)

    def __init__(self):
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

        self.host = sHost 
        self.port = sPort        
        self.user = sUser
        self.password = sPass
        self.database = sDB
    


    def queryVtiger(self, sQuery):
        values = {}
        values['sessionName'] = self.sessionName
        values['operation'] = 'query'
        values['query'] =  sQuery
        data = urllib.urlencode(values)
        req = urllib2.Request("%s?%s" % (self.url,data))
        response = urllib2.urlopen(req,context=self.gcontext)
        return json.loads(response.read())
    
    
    def createVtiger(self, sElementType, elementDict):
        values = {}
        values['sessionName'] = self.sessionName
        values['operation'] = 'create'
        values['elementType'] =  sElementType
        values['element'] = json.dumps(elementDict)
        data = urllib.urlencode(values)
        req = urllib2.Request(self.url,data)
        response = urllib2.urlopen(req,context=self.gcontext)
        return json.loads(response.read())
    
    def createLinks(self, elementListDict):
        values = {}
        values['sessionName'] = self.sessionName
        values['operation'] = 'link_entities'
        values['element'] = json.dumps(elementListDict)
        data = urllib.urlencode(values)
        req = urllib2.Request(self.url,data)
        response = urllib2.urlopen(req,context=self.gcontext)
        return json.loads(response.read())
        
    def updateVtiger(self, sElementType, elementDict):
        values = {}
        values['sessionName'] = self.sessionName
        values['operation'] = 'update'
        values['elementType'] =  sElementType
        values['element'] = json.dumps(elementDict)
        data = urllib.urlencode(values)
        req = urllib2.Request(self.url,data)
        response = urllib2.urlopen(req,context=self.gcontext)
        return json.loads(response.read())    
    
    
    def addEventToEntity(self,retDict, entityItem, entityType ):
        result = None
        duedate = retDict["timestamp"] + datetime.timedelta(hours=1)
        sDescr = ""
        if "description" in retDict:
            sDescr = retDict["description"]
        eventDict = { 
                        "assigned_user_id":entityItem["assigned_user_id"], 
                        "activitytype":"website_{0}".format(retDict["type_event"]), 
                        "subject":keySubjects[retDict["type_event"]].format(retDict["email"]),
                        "date_start":retDict["timestamp"].strftime('%Y-%m-%d'),
                        "time_start":retDict["timestamp"].strftime('%H:%M'),
                        "due_date":duedate.strftime('%Y-%m-%d'),
                        "time_end":duedate.strftime('%H:%M'),
                        "eventstatus":"Held",
                        "description":sDescr,
                        "cf_1547": retDict["targetKey"]
                        }
        if entityType =='Contacts':
            eventDict["contact_id"] = entityItem["id"]
            if "account_id" in entityItem:
                eventDict["parent_id"] = entityItem["account_id"]
        else:
            eventDict["parent_id"] = entityItem["id"]
        
        if retDict["type_event"] == "consulting":
            eventDict["subject"] = "{0} ({1})".format(eventDict["subject"],retDict["category"])
            if "file" in retDict:
                eventDict["description"] = "{0}\n[{1}]".format(eventDict["description"],retDict["file"])
        if retDict["type_event"] == "course_subscribe":
            eventDict["subject"] = "{0} ({1})".format(eventDict["subject"],retDict["course_id"])
        if retDict["type_event"] == "new_course":
            eventDict["subject"] = "{0} {1} ({2})".format(eventDict["subject"],retDict["name"],retDict["id"])
        ret = self.createVtiger("Events", eventDict)            
        if ret["success"]:
            setMessageLogStatus(self.host,self.port,self.user,self.password,self.database,retDict["idmessage_log"],3)
            result = ret["result"]
        else:
            print( "ERRORE: Error on create event {0}".format(ret) )
            log.error( "ERRORE: Error on create event {0}".format(ret) )
            
            setMessageLogStatus(self.host,self.port,self.user,self.password,self.database,retDict["idmessage_log"],-5)
        return result
    
    def processEmail(self,retDict):
        result = None
        entityKey = None
        entityKey = retDict["email"]
        bNewsletter = True
        if retDict["type_event"] == "registration" and "newsletter" in retDict:
            bNewsletter = retDict["newsletter"] == "1"
        if entityKey in self.dictEntities:
            result = self.dictEntities[entityKey]
        else:
            # Search Leads
            sQueryLeads = "SELECT * FROM Leads WHERE leadsource != 'website_course_subscribe' AND email  = '{0}';".format(entityKey)
            ret = self.queryVtiger(sQueryLeads)
            if ret['success']:
                for item in ret['result']:
                    self.dictEntities[entityKey].append(('Leads',item, False))
                    print( "Trovato Leads con entityKey = {0} e id = {1}".format(entityKey,item["id"] ))
                    log.info( "Trovato Leads con entityKey = {0} e id = {1}".format(entityKey,item["id"] ))
            else:
                print( "ERRORE: Errore in ricerca Leads {0} [{1}] ".format( sQueryLeads, ret))
                log.error( "ERRORE: Errore in ricerca Leads {0} [{1}] ".format( sQueryLeads, ret))
                setMessageLogStatus(self.host,self.port,self.user,self.password,self.database,retDict["idmessage_log"],-1)
            
            # Search Accounts
            sQueryAccounts = "SELECT * FROM Accounts WHERE email1 = '{0}';".format(entityKey)
            ret = self.queryVtiger(sQueryAccounts)
            if ret['success']:
                for item in ret['result']:
                    self.dictEntities[entityKey].append(('Accounts',item, False))
                    print(  "Trovato Accounts con entityKey = {0} e id = {1}".format(entityKey,item["id"] ))
                    log.info(  "Trovato Accounts con entityKey = {0} e id = {1}".format(entityKey,item["id"] ))
            else:
                print( "ERRORE: Errore in ricerca Accounts {0} [{1}] ".format( sQueryAccounts, ret) )
                log.error( "ERRORE: Errore in ricerca Accounts {0} [{1}] ".format( sQueryAccounts, ret) )
                setMessageLogStatus(self.host,self.port,self.user,self.password,self.database,retDict["idmessage_log"],-2)
            
            # Search Contacts
            sQueryContacts = "SELECT * FROM Contacts WHERE email = '{0}';".format(entityKey)
            ret = self.queryVtiger(sQueryContacts)
            if ret['success']:
                for item in ret['result']:
                    self.dictEntities[entityKey].append(('Contacts',item, False))
                    print( "Trovato Contacts con entityKey = {0} e id = {1}".format(entityKey,item["id"] ) )
                    log.info( "Trovato Contacts con entityKey = {0} e id = {1}".format(entityKey,item["id"] ) )
            else:
                print( "ERRORE: Errore in ricerca Contacts {0} [{1}] ".format( sQueryContacts, ret) )
                log.error( "ERRORE: Errore in ricerca Contacts {0} [{1}] ".format( sQueryContacts, ret) )
                setMessageLogStatus(self.host,self.port,self.user,self.password,self.database,retDict["idmessage_log"],-3)
            
            if entityKey in self.dictEntities:
                setMessageLogStatus(self.host,self.port,self.user,self.password,self.database,retDict["idmessage_log"],1)
            else:
                bHasRegData = False
                if retDict["type_event"] == "registration" or retDict["type_event"] == "consulting":
                    bHasRegData = True
                else:
                    regDict, reg_idmessage_log, timestamp, eventTypeCode = getLastEventByType(self.host,self.port,self.user,self.password,self.database,"registration",retDict["email"])
                    if len(regDict) == 0:
                        print("ERRORE: manca registrazione per {0} {1}".format(retDict["email"],retDict["type_event"]))
                        log.error( "ERRORE: manca registrazione per {0} {1}".format(retDict["email"],retDict["type_event"]))
                        setMessageLogStatus(self.host,self.port,self.user,self.password,self.database,retDict["idmessage_log"],-6)
                    else:
                        print "Registrazione per {0} il {2} con id = {1}".format(retDict["email"],reg_idmessage_log, timestamp)
                        log.info( "Registrazione per {0} il {2} con id = {1}".format(retDict["email"],reg_idmessage_log, timestamp))
                        if "newsletter" in regDict:
                            bNewsletter = regDict["newsletter"] == "1"
                        for key in regDict:
                            keyMap = keyLeadMapping[regDict["type_event"]]
                            if key in keyMap:
                                elementDict[keyMap[key]] = regDict[key]
                        bHasRegData = True
                if bHasRegData:
                    elementDict = {"assigned_user_id":self.userId,"newsletter_permission":bNewsletter,"leadstatus":"Not Contacted", "leadsource":"website_{0}".format(retDict["type_event"]), "cf_744":"{0}".format(retDict["idmessage_log"])}                   
                    for key in retDict:
                        keyMap = keyLeadMapping[retDict["type_event"]]
                        if key in keyMap:
                            elementDict[keyMap[key]] = retDict[key]
                    ret = self.createVtiger("Leads", elementDict)
                    if ret["success"]:
                        bCourseAdded = False
                        if retDict["type_event"] == "course_subscribe":
                            bCourseAdded = True
                        self.dictEntities[entityKey].append(('Leads',ret["result"], bCourseAdded))
                        print( "Aggiunto nuovo Lead con entityKey = {0} e id = {1}".format(entityKey,ret["result"]["id"] ) )
                        log.info( "Aggiunto nuovo Lead con entityKey = {0} e id = {1}".format(entityKey,ret["result"]["id"] ) )
                        setMessageLogStatus(self.host,self.port,self.user,self.password,self.database,retDict["idmessage_log"],2)
                    else:
                        setMessageLogStatus(self.host,self.port,self.user,self.password,self.database,retDict["idmessage_log"],-4)
                        print( "ERRORE: Errore in creazione Lead {0} [{1}] ".format( elementDict, ret)) 
                        log.error( "ERRORE: Errore in creazione Lead {0} [{1}] ".format( elementDict, ret)) 
            result = self.dictEntities[entityKey]       
        return result

    def searchTarget(self,retDict):
        result = None
        targetKey = None
        targetname = None
        assignedUserId = self.userId
        cf_1470 = ""
        cf_1226 = ""
        cf_1468 = ""
        cf_1469 = ""
        cf_1471 = ""
        refId = "{0}_{1}".format(retDict["type_event"],retDict["idmessage_log"]) 
        if retDict["type_event"] == "new_course":
            targetKey =  "{0}_{1}".format(retDict["type_event"],retDict["id"])
            cf_1471 = "name"
            if "name" in retDict:
                targetname = "Corso WEB: {0} ({1})".format(retDict["name"], retDict["id"])
                cf_1471 = retDict["name"]
            else:
                targetname = "Corso WEB: Corso senza nome ({0})".format(retDict["id"])
                print( "ERRORE: {0}-{1} missing {2}".format(retDict["idmessage_log"],retDict["type_event"],"name"))
                log.error( "ERRORE: {0}-{1} missing {2}".format(retDict["idmessage_log"],retDict["type_event"],"name"))
            assignedUserId = "19x1705"
            targetType = "Iscrizione Corso"
            cf_1470 = retDict["id"]
            cf_1226 = retDict["begins_at"]
            cf_1468 = retDict["ends_at"]
            cf_1469 = retDict["language"]
        elif retDict["type_event"] == "download":
            if "description" in retDict:
                targetKey =  "{0}_{1}".format(retDict["type_event"],retDict["description"])
                targetType = "Download"
                targetname = "Download WEB: {0} {1}".format(retDict["type_event"],retDict["description"])
            else:
                print( "ERRORE: {0}-{1} missing {2}".format(retDict["idmessage_log"],retDict["type_event"],"description"))
                log.error( "ERRORE: {0}-{1} missing {2}".format(retDict["idmessage_log"],retDict["type_event"],"description"))
        elif retDict["type_event"] == "consulting":
            if "category" in retDict:
                targetKey =  "{0}_{1}".format(retDict["type_event"],retDict["category"])
                targetType = "Richiesta Consulenze (Form)"
                targetname = "Consulenza WEB: {0}".format(retDict["category"])
            else:
                print( "ERRORE: {0}-{1} missing {2}".format(retDict["idmessage_log"],retDict["type_event"],"category"))
                log.error( "ERRORE: {0}-{1} missing {2}".format(retDict["idmessage_log"],retDict["type_event"],"category"))
        elif retDict["type_event"] == "registration":
            targetKey =  retDict["type_event"]
            targetType = "Registrazione WEB"
            targetname = targetType
        elif retDict["type_event"] == "newsletter_subscribe":
            targetKey =  retDict["type_event"]
            targetType = "Newsletter Subscription WEB"
            targetname = targetType
        elif retDict["type_event"] == "newsletter_unsubscribe":
            targetKey =  retDict["type_event"]
            targetType = "Newsletter Unsubscription WEB"
            targetname = targetType
        elif retDict["type_event"] == "course_subscribe":
            if "course_id" in retDict:
                targetKey =  "new_course_{0}".format(retDict["course_id"])
                courseDict = getCourseById(self.host,self.port, self.user,self.password, self.database,retDict["course_id"])
                courseName = "Senza Nome"
                if "name" in courseDict:
                    courseName = courseDict["name"]
                targetname = "Corso WEB: {0} ({1})".format(courseName, courseDict["id"])
                assignedUserId = "19x1705"
                targetType = "Iscrizione Corso"
                cf_1470 = courseDict["id"]
                cf_1226 = courseDict["begins_at"]
                cf_1468 = courseDict["ends_at"]
                cf_1469 = courseDict["language"]
                cf_1471 = courseName
            else:
                print( "ERRORE: {0}-{1} missing {2}".format(retDict["idmessage_log"],retDict["type_event"],"course_id") )
                log.error( "ERRORE: {0}-{1} missing {2}".format(retDict["idmessage_log"],retDict["type_event"],"course_id") )
        if targetKey:
            if targetKey in self.dictTargets: 
                result = self.dictTargets[targetKey]
                print(  "trovato TARGET {0} {1} nella cache con key = {2}".format(result["id"], result["targetname"], targetKey ))
                log.info(  "trovato TARGET {0} {1} nella cache con key = {2}".format(result["id"], result["targetname"], targetKey ))
                if retDict["type_event"] == "new_course":
                    setMessageLogStatus(self.host,self.port,self.user,self.password,self.database,retDict["idmessage_log"],1)
            else:
                sQueryTargets = "SELECT * FROM Targets WHERE cf_1545 = '{0}';".format(targetKey)
                ret = self.queryVtiger(sQueryTargets)
                if ret['success']:
                    for item in ret['result']:
                        result = item
                    if( result ):
                        self.dictTargets[targetKey] = result
                        print(  "trovato TARGET {0} {1} in VTE con cf_1545 = {2}".format(result["id"], result["targetname"], targetKey ))
                        log.info(  "trovato TARGET {0} {1} in VTE con cf_1545 = {2}".format(result["id"], result["targetname"], targetKey ))
                        if retDict["type_event"] == "new_course":
                            setMessageLogStatus(self.host,self.port,self.user,self.password,self.database,retDict["idmessage_log"],2)
                    else:
                        targetDict = {"targetname":targetname,  
                                       "assigned_user_id":assignedUserId,   
                                       "target_type" : targetType,  
                                       "target_state" : "In preparazione" , 
                                       "cf_1225":"NA",
                                       "cf_1226":cf_1226, 
                                       "cf_1006":targetKey, 
                                       "cf_1545":targetKey, 
                                       "cf_1546":refId}
                        ret = self.createVtiger("Targets", targetDict)
                        if ret["success"]:
                            result = ret['result'] 
                            self.dictTargets[targetKey] = result
                            print(  "Creato TARGET {0} {1} in VTE con cf_1545 = {2}".format(result["id"], result["targetname"], targetKey ))
                            log.info(  "Creato TARGET {0} {1} in VTE con cf_1545 = {2}".format(result["id"], result["targetname"], targetKey ))
                            if retDict["type_event"] == "new_course":
                                setMessageLogStatus(self.host,self.port,self.user,self.password,self.database,retDict["idmessage_log"],3)
                        else:
                            print( "ERRORE: Errore in creazione {0} {1} [{2}] ".format( sQueryTargets,retDict["idmessage_log"], ret) )
                            log.error( "ERRORE: Errore in creazione {0} {1} [{2}] ".format( sQueryTargets,retDict["idmessage_log"], ret) )
                            if retDict["type_event"] == "new_course":
                                setMessageLogStatus(self.host,self.port,self.user,self.password,self.database,retDict["idmessage_log"],-3)
                else:
                    print( "ERRORE: Errore in ricerca {0} {1} [{2}] ".format( sQueryTargets,retDict["idmessage_log"], ret) )
                    log.error( "ERRORE: Errore in ricerca {0} {1} [{2}] ".format( sQueryTargets,retDict["idmessage_log"], ret) )
                    if retDict["type_event"] == "new_course":
                        setMessageLogStatus(self.host,self.port,self.user,self.password,self.database,retDict["idmessage_log"],-1)
        return targetKey, result

def getMessageLog(host,port, user,password, database):
    cnx = MySQLdb.connect(user=user, passwd=password,port=int(port),
                                  host=host,
                                  db=database)
    cursor = cnx.cursor()
    query = """SELECT message_log.idmessage_log,
                      message_log.timestamp, 
                      event_types.idevent_types ,
                      message_log.type_event, 
                      email.idemail,
                      message_log.by_email, 
                      email.import_status
                      FROM message_log 
                      LEFT JOIN event_types ON event_types.event_type_code = message_log.type_event 
                      LEFT JOIN email ON email.email_address = message_log.by_email 
                      WHERE message_log.import_status = 0
                      ORDER BY message_log.when_timestamp"""
    cursor.execute(query)    
    mvt = MyVtiger()
    # elementListDict = {}
    for row in cursor:
        type_event = row[3] 
        retDict, eventTypeCode = getMessage(host,port, user,password, database,row[0])
        print( "###### message_log id = {0} by {1} type {2} at {3}".format(row[0],row[5],row[3],row[1]))
        log.info( "###### message_log id = {0} by {1} type {2} at {3}".format(row[0],row[5],row[3],row[1]))
        retDict["idmessage_log"] = row[0]
        retDict["email"] = row[5]
        retDict["timestamp"] = row[1]
        retDict["type_event"] = type_event  
        targetKey, retTargetVal = mvt.searchTarget(retDict)
        retDict["targetKey"] = targetKey
        retEntityList = []
        if type_event != 'new_course':
            retEntityList = mvt.processEmail(retDict)
        """
        $relentity["crmid"];
        $relentity["module"];
        $relentity["relcrmid"];
        $relentity["relmodule"];
        """
        bNewLead = False
        iNum = 0
        for entityItem in retEntityList:
            retEvent = mvt.addEventToEntity(retDict, entityItem[1],entityItem[0]  )
            bNewLead = entityItem[2]
            # elementListDict[iNum] = {"crmid":retTargetVal["id"],"relcrmid":entityItem[1]["id"]}
            iNum += 1
        if type_event == 'registration':
            pass
        if type_event == 'new_course':
            pass
        if type_event == 'download':
            pass
        if type_event == 'consulting':
            # Consulenza
            pass
            """
            if entityItem[0] == "Accounts" or (entityItem[0] == "Contacts" and "account_id" in entityItem[1]):
                contactId = 0
                entId = entityItem[1]["id"]
                if entityItem[0] == "Contacts":
                    contactId = entId
                    entId = entityItem[1]["account_id"]
                consultingDict = {"assigned_user_id":entityItem[1]["assigned_user_id"],"consulenzaname":22, "parent_display":entId, "contact":contactId, "consulenzastatus":"Open", "description":retDict["description"]}
                if "file" in retDict:
                    consultingDict["description"] = "{0}\n[{1}]".format(consultingDict["description"], retDict["file"])
                retCons = mvt.createVtiger("Consulenza", consultingDict)
                if retCons["success"]:
                    result = retCons['result']
                    setMessageLogStatus(mvt.host,mvt.port,mvt.user,mvt.password,mvt.database,retDict["idmessage_log"],5)
                else:
                    print( "ERRORE: Errore in creazione Consulenza per message_log con id {2} -  Consulenza element = {0} - [{1}] ".format( consultingDict, retCons, retDict["idmessage_log"]) ) 
                    log.error( "ERRORE: Errore in creazione Consulenza per message_log con id {2} -  Consulenza element = {0} - [{1}] ".format( consultingDict, retCons, retDict["idmessage_log"]) ) 
                    setMessageLogStatus(mvt.host,mvt.port,mvt.user,mvt.password,mvt.database,retDict["idmessage_log"],-5)           
           """
        if type_event == 'course_subscribe':
            regDict, reg_idmessage_log, timestamp, eventTypeCode = getLastEventByType(mvt.host,mvt.port,mvt.user,mvt.password,mvt.database,"registration",retDict["email"])
            elementDict = {"assigned_user_id":"19x1705","leadstatus":"Not Contacted", "leadsource":"website_{0}".format(retDict["type_event"]), "cf_744":"{0}".format(retDict["idmessage_log"])}     
            keyMap = keyLeadMapping[eventTypeCode]
            for key in regDict:
                if key in keyMap:
                    elementDict[keyMap[key]] = regDict[key]
            keyMap = keyLeadMapping[retDict["type_event"]]     
            for key in retDict:
                if key in keyMap:
                    elementDict[keyMap[key]] = retDict[key]
            courseDict = getCourseById(mvt.host,mvt.port, mvt.user,mvt.password, mvt.database,retDict["course_id"])
            courseName = "Senza Nome"
            if "name" in courseDict:
                courseName = courseDict["name"]
            elementDict["cf_726"] = "{0} ({1})".format( courseName, courseDict["language"])
            elementDict["cf_733"] = "{0}-{1}".format(courseDict["begins_at"], courseDict["ends_at"])
            elementDict["cf_756"] = courseDict["id"]            
            retLead = mvt.createVtiger("Leads", elementDict)
            if retLead["success"]:
                result = retLead['result']
            else:
                print( "ERRORE: Errore in creazione Lead per message_log con id {2} -  Lead element = {0} - [{1}] ".format( elementDict, retLead, retDict["idmessage_log"]) )
                log.error( "ERRORE: Errore in creazione Lead per message_log con id {2} -  Lead element = {0} - [{1}] ".format( elementDict, retLead, retDict["idmessage_log"]) )
    cursor.close()
    cnx.close()
    retLinks = mvt.createLinks({"name":"value"})
    if not retLinks["success"]:
        print( "ERRORE: Errore in creazione link Target vs Entityies  [{0}] ".format( retLinks) )     
        log.error( "ERRORE: Errore in creazione link Target vs Entityies  [{0}] ".format( retLinks) )         
    return True


print("setup....")   
    
def hyper_task():
    print("starting loop....")
    getMessageLog(sHost,sPort,sUser,sPass,sDB)
    print("loop terminated")

# hyper_task()

from twisted.internet.task import LoopingCall
from twisted.internet import reactor
    

lc = LoopingCall(hyper_task)
lc.start(60*5)
reactor.run()
