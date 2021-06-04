<?php
require __DIR__.'/vendor/autoload.php';
use Kreait\Firebase\Factory;
use Kreait\Firebase\ServiceAccount;
use Kreait\Firebase\Storage;


$factory = (new Factory)
    ->withServiceAccount('firebase_key/fintech-61df3-firebase-adminsdk-4vr8z-629365b6cf.json')
    ->withDatabaseUri('https://fintech-61df3-default-rtdb.firebaseio.com/');
    ;

$storage = $factory->createStorage();
$database = $factory->createDatabase();


//for test

$database->getReference('config/website')
   ->set([
       'name' => 'My Application',
       'emails' => [
           'support' => 'support@domain.tld',
           'sales' => 'sales@domain.tld',
       ],
       'website' => 'https://app.domain.tld',
      ]);

$database->getReference('config/website/name')->set('New name');


//done test


?>