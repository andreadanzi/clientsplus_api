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
# cf_1472 Message Log ID
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
                                    "tel":"phone",
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

sHost = '127.0.0.1'
sPort = '3386'
sUser = 'root'
sPass = 'root'
sDB = 'clientsplus'


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

    emails = collections.defaultdict(list)
    not_found_emails = collections.defaultdict(list)
    found = collections.defaultdict(list)
    courses = collections.defaultdict(list)
    courses_list = []
    for row in cursor:
        if row[3] == 'new_course':
            courses_list.append(SiteMessage(*row))
        else:
            emails[row[5]].append(SiteMessage(*row))
            not_found_emails[row[5]].append(SiteMessage(*row))
    cursor.close()
    cnx.close()
    for course_msg in courses_list:
        retDict, eventTypeCode = getMessage(host,port, user,password, database,course_msg.idmessage_log)
        retDict["idmessage_log"] = course_msg.idmessage_log
        retDict["timestamp"] = course_msg.timestamp
        retDict["type_event"] = course_msg.type_event
        courses[retDict["id"]].append(retDict)
    return emails, not_found_emails, found, courses



emails, not_found_emails, found , new_courses = getMessageLog(sHost,sPort,sUser,sPass,sDB)


    
# Vtiger Parameters
accessKey = 'BLmHQc0IvDXC665o'
vtigerserver = 'https://crmtest.rothoblaas.com/vte'
url = '%s/webservice.php' % vtigerserver
username = 'webweb'

gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)

### let's set up the session
# get the token using 'getchallenge' operation
values = {'operation':'getchallenge','username': username }
data = urllib.urlencode(values)
req = urllib2.Request('%s?%s' % (url,data))

response = urllib2.urlopen(req,context=gcontext).read()
token = json.loads(response)['result']['token']

# use the token to + accesskey to create the tokenized accessKey
key = md5(token + accessKey)
tokenizedAccessKey = key.hexdigest()
values['accessKey'] = tokenizedAccessKey

# now that we have an accessKey tokenized, let's perform a login operation 
values['operation']  = 'login'
data = urllib.urlencode(values)
req = urllib2.Request(url, data)
response = urllib2.urlopen(req,context=gcontext)
response = json.loads(response.read())
print "######## login"
if not response["success"]:
    print "login failed"
    exit(1)

userId = response["result"]["userId"]
# set the sessionName
sessionName = response['result']['sessionName']

"""
values['sessionName'] = sessionName
### now let's do stuff
# listtypes
values['operation'] = 'listtypes'
data = urllib.urlencode(values)
# added data a parameter here makes this a POST
req = urllib2.Request(url,data)
response = urllib2.urlopen(req)
print 'here are the available types'
print json.loads(response.read())

# find out about a particular vTiger Object Type
# we'll look at 'Contacts'
values['operation'] = 'describe'
values['elementType'] = 'Events'
data = urllib.urlencode(values)
# must be a get according to docs
# so we append data to url
req = urllib2.Request("%s?%s" % (url,data))
response = urllib2.urlopen(req)
print '########################'
print 'about Events'
print values
print json.loads(response.read())

exit()
"""


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

