<?php
return [
    'settings' => [
        'displayErrorDetails' => true, // set to false in production
        'addContentLengthHeader' => false, // Allow the web server to send the content-length header

        // Renderer settings
        'renderer' => [
            'template_path' => __DIR__ . '/../templates/',
        ],

        // Monolog settings
        'logger' => [
            'name' => 'slim-app',
            'path' => __DIR__ . '/../logs/app.log',
            'level' => \Monolog\Logger::DEBUG,
        ],
        
        // Mysql settings
        "db" => [
            "host" => "localhost",
            "dbname" => "clientsplus",
            "user" => "root",
            "pass" => "root"
        ],
        'security' => [
            'token' => 'AetheiNae0waiy0aeB1angooy5Foh3Th',
        ]
    ],
];
