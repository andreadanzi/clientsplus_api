#!/bin/bash
#
# Tutte le request devono avere il parametro token=AetheiNae0waiy0aeB1angooy5Foh3Th, nel caso si può mettere anche il token nell'header X-Auth-Token (vedi ultimo esempio)
# Se token è sbagliato lancia InvalidArgumentException('Wrong Auth Token');
# 
# API Disponibli
#
#   /try        api GET per testare la connessione, restituisce retcode = 0 se OK - {"retcode":"0","message":"Your test succedeed!"}
#   
#   /message    api POST per inviare messaggi: parametri obbilgatori sono
#                                                                           token:  AetheiNae0waiy0aeB1angooy5Foh3Th
#                                                                           by:     email
#                                                                           whem:   timestemp since the epoch
#                                                                           type:   tipologia di messaggio (es. registration. form_catalogo ,etc)
#                                                                           data:   payload chiave valore con dati aggiuntivi
#
#               return value: lo stesso json inviato con in più "retcode" (0 se tutto OK, > 0 se errore) e "id" con l'identificativo unico (key) del messaggio come inserito nel NS DB
#                                                                      
#               errori: se retcode > 0 allora c'è un campo error contenente codice di errore e messaggio (es. {"by":"info@danzi.tn.com","when":"1481888078","type":"corso","data":{"first_name":"Andrea","last_name":"Danzi","code":"WX012","company":"DANZI.TN","date":"14\/05\/2017"},"retcode":1,"error":{"code":"120","message":"Message Already Exists!"}})
#
#   Il sistema identifica l'univocità di un messaggio dalla terna composta dai parametri (by,when,type)  
#   Quindi se due messaggi hanno questa terna uguale, il primo viene registrato, per il secondo viene restituito errore e non viene registrato il messaggio
#
AUTH_TOKEN=AetheiNae0waiy0aeB1angooy5Foh3Th
CURTIME="$(date +%s)"

# test connection
curl -X GET http://openon.it:8888/try?token=$AUTH_TOKEN
# expected return {"retcode":"0","message":"Your test succedeed!"}
echo
echo "########################################"
echo "registration example"
# registration example
curl -H "Content-Type: application/json" -X POST -d '{"token":"'"$AUTH_TOKEN"'", "by":"andrea.dnz@gmail.com","when":"'"$CURTIME"'","type":"registration","data":{"first_name":"Andrea","last_name":"Danzi","username":"andrea.danzi","company":"DANZI.TN"}}' http://openon.it:8888/message
echo
echo "########################################"
echo "form request example"
# form request example
curl -H "Content-Type: application/json" -X POST -d '{"token":"'"$AUTH_TOKEN"'","by":"andrea@danzi.tn.com","when":"'"$CURTIME"'","type":"form_catalogo","data":{"first_name":"Andrea","last_name":"Danzi","username":"andrea.danzi","company":"DANZI.TN"}}' http://openon.it:8888/message
echo
echo "########################################"
echo "download example"
# download example
curl -H "Content-Type: application/json" -X POST -d '{"token":"'"$AUTH_TOKEN"'","by":"info@danzi.tn.com","when":"'"$CURTIME"'","type":"download","data":{"first_name":"Andrea","last_name":"Danzi","username":"andrea.danzi","company":"DANZI.TN","download":"calcolo_viti.xls"}}' http://openon.it:8888/message
echo
echo "########################################"
echo "course example"
# course example
curl -H "Content-Type: application/json"  -X POST -d '{"token":"'"$AUTH_TOKEN"'","by":"info@danzi.tn.com","when":"'"$CURTIME"'","type":"corso","data":{"first_name":"Andrea","last_name":"Danzi","code":"WX012","company":"DANZI.TN","date":"14/05/2017"}}' http://openon.it:8888/message
echo
echo "########################################"
echo "course example with error"
# course example, same message as previous, error expected!
curl -H "Content-Type: application/json"  -X POST -d '{"token":"'"$AUTH_TOKEN"'","by":"info@danzi.tn.com","when":"'"$CURTIME"'","type":"corso","data":{"first_name":"Andrea","last_name":"Danzi","code":"WX012","company":"DANZI.TN","date":"14/05/2017"}}' http://openon.it:8888/message
# expected return 
echo
echo "########################################"
echo "course example with auth token inside the header"
CURTIME="$(date +%s)"
# course example auth token inside the header
curl -H "Content-Type: application/json"  -H "X-Auth-Token: ${AUTH_TOKEN}" -X POST -d '{"by":"info@danzi.tn.com","when":"'"$CURTIME"'","type":"corso","data":{"first_name":"Andrea","last_name":"Danzi","code":"WX012","company":"DANZI.TN","date":"14/05/2017"}}' http://openon.it:8888/message