# TARGET COURSES
if len(new_courses) > 0:    
    sQueryTargets = "SELECT * FROM Targets WHERE cf_1470 IN ('{0}');".format("','".join(new_courses.keys()))
    print sQueryTargets
    resp = queryVtiger(url,gcontext,sessionName,sQueryTargets)
    if resp['success']:
        for item in resp['result']:
            # print "trovato TARGET {0}".format(item)
            for courseDict in new_courses[item["cf_1470"]]:
                item["targetname"] = "Corso WEB: {0} ({1})".format(courseDict["name"], courseDict["id"])
                item["cf_1226"] = courseDict["begins_at"]
                item["cf_1468"] = courseDict["ends_at"]
                item["cf_1469"] = courseDict["language"]
                item["cf_1471"] = courseDict["name"]
                item["cf_1225"] = "NA"
                item["cf_1472"] = "{0}_{1}".format(courseDict["type_event"],courseDict["idmessage_log"])
                ret = updateVtiger(url,gcontext, sessionName, "Targets", item)
                if ret["success"]:
                    setMessageLogStatus(sHost,sPort,sUser,sPass,sDB,courseDict["idmessage_log"],1)
                else:
                    setMessageLogStatus(sHost,sPort,sUser,sPass,sDB,courseDict["idmessage_log"],-1)
            new_courses.pop(item["cf_1470"],None)
    for key_c in new_courses:
        course_list = new_courses[key_c]
        for courseDict in course_list:
            # TODO aggiugegere codice fatturazione
            elementDict = {"targetname":"Corso WEB: {0} ({1})".format(courseDict["name"], courseDict["id"]),  
                           "assigned_user_id":"19x1705",   
                           "target_type" : "Iscrizione Corso",  
                           "target_state" : "Pronto" , 
                           "cf_1225":"NA",
                           "cf_1470":courseDict["id"], 
                           "cf_1226":courseDict["begins_at"],  
                           "cf_1468":courseDict["ends_at"],
                           "cf_1469":courseDict["language"],
                           "cf_1471":courseDict["name"],
                           "cf_1472":"{0}_{1}".format(courseDict["type_event"],courseDict["idmessage_log"])  }
            ret = createVtiger(url,gcontext, sessionName, "Targets", elementDict)
            if ret["success"]:
                # print "OK Target per corso creato {0}".format(ret["result"])
                setMessageLogStatus(sHost,sPort,sUser,sPass,sDB,courseDict["idmessage_log"],2)
            else:
                # print "errore nella creazione del Target per corsi {0}  - {1}".format(elementDict , ret)
                setMessageLogStatus(sHost,sPort,sUser,sPass,sDB,courseDict["idmessage_log"],-2)


if len(emails) == 0:
    exit(0)

sQueryLeads = "SELECT * FROM Leads WHERE email IN ('{0}');".format("','".join(emails.keys()))
sQueryAccounts = "SELECT * FROM Accounts WHERE email1 IN ('{0}');".format("','".join(emails.keys()))
sQueryContacts = "SELECT * FROM Contacts WHERE email IN ('{0}');".format("','".join(emails.keys()))

# LEADS
resp = queryVtiger(url,gcontext,sessionName,sQueryLeads)
# print "#################### LEADS"
if resp['success']:
    for item in resp['result']:
        # print "id {0}. Last Name {1}, First Name {2} and newsletter_permission = {3}".format(item["id"],item["lastname"],item["firstname"],item["newsletter_permission"])
        for message in emails[item["email"]]:
            dictMsg = message._asdict()
            dictMsg["id"] = item["id"]
            dictMsg["company"] = item["company"]
            dictMsg["newsletter_permission"] = item["newsletter_permission"]
            dictMsg["lastname"] = item["lastname"]
            dictMsg["firstname"] = item["firstname"]
            dictMsg["assigned_user_id"] = item["assigned_user_id"]
            found["Leads"].append(dictMsg)
        not_found_emails.pop(item["email"],None)

# ACCOUNTS
resp = queryVtiger(url,gcontext,sessionName,sQueryAccounts)
# print "#################### ACCOUNTS"
if resp['success']:
    for item in resp['result']:
        # print "id {0}. Account Name {1}, Semiramis Code {2} and newsletter_permission = {3}".format(item["id"],item["accountname"],item["external_code"],item["newsletter_permission"])
        for message in emails[item["email1"]]:
            dictMsg = message._asdict()
            dictMsg["id"] = item["id"]
            dictMsg["accountname"] = item["accountname"]
            dictMsg["newsletter_permission"] = item["newsletter_permission"]
            dictMsg["external_code"] = item["external_code"]
            dictMsg["assigned_user_id"] = item["assigned_user_id"]
            found["Accounts"].append(dictMsg)
        not_found_emails.pop(item["email1"],None)


