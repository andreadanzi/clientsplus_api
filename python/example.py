# -*- coding: utf-8 -*-
import mysql.connector
import urllib2,ssl
import json
import urllib
import collections
import datetime
from hashlib import md5

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
    cnx = mysql.connector.connect(user=user, password=password,port=port,
                                  host=host,
                                  database=database)
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
    cnx = mysql.connector.connect(user=user, password=password,port=port,
                                  host=host,
                                  database=database)
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
    cnx = mysql.connector.connect(user=user, password=password,port=port,
                                  host=host,
                                  database=database)
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
    cnx = mysql.connector.connect(user=user, password=password,port=port,
                                  host=host,
                                  database=database)
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
        print "######## login"
        if not response["success"]:
            print "login failed"
            exit(1)
        
        self.userId = response["result"]["userId"]
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
    
    
    def addEventToEntity(self,retDict, entityItem ):
        result = None
        duedate = retDict["timestamp"] + datetime.timedelta(hours=1)
        sDescr = ""
        if "description" in retDict:
            sDescr = retDict["description"]
        eventDict = { 
                        "assigned_user_id":entityItem["assigned_user_id"], 
                        "parent_id" : entityItem["id"],
                        "activitytype":"website_{0}".format(retDict["type_event"]), 
                        "subject":keySubjects[retDict["type_event"]].format(retDict["email"]),
                        "date_start":retDict["timestamp"].strftime('%d-%m-%Y'),
                        "time_start":retDict["timestamp"].strftime('%H:%M'),
                        "due_date":duedate.strftime('%d-%m-%Y'),
                        "time_end":duedate.strftime('%H:%M'),
                        "eventstatus":"Held",
                        "description":sDescr,
                        "cf_1547": "{0}_{1}".format(retDict["type_event"], retDict["idmessage_log"])
                        }
        if retDict["type_event"] == "consulting":
            eventDict["subject"] = "{0} ({1})".format(eventDict["subject"],retDict["category"])
        if retDict["type_event"] == "course_subscribe":
            eventDict["subject"] = "{0} ({1})".format(eventDict["subject"],retDict["course_id"])
        if retDict["type_event"] == "new_course":
            eventDict["subject"] = "{0} {1} ({2})".format(eventDict["subject"],retDict["name"],retDict["id"])
        ret = self.createVtiger("Events", eventDict)            
        if ret["success"]:
            setMessageLogStatus(self.host,self.port,self.user,self.password,self.database,retDict["idmessage_log"],3)
            result = ret["result"]
        else:
            setMessageLogStatus(self.host,self.port,self.user,self.password,self.database,retDict["idmessage_log"],-5)
        return result
    
    def processEmail(self,retDict):
        result = None
        entityKey = None
        entityKey = retDict["email"]
        if entityKey in self.dictEntities:
            result = self.dictEntities[entityKey]
        else:
            # Search Leads
            sQueryLeads = "SELECT * FROM Leads WHERE leadsource != 'website_course_subscribe' AND email  = '{0}';".format(entityKey)
            ret = self.queryVtiger(sQueryLeads)
            if ret['success']:
                for item in ret['result']:
                    self.dictEntities[entityKey].append(('Leads',item, False))
                    print "Trovato Leads con entityKey = {0} e id = {1}".format(entityKey,item["id"] )
            else:
                print "Errore in ricerca Leads {0} [{1}] ".format( sQueryLeads, ret)
                setMessageLogStatus(self.host,self.port,self.user,self.password,self.database,retDict["idmessage_log"],-1)
            
            # Search Accounts
            sQueryAccounts = "SELECT * FROM Accounts WHERE email1 = '{0}';".format(entityKey)
            ret = self.queryVtiger(sQueryAccounts)
            if ret['success']:
                for item in ret['result']:
                    self.dictEntities[entityKey].append(('Accounts',item, False))
                    print "Trovato Accounts con entityKey = {0} e id = {1}".format(entityKey,item["id"] )
            else:
                print "Errore in ricerca Accounts {0} [{1}] ".format( sQueryAccounts, ret)
                setMessageLogStatus(self.host,self.port,self.user,self.password,self.database,retDict["idmessage_log"],-2)
            
            # Search Contacts
            sQueryContacts = "SELECT * FROM Contacts WHERE email = '{0}';".format(entityKey)
            ret = self.queryVtiger(sQueryContacts)
            if ret['success']:
                for item in ret['result']:
                    self.dictEntities[entityKey].append(('Contacts',item, False))
                    print "Trovato Contacts con entityKey = {0} e id = {1}".format(entityKey,item["id"] )
            else:
                print "Errore in ricerca Contacts {0} [{1}] ".format( sQueryContacts, ret)
                setMessageLogStatus(self.host,self.port,self.user,self.password,self.database,retDict["idmessage_log"],-3)
            
            if entityKey in self.dictEntities:
                setMessageLogStatus(self.host,self.port,self.user,self.password,self.database,retDict["idmessage_log"],1)
            else:
                elementDict = {"assigned_user_id":self.userId,"leadstatus":"Not Contacted", "leadsource":"website_{0}".format(retDict["type_event"]), "cf_744":"{0}".format(retDict["idmessage_log"])}                
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
                    print "Aggiunto nuovo Lead con entityKey = {0} e id = {1}".format(entityKey,ret["result"]["id"] )
                    setMessageLogStatus(self.host,self.port,self.user,self.password,self.database,retDict["idmessage_log"],2)
                else:
                    setMessageLogStatus(self.host,self.port,self.user,self.password,self.database,retDict["idmessage_log"],-4)
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
            targetname = "Corso WEB: {0} ({1})".format(retDict["name"], retDict["id"])
            assignedUserId = "19x1705"
            targetType = "Iscrizione Corso"
            cf_1470 = retDict["id"]
            cf_1226 = retDict["begins_at"]
            cf_1468 = retDict["ends_at"]
            cf_1469 = retDict["language"]
            cf_1471 = retDict["name"]
        elif retDict["type_event"] == "download":
            targetKey =  "{0}_{1}".format(retDict["type_event"],retDict["description"])
            targetType = "Download"
            targetname = "Download WEB: {0} {1}".format(retDict["type_event"],retDict["description"])
        elif retDict["type_event"] == "consulting":
            targetKey =  "{0}_{1}".format(retDict["type_event"],retDict["category"])
            targetType = "Richiesta Consulenze (Form)"
            targetname = "Consulenza WEB: {0}".format(retDict["category"])
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
            targetKey =  "new_course_{0}".format(retDict["course_id"])
            courseDict = getCourseById(self.host,self.port, self.user,self.password, self.database,retDict["course_id"])
            targetname = "Corso WEB: {0} ({1})".format(courseDict["name"], courseDict["id"])
            assignedUserId = "19x1705"
            targetType = "Iscrizione Corso"
            cf_1470 = courseDict["id"]
            cf_1226 = courseDict["begins_at"]
            cf_1468 = courseDict["ends_at"]
            cf_1469 = courseDict["language"]
            cf_1471 = courseDict["name"]
        if targetKey:
            if targetKey in self.dictTargets: 
                result = self.dictTargets[targetKey]
                print "trovato TARGET {0} {1} nella cache con key = {2}".format(result["id"], result["targetname"], targetKey )
            else:
                sQueryTargets = "SELECT * FROM Targets WHERE cf_1545 = '{0}';".format(targetKey)
                ret = self.queryVtiger(sQueryTargets)
                if ret['success']:
                    for item in ret['result']:
                        result = item
                    if( result ):
                        self.dictTargets[targetKey] = result
                        print "trovato TARGET {0} {1} in VTE con cf_1545 = {2}".format(result["id"], result["targetname"], targetKey )
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
                        else:
                            print "Errore in creazione {0} [{1}] ".format( targetDict, ret)
                else:
                    print "Errore in ricerca {0} [{1}] ".format( sQueryTargets, ret)
        return result

