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
WRONG_AUTH_TOKEN=wrongtoken1345687
CURTIME="$(date +%s)"
# 'http://10.88.102.73/vte'
URL=http://10.88.102.73/api
# test connection
curl -X GET $URL/try?token=$AUTH_TOKEN
echo
echo "########################################"
echo "registration example"
# registration example
curl -H "Content-Type: application/json" -X POST -d '{"token":"'"$AUTH_TOKEN"'", "by":"mario.rossi@example.com","when":"'"$CURTIME"'","type":"registration","data":{"first_name": "Mario","last_name": "Rossi","language": "IT","tel": "+391234567890","job": "engineer","company": "Mario Rossi Engineering","address": "Piazza del Popolo 11","city": "Roma","region": "IT-62","country": "IT","zip": "12345"}}' $URL/message
sleep 2
CURTIME="$(date +%s)"
echo
echo "########################################"
echo "course_subscribe example"
# course_subscribe
curl -H "Content-Type: application/json"  -X POST -d '{"token":"'"$AUTH_TOKEN"'","by":"mario.rossi@example.com","when":"'"$CURTIME"'","type":"course_subscribe","data":{"course_id":45,"plan": "course_only","intolerances": "gluten","overnight_stay": "none"}}' $URL/message