# CONTACTS
resp = queryVtiger(url,gcontext,sessionName,sQueryContacts)
# print "#################### CONTACTS"
if resp['success']:
    for item in resp['result']:
        # print "id {0}. Last Namee {1}, First Name {2}, Account ID = {4} and newsletter_permission = {3}".format(item["id"],item["lastname"],item["firstname"],item["newsletter_permission"], item["account_id"]) 
        for message in emails[item["email"]]:
            dictMsg = message._asdict()
            dictMsg["id"] = item["id"]
            dictMsg["account_id"] = item["account_id"]
            dictMsg["newsletter_permission"] = item["newsletter_permission"]
            dictMsg["lastname"] = item["lastname"]
            dictMsg["firstname"] = item["firstname"]
            dictMsg["assigned_user_id"] = item["assigned_user_id"]
            found["Contacts"].append(dictMsg)     
        not_found_emails.pop(item["email"],None)  

created = {}
for email in not_found_emails:
    sId = ""
    leadDict = None
    # print "{0} not found".format(email)
    for message in not_found_emails[email]: 
        
        # print "\t\tid {0}, type {1} at {2}".format(message.idmessage_log, message.type_event, message.timestamp)
        retDict, keyType = getMessage(sHost,sPort,sUser,sPass,sDB,message.idmessage_log)
        dictMsg = message._asdict()
        #elementDict={"email":"pippo@pippo.com", "lastname":"bello", "firstname":"pippo", "newsletter_permission":1, "company":"example", "assigned_user_id":userId}
        if message.type_event in keyLeadMapping:
            keyMap = keyLeadMapping[message.type_event]
            if email in created:
                sId = created[email]
                # per gestione corsi un lead nuovo
                if message.type_event == 'course_subscribe':
                    leadDict["assigned_user_id"] = "19x1705"
                    leadDict["leadsource"] = "website_{0}".format(message.type_event)
                    leadDict["cf_744"] =  "{0}_{1}".format(message.type_event, message.idmessage_log)
                    if leadDict:
                        for key in retDict:
                            if key in keyMap:
                                leadDict[keyMap[key]] = retDict[key]
                        ret = createVtiger(url,gcontext, sessionName, "Leads", leadDict)
                        if ret["success"]:
                            print "OK Lead per corso creato {0}".format(ret["success"]["id"])
                        else:
                            print "errore nella creazione del Lead per corsi {0}  - {1}".format(retDict , ret)
                    else:
                        print "Errore.....iscizione al corso senza registrazione"
            else:
                if message.type_event == 'new_course':
                    pass
                else:
                    elementDict = {"assigned_user_id":userId, "leadsource":"website_{0}".format(message.type_event), "cf_744":"{0}_{1}".format(message.type_event, message.idmessage_log)}
                    for key in dictMsg:
                        if key in keyMap:
                            elementDict[keyMap[key]] = dictMsg[key]
                    for key in retDict:
                        if key in keyMap:
                            elementDict[keyMap[key]] = retDict[key]
                    ret = createVtiger(url,gcontext, sessionName, "Leads", elementDict)
                    print ret               
                    if ret["success"]:
                        sId = ret["result"]["id"]
                        leadDict = ret["result"]
                        created[email] = sId               
                        """
                        dictMsg["id"] = sId
                        dictMsg["company"] = ret["result"]["company"]
                        dictMsg["newsletter_permission"] = ret["result"]["newsletter_permission"]
                        dictMsg["lastname"] = ret["result"]["lastname"]
                        dictMsg["firstname"] = ret["result"]["firstname"]
                        found["Leads"].append(dictMsg)
                        """                    
                        setMessageLogStatus(sHost,sPort,sUser,sPass,sDB,message.idmessage_log,1)
                        bInsertedLead = True
                    else:
                        setMessageLogStatus(sHost,sPort,sUser,sPass,sDB,message.idmessage_log,-1)
            if len(sId) > 0:
                duedate = message.timestamp + datetime.timedelta(hours=1)   
                eventDict = { 
                                "assigned_user_id":userId, 
                                "parent_id" : sId,
                                "activitytype":"website_{0}".format(message.type_event), 
                                "subject":keySubjects[message.type_event].format(email),
                                "date_start":message.timestamp.strftime('%d-%m-%Y'),
                                "time_start":message.timestamp.strftime('%H:%M'),
                                "due_date":duedate.strftime('%d-%m-%Y'),
                                "time_end":duedate.strftime('%H:%M'),
                                "eventstatus":"Held",
                                "description":json.dumps(retDict),
                                "cf_1467": "{0}_{1}".format(message.type_event, message.idmessage_log)
                                }
                ret = createVtiger(url,gcontext, sessionName, "Events", eventDict)
                if ret["success"]:
                    sEventId = ret["result"]["id"]
                    setMessageLogStatus(sHost,sPort,sUser,sPass,sDB,message.idmessage_log,2)
                else:
                    print "\t\t\t" , ret
                    setMessageLogStatus(sHost,sPort,sUser,sPass,sDB,message.idmessage_log,-2)
    
