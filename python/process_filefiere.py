# -*- coding: utf-8 -*-
# danzi.tn@20170117 gestione Consulenze e link Target
import logging
import logging.handlers
import os, pickle, datetime
import sys
import getopt
import ConfigParser
from vtiger import VtigerCli
import pandas as pd

log = logging.getLogger()
log.setLevel(logging.DEBUG)
file_handler = logging.handlers.RotatingFileHandler("{0}.log".format(os.path.basename(__file__).split(".")[0]), maxBytes=5000000,backupCount=5)
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
file_handler.setFormatter(formatter)
log.addHandler(file_handler)

sCFGName = "{0}.cfg".format(os.path.basename(__file__).split(".")[0])

allowedModules =['Accounts','Leads','Contacts']




def main(argv):
    syntax = "python " + os.path.basename(__file__) + " -h -c -f <file path>"   
    bUseConfig = False
    xlsFile = None
    wb = None
    try:
        opts = getopt.getopt(argv, "hcf:", ["help","config","file="])[0]
    except getopt.GetoptError:
        print syntax
        sys.exit(1)
    
    # parse args
    for opt, arg in opts:
        if opt == '-h':
            print syntax
            sys.exit()
        elif opt in ("-c", "--config"):
            bUseConfig = True    
        elif opt in ("-f", "--file"):
            xlsFile = arg
            if not os.path.exists(xlsFile):
                print "{0} does not exists".format(xlsFile)
                log.error("{0} does not exists".format(xlsFile))
                sys.exit(2)
            else:
                xl = pd.ExcelFile(xlsFile)
    # only config
    if bUseConfig:
        if os.path.exists(sCFGName):    
            syncConfig = ConfigParser.RawConfigParser()
            cfgItems = syncConfig.read(sCFGName)
            accessKey = syncConfig.get("vte","accesskey")
            vtigerserver = syncConfig.get("vte","url")        
            username = syncConfig.get("vte","username")
            vtc = VtigerCli(vtigerserver,username,accessKey)            
            targetDict = {}
            for sn in xl.sheet_names:
                if sn in allowedModules:
                    print "{1} has valid sheet {0} ".format(sn,xlsFile)
                    log.info("{1} has valid sheet {0} ".format(sn,xlsFile))
                    df = xl.parse(sn)
                    for row_index, row in df.iterrows():
                        sTargetName = row["targetname"]
                        print('%s => %s' % (row_index, row["account_no"]))
                        if sTargetName not in targetDict:
                            sQueryTargets = "SELECT * FROM Targets WHERE targetname = '{0}';".format(sTargetName)
                            ret = vtc.queryVtiger(sQueryTargets)
                            if ret['success']:
                                bTargetFound = False
                                for item in ret['result']:
                                    bTargetFound = True
                                    print( "Trovato Targets con id = {0}".format(item["id"] ))
                                    log.info( "Trovato Targets con id = {0}".format(item["id"] ))
                                    targetDict[sTargetName] = item
                                if not bTargetFound:
                                    newItem = {"targetname":sTargetName,  
                                       "assigned_user_id":"19x9",   
                                       "target_type" : "Form Fiere",  
                                       "target_state" : "In preparazione" , 
                                       "cf_1545":sTargetName}
                                    newItem["targetname"] = sTargetName
                                    newItem["cf_1545"] = sTargetName
                                    newItem["target_type"] = "Form Fiere"
                                    retTarget = vtc.createVtiger("Targets", newItem)
                                    if retTarget["success"]:
                                        targetItem = retTarget['result'] 
                                        targetDict[sTargetName] = targetItem
                                        print(  "Creato TARGET {0} in VTE ".format(targetItem["id"] ))
                                        log.info(  "Creato TARGET {0} in VTE ".format(targetItem["id"] ))
                                    else:
                                        print( "ERRORE: Errore in creazione {0} [{1}] ".format( sQueryTargets, retTarget) )
                                        log.error( "ERRORE: Errore in creazione {0} [{1}] ".format( sQueryTargets, retTarget) )                      
                            else:
                                print( "ERRORE: Errore in ricerca Targets {0} [{1}] ".format( sQueryTargets, ret))
                                log.error( "ERRORE: Errore in ricerca Targets {0} [{1}] ".format( sQueryTargets, ret))
                        else:
                            print( "TARGET {0} trattato ".format(sTargetName))
                            log.info( "TARGET {0} trattato  ".format(sTargetName))
                        if sn == 'Accounts':    
                            sQueryAccounts = "SELECT * FROM {0} WHERE account_no = '{1}';".format(sn,row["account_no"])
                            ret = vtc.queryVtiger(sQueryAccounts)
                            if ret['success']:
                                for item in ret['result']:
                                    print( "Trovato Accounts con account_no = {0} e id = {1}".format(row["account_no"],item["id"] ))
                                    log.info( "Trovato Accounts con account_no = {0} e id = {1}".format(row["account_no"],item["id"] ))
                                    sDate = datetime.datetime.now().strftime('%Y-%m-%d')
                                    eventDict = { 
                                        "assigned_user_id":item["assigned_user_id"], 
                                        "parent_id":item["id"],
                                        "activitytype":"Contatto - Fiera", 
                                        "subject":"Contatto in fiera {0}".format(sTargetName),
                                        "date_start":sDate,
                                        "time_start":"00:00",
                                        "due_date":sDate,
                                        "time_end":"23:59",
                                        "is_all_day_event":1,
                                        "eventstatus":"Held",
                                        "description":"{0}".format(row["description"]),
                                        "cf_1547": sTargetName
                                    }
                                    eventDict["subject"] = "Contattato in fiera {0}".format(sTargetName)
                                    retEvent = vtc.createVtiger("Events", eventDict)
                                    if retEvent["success"]:
                                        print "OK evento ".format(retEvent["result"])
                                    else:
                                        print( "ERRORE: Error on create event {0}".format(retEvent) )
                                        log.error( "ERRORE: Error on create event {0}".format(retEvent) )
                            else:
                                print( "ERRORE: Errore in ricerca Accounts {0} [{1}] ".format( sQueryAccounts, ret))
                                log.error( "ERRORE: Errore in ricerca Accounts {0} [{1}] ".format( sQueryAccounts, ret))
                    vtc.createLinks({"name":"value"})
                else:
                    log.error("{0} is not an entity".format(sn))
        else:
            errMsg = "Error: config file {0} does not exists!".format(sCFGName)
            log.error(errMsg)
            print errMsg
            sys.exit()

if __name__ == "__main__":
    main(sys.argv[1:])