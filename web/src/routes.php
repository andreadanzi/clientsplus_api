<?php

$c = $app->getContainer(); //['settings']['security']['token'];
$auth_token = $c['settings']['security']['token'];


// get all messages
$app->get('/try', function ($request, $response, $args) {
    global $auth_token;
    $this->logger->addInfo("try GET request, started");
    $token = "";
    if(isset($_GET['token'])) $token = $_GET['token'];    
    $headers = $request->getHeaders();
    # TODO Undefined index: HTTP_X_AUTH_TOKEN
    if(isset($headers["HTTP_X_AUTH_TOKEN"])) {
        $head_auth_token = trim($headers["HTTP_X_AUTH_TOKEN"][0]);
        if(empty($token)) {
            $token = $head_auth_token;
        }
    }
    if($token != $auth_token) 
    { 
        $resp = $this->response->withStatus(400);
        return $resp->withJson(array("retcode"=>"1", "message"=>"Wrong or missing Token. Your test failed!"));
    }
    $this->logger->addInfo("try GET request, terminated");    
    return $this->response->withJson(array("retcode"=>"0", "message"=>"Your test succedeed!"));
});

// get all messages
$app->get('/messages', function ($request, $response, $args) {
    global $auth_token;
    $this->logger->addInfo("messages GET request, started");
    $token = "";
    if(isset($_GET['token'])) $token = $_GET['token'];    
    
    $headers = $request->getHeaders();
    # TODO Undefined index: HTTP_X_AUTH_TOKEN
    if(isset($headers["HTTP_X_AUTH_TOKEN"])) {
        $head_auth_token = trim($headers["HTTP_X_AUTH_TOKEN"][0]);
        if(empty($token)) {
            $token = $head_auth_token;
        }
    }
    if($token != $auth_token) 
    {
        $resp = $this->response->withStatus(400);
        return $resp->withJson(array("retcode"=>"1","error" => array("code"=>"250","message"=>"Wrong or Missing Token!") ) );
    }
    $sql = "SELECT idmessage_log, timestamp, hashstring, by_email, when_timestamp, type_event, import_status FROM message_log
                                ORDER BY
                                message_log.idmessage_log ASC";
    $child_sql = "SELECT 
                                message_log.idmessage_log,
                                message.datastructure_value,
                                datastructure.name,
                                email.email_address,
                                event_types.event_type_code
                                FROM 
                                message,
                                datastructure,
                                email,
                                event_types,
                                message_log
                                WHERE
                                message.message_log_idmessage_log = :id
                                AND message.datastructure_iddatastructure = datastructure.iddatastructure
                                AND message.email_idemail = email.idemail
                                AND event_types.idevent_types = message.event_types_idevent_types
                                AND datastructure.event_types_idevent_types = event_types.idevent_types 
                                AND message_log.idmessage_log = message.message_log_idmessage_log
                                ORDER BY
                                message_log.idmessage_log ASC";                                
    $sth = $this->db->prepare($sql);
    $sth->execute();
    $messages = $sth->fetchAll();
    $outs = array();
    $sth = $this->db->prepare($child_sql);
    foreach($messages as $item) {
        $message_id = $item["idmessage_log"];
        $sth->bindParam("id", $message_id);
        $sth->execute();
        $message_data = $sth->fetchAll();
        $dataArray = [];
        foreach($message_data as $data_item) {
            $dataArray[$data_item['name']] = $data_item['datastructure_value'];
        }
        $outs[]= array("id"=>$message_id
                       ,"by"=> $item["by_email"]
                       ,"when"=> $item["when_timestamp"]
                       ,"type"=> $item["type_event"]
                       , "data"=> $dataArray
                       ,"status"=> $item["import_status"]
                       );
    }
    $this->logger->addInfo("messages GET request, terminated");
    return $this->response->withJson($outs);
});