for keyModule in found:
    for dictMsg in found[keyModule]:
        idmessage_log = dictMsg["idmessage_log"]        
        sId = dictMsg["id"]
        if len(sId) > 0:
            retMsgDict, keyType = getMessage(sHost,sPort,sUser,sPass,sDB,idmessage_log)
            # IF COURSE CREATE A NEW LEAD
            if dictMsg["type_event"] == 'course_subscribe':
                retDict, reg_idmessage_log, timestamp, eventTypeCode = getLastEventByType(sHost,sPort,sUser,sPass,sDB,"registration",dictMsg["email"])
                # MAP FIRST REGISTRATION DATA
                keyMap = keyLeadMapping[eventTypeCode]
                elementDict = {"assigned_user_id":dictMsg["assigned_user_id"], "leadsource":"website_{0}".format(dictMsg["type_event"])}
                for key in dictMsg:
                    if key in keyMap:
                        elementDict[keyMap[key]] = dictMsg[key]
                for key in retDict:
                    if key in keyMap:
                        elementDict[keyMap[key]] = retDict[key]
                # MAP COURSE FIELDS
                keyMap = keyLeadMapping[dictMsg["type_event"]]
                for key in retMsgDict:
                    if key in keyMap:
                        elementDict[keyMap[key]] = retMsgDict[key]
                ret = createVtiger(url,gcontext, sessionName, "Leads", elementDict)
                if ret["success"]:            
                    setMessageLogStatus(sHost,sPort,sUser,sPass,sDB,idmessage_log,1)
                else:
                    setMessageLogStatus(sHost,sPort,sUser,sPass,sDB,idmessage_log,-1)                        
            print "Processing event for {0} id {1} ({2})".format(keyModule,sId, idmessage_log)
            duedate = dictMsg["timestamp"] + datetime.timedelta(hours=1)
            eventDict = { 
                            "assigned_user_id":dictMsg["assigned_user_id"], 
                            "parent_id" : sId,
                            "activitytype":"website_{0}".format(dictMsg["type_event"]), 
                            "subject":keySubjects[dictMsg["type_event"]].format(dictMsg["email"]),
                            "date_start":dictMsg["timestamp"].strftime('%d-%m-%Y'),
                            "time_start":dictMsg["timestamp"].strftime('%H:%M'),
                            "due_date":duedate.strftime('%d-%m-%Y'),
                            "time_end":duedate.strftime('%H:%M'),
                            "eventstatus":"Held",
                            "description":json.dumps(retMsgDict),
                            "cf_1467": "{0}_{1}".format(dictMsg["type_event"], idmessage_log)
                            }
            ret = createVtiger(url,gcontext, sessionName, "Events", eventDict)            
            if ret["success"]:
                sEventId = ret["result"]["id"]
                setMessageLogStatus(sHost,sPort,sUser,sPass,sDB,idmessage_log,2)
            else:
                print "\t\t\t" , ret
                setMessageLogStatus(sHost,sPort,sUser,sPass,sDB,idmessage_log,-2)
        