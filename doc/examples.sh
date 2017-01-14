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
URL=https://crmtest.rothoblaas.com/api


# test connection
curl -X GET $URL/try?token=$AUTH_TOKEN
# expected return {"retcode":"0","message":"Your test succedeed!"}
echo
echo "########################################"
echo "registration example"
# registration example
curl -H "Content-Type: application/json" -X POST -d '{"token":"'"$AUTH_TOKEN"'", "by":"mario.rossi@example.com","when":"'"$CURTIME"'","type":"registration","data":{"first_name": "Mario","last_name": "Rossi","language": "IT","tel": "+391234567890","job": "engineer","company": "Mario Rossi Engineering","address": "Piazza del Popolo 11","city": "Roma","region": "IT-62","country": "IT","zip": "12345"}}' $URL/message
sleep 2
CURTIME="$(date +%s)"
echo
echo "########################################"
echo "newsletter_subscribe example"
# newsletter_subscribe example NEW USER
curl -H "Content-Type: application/json" -X POST -d '{"token":"'"$AUTH_TOKEN"'", "by":"mario.rossi@example.com","when":"'"$CURTIME"'","type":"newsletter_subscribe","data":{"first_name": "Mario","last_name": "Rossi","language": "IT"}}' $URL/message
sleep 2
CURTIME="$(date +%s)"
echo
echo "########################################"
echo "newsletter_subscribe example"
# newsletter_subscribe example REGISTERED USER
curl -H "Content-Type: application/json" -X POST -d '{"token":"'"$AUTH_TOKEN"'", "by":"mario.rossi@example.com","when":"'"$CURTIME"'","type":"newsletter_subscribe"}' $URL/message
sleep 2
CURTIME="$(date +%s)"
echo
echo "########################################"
echo "newsletter_unsubscribe example"
# newsletter_subscribe example REGISTERED USER
curl -H "Content-Type: application/json" -X POST -d '{"token":"'"$AUTH_TOKEN"'", "by":"mario.rossi@example.com","when":"'"$CURTIME"'","type":"newsletter_unsubscribe"}' $URL/message
sleep 2
CURTIME="$(date +%s)"
echo
echo "########################################"
echo "registration example"
# registration example
curl -H "Content-Type: application/json" -X POST -d '{"token":"'"$AUTH_TOKEN"'", "by":"mario.bianchi@example.com","when":"'"$CURTIME"'","type":"registration","data":{"first_name": "Mario","last_name": "Bianchi","language": "IT","tel": "+391234567890","job": "engineer","company": "Mario Bianchi Engineering","address": "Piazza del Popolo 11","city": "Roma","region": "IT-62","country": "IT","zip": "12345"}}' $URL/message
sleep 2
CURTIME="$(date +%s)"
echo
echo "########################################"
echo "consulting example"
# consulting example
curl -H "Content-Type: application/json" -X POST -d '{"token":"'"$AUTH_TOKEN"'", "by":"mario.bianchi@example.com","when":"'"$CURTIME"'","type":"consulting","data":{"category": "fixing","description": "Testo della richiesta di consulenza"}}' $URL/message
sleep 2
CURTIME="$(date +%s)"
echo
echo "########################################"
echo "download example"
# download example
curl -H "Content-Type: application/json" -X POST -d '{"token":"'"$AUTH_TOKEN"'","by":"mario.rossi@example.com","when":"'"$CURTIME"'","type":"download","data":{"category":"software","description": "MyProject 1.3","filename":"calcolo_viti.xls"}}' $URL/message
echo
echo "########################################"
echo "new_course example"
# new_course
curl -H "Content-Type: application/json"  -X POST -d '{"token":"'"$AUTH_TOKEN"'","by":"courses@rothoblaas.com","when":"'"$CURTIME"'","type":"new_course","data":{"id":45,"begins_at":124578120,"ends_at":124578120,"language":"IT","name":"Corso avanzato di carpenteria"}}' $URL/message
echo
echo "########################################"
echo "course_subscribe example"
# course_subscribe
curl -H "Content-Type: application/json"  -X POST -d '{"token":"'"$AUTH_TOKEN"'","by":"mario.rossi@example.com","when":"'"$CURTIME"'","type":"course_subscribe","data":{"course_id":45,"plan": "course_only","intolerances": "gluten","overnight_stay": "none"}}' $URL/message
echo
echo "########################################"
echo "course example with error"
# course example, same message as previous, error expected!
curl -H "Content-Type: application/json"  -X POST -d '{"token":"'"$AUTH_TOKEN"'","by":"mario.rossi@example.com","when":"'"$CURTIME"'","type":"course_subscribe","data":{"course_id":45,"plan": "course_only","intolerances": "gluten","overnight_stay": "none"}}' $URL/message
echo
echo "########################################"
echo "course example with auth token inside the header"
CURTIME="$(date +%s)"
# course example auth token inside the header
curl -H "Content-Type: application/json"  -H "X-Auth-Token: ${AUTH_TOKEN}" -X POST -d '{"by":"mario.bianchi@example.com","when":"'"$CURTIME"'","type":"course_subscribe","data":{"course_id":45,"plan": "course_only","intolerances": "gluten","overnight_stay": "none"}}' $URL/message
echo
echo "########################################"
echo "registration example with error: wrong token"
# registration example with error: wrong token
curl -H "Content-Type: application/json" -X POST -d '{"token":"'"$WRONG_AUTH_TOKEN"'", "by":"mario.rossi@example.com","when":"'"$CURTIME"'","type":"registration","data":{"first_name": "Mario","last_name": "Rossi","language": "IT","tel": "+391234567890","job": "engineer","company": "Mario Rossi Engineering","address": "Piazza del Popolo 11","city": "Roma","region": "IT-62","country": "IT","zip": "12345"}}' $URL/message
echo
echo "########################################"
echo "newsletter_subscribe example with error: missing required parameter by"
# newsletter_subscribe examplewith error: missing required parameter by
curl -H "Content-Type: application/json" -X POST -d '{"token":"'"$AUTH_TOKEN"'","when":"'"$CURTIME"'","type":"newsletter_subscribe"}' $URL/message
echo
echo "########################################"
echo "consulting example with error: missing required parameter when"
# consulting example with error: missing required parameter when
curl -H "Content-Type: application/json" -X POST -d '{"token":"'"$AUTH_TOKEN"'", "by":"mario.bianchi@example.com","type":"consulting","data":{"first_name": "Mario","last_name": "Rossi","language": "IT","tel": "+391234567890","job": "engineer","company": "Mario Rossi Engineering","address": "Piazza del Popolo 11","city": "Roma","region": "IT-62","country": "IT","zip": "12345","category": "fixing","description": "Testo della richiesta di consulenza"}}' $URL/message
echo
echo "########################################"
echo "download example with error: missing required parameter type" 
# download example with error: missing required parameter type
curl -H "Content-Type: application/json" -X POST -d '{"token":"'"$AUTH_TOKEN"'","by":"mario.bianchi@example.com","when":"'"$CURTIME"'","data":{"category":"software","description": "MyProject 1.3","filename":"calcolo_viti.xls"}}' $URL/message