$app->post('/message', function ($request, $response) {
        global $auth_token;
        $this->logger->addInfo("message POST request, started");
        $input = $request->getParsedBody();
        $input['id'] = 0;
        $token = "";
        if(!isset($input['when']) ) {
            $input['retcode'] = 1;
            $input['error'] = array("code"=>"130","message"=>"when parameter is missing from request!");
            $resp = $this->response->withStatus(400);
            return $resp->withJson($input);
        }
        if(!isset($input['type'])) {
            $input['retcode'] = 1;
            $input['error'] = array("code"=>"140","message"=>"type parameter is missing from request!");
            $resp = $this->response->withStatus(400);
            return $resp->withJson($input);
        }
        if(!isset($input['by'])) {
            $input['retcode'] = 1;
            $input['error'] = array("code"=>"150","message"=>"by parameter is missing from request!");
            $resp = $this->response->withStatus(400);
            return $resp->withJson($input);
        }
        if(isset($input['token'])) $token = $input['token'];
        
        $this->logger->addInfo("message ok!");
        $headers = $request->getHeaders();
        # TODO Undefined index: HTTP_X_AUTH_TOKEN
        if(isset($headers["HTTP_X_AUTH_TOKEN"])) {
            $head_auth_token = trim($headers["HTTP_X_AUTH_TOKEN"][0]);
            if(empty($token)) {
                $token = $head_auth_token;
            }
        }
        if($token != $auth_token) 
        {
            // throw new InvalidArgumentException('Wrong Auth Token');
            $input['retcode'] = 1;
            $input['error'] = array("code"=>"250","message"=>"Wrong or Missing Token!");
            $resp = $this->response->withStatus(400);
            return $resp->withJson($input);
        }
        $strToHash = $input['when'];
        $strToHash .= $input['type'];
        $strToHash .= $input['by'];
        $hashed = hash("md5",$strToHash);
        $payload = $input['data'];
        // Check if exists
        $sql = "SELECT count(*) AS cnt FROM message_log WHERE hashstring =:hs";
        $sth = $this->db->prepare($sql);
        $sth->bindParam("hs", $hashed);
        $sth->execute();
        $retCnt = $sth->fetchObject();
        $input['retcode'] = 0;
        if( $retCnt->cnt > 0 ) {
            $this->logger->addInfo("message_log already exists! when = ".$input['when']. " type = ". $input['by'] . " by = " .$input['by']);
            $input['retcode'] = 1;
            $input['error'] = array("code"=>"120","message"=>"Message Already Exists! Params are when = ".$input['when']. " type = ". $input['by'] . " by = " .$input['by']);
        } else {
            $sql = "INSERT INTO message_log (when_timestamp,type_event,by_email,hashstring, import_status, import_date, timestamp, payload ) VALUES (:when_timestamp,:type_event,:by_email,:hashstring, 0, NOW(), from_unixtime(:when_timestamp), :payload)";
            $sth = $this->db->prepare($sql);
            $sth->bindParam("when_timestamp", $input['when']);
            $sth->bindParam("type_event", $input['type']);
            $sth->bindParam("by_email", $input['by']);
            $sth->bindParam("hashstring",$hashed);
            $insert_payload = $payload;
            if( array_key_exists("file",$insert_payload )) {
               unset($insert_payload['file']);
            }
            $sth->bindParam("payload",json_encode($insert_payload) );
            $sth->execute();
            $input['id'] = $this->db->lastInsertId();
            $this->logger->addInfo("new message_log id = " . $input["id"]);
            // check type
            $sql = "SELECT 
                    *
                    FROM 
                    event_types
                    WHERE
                    event_types.event_type_code = :type_event";
            $sth = $this->db->prepare($sql);
            $sth->bindParam("type_event", $input['type']);
            $sth->execute();
            $retObj = $sth->fetchObject();
            $id_type = 0;
            if(!$retObj) {
                $sql = "INSERT INTO event_types (event_type_code, timestamp) VALUES(:type_event, from_unixtime(:when_timestamp))";
                $sth = $this->db->prepare($sql);
                $sth->bindParam("type_event", $input['type']);
                $sth->bindParam("when_timestamp", $input['when']);
                $sth->execute();
                $id_type = $this->db->lastInsertId();
            	$this->logger->addInfo("new type id = " . $id_type);
            } else {
                $id_type = $retObj->idevent_types;
            	$this->logger->addInfo("existing type id = " . $id_type);
            }
            // check email
            $sql = "SELECT *
                    FROM email
                    WHERE
                    email_address =:by_email";
            $sth = $this->db->prepare($sql);
            $sth->bindParam("by_email", $input['by']);
            $sth->execute();
            $retObj = $sth->fetchObject();
            $idemail = 0;
            if(!$retObj) {
                $sql = "INSERT INTO email (email_address,import_status, import_relations, import_date, timestamp) VALUES(:by_email, 0, 'ND',NOW(), from_unixtime(:when_timestamp))";
                $sth = $this->db->prepare($sql);
                $sth->bindParam("by_email", $input['by']);
                $sth->bindParam("when_timestamp", $input['when']);
                $sth->execute();
                $idemail = $this->db->lastInsertId();
            	$this->logger->addInfo("new email id = " . $idemail);
            } else {
                $idemail = $retObj->idemail;
            	$this->logger->addInfo("existing email id = " . $idemail);
            }
            // check payload
            $sql = "SELECT *
                    FROM datastructure
                    WHERE
                    datastructure.event_types_idevent_types = :type_event
                    AND datastructure.name = :key";
            $sthDs = $this->db->prepare($sql);
            if(count($payload)) {
                $this->logger->addInfo("Payload available with " .count($payload). " items");
                foreach($payload as $key=>$value) {
                    if($key=='file') {
                        $filename = "";
                        $this->logger->addInfo("POST request contain file parameter");
                        if(empty($value)) {
                            $this->logger->addInfo("Uploaded file is empty");
                        } else {
                            $this->logger->addInfo("Uploaded file is NOT empty (".count($value).")");
                            list($type, $data) = explode(';', $value);
                            list(, $data)      = explode(',', $data);
                            $data = base64_decode($data);
                            $this->logger->addInfo("type is ". $type);
                            list($pre, $ext) = explode('/',$type);
                            $filename = "uploaded_".$input['type']."-".$input['when'].".".$ext;
                            $this->logger->addInfo("Uploaded file name is " . $filename);
                            file_put_contents("/data_backend/".$filename, $data);
                        }
                        $value = $filename;
                    }
                    $sthDs->bindParam("type_event", $id_type);
                    $sthDs->bindParam("key", $key);
                    $sthDs->execute();
                    $retObj = $sthDs->fetchObject();
                    $iddatastructure = 0;
                    if(!$retObj) {
                        $sql = "INSERT INTO datastructure (event_types_idevent_types, name, type) VALUES(:type_event, :key, :datatype)";
                        $sth = $this->db->prepare($sql);
                        $sth->bindParam("type_event",$id_type);
                        $sth->bindParam("key", $key);
                        $datatype="string";
                        $sth->bindParam("datatype", $datatype);
                        $sth->execute();
                        $iddatastructure = $this->db->lastInsertId();
                    } else {
                        $iddatastructure = $retObj->iddatastructure;
                    }
                    $sql = "INSERT INTO message (	message_log_idmessage_log, event_types_idevent_types, email_idemail, datastructure_iddatastructure, datastructure_name, datastructure_value) VALUES(:id_message, :type_event, :by_email, :datastructure, :key, :value)";
                    $sth = $this->db->prepare($sql);
                    $sth->bindParam("id_message",$input['id']);
                    $sth->bindParam("type_event",$id_type);
                    $sth->bindParam("by_email", $idemail);
                    $sth->bindParam("datastructure", $iddatastructure);
                    $sth->bindParam("key", $key);
                    $sth->bindParam("value", $value);
                    $sth->execute();
                }
            }
        }
        $this->logger->addInfo("message POST request, terminated");
        return $this->response->withJson($input);
    });