def getMessageLog(host,port, user,password, database):
    cnx = mysql.connector.connect(user=user, password=password,port=port,
                                  host=host,
                                  database=database)
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
    for row in cursor:
        type_event = row[3] 
        retDict, eventTypeCode = getMessage(host,port, user,password, database,row[0])
        print "message_log id = {0}".format(row[0])
        retDict["idmessage_log"] = row[0]
        retDict["email"] = row[5]
        retDict["timestamp"] = row[1]
        retDict["type_event"] = type_event  
        retTargetVal = mvt.searchTarget(retDict) 
        retEntityList = mvt.processEmail(retDict)
        bNewLead = False
        for entityItem in retEntityList:
            retEvent = mvt.addEventToEntity(retDict, entityItem[1] )
            bNewLead = entityItem[2]
        if type_event == 'registration':
            pass
        if type_event == 'new_course':
            pass
        if type_event == 'download':
            pass
        if type_event == 'consulting':
            pass
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
            elementDict["cf_726"] = "{0} ({1})".format(courseDict["name"] , courseDict["language"])
            elementDict["cf_733"] = "{0}-{1}".format(courseDict["begins_at"], courseDict["ends_at"])
            elementDict["cf_756"] = courseDict["id"]            
            retLead = mvt.createVtiger("Leads", elementDict)
            if retLead["success"]:
                result = retLead['result']
            else:
                print "Errore in creazione Lead {0} [{1}] ".format( elementDict, retLead)
    cursor.close()
    cnx.close()
    return True

getMessageLog(sHost,sPort,sUser,sPass,sDB)