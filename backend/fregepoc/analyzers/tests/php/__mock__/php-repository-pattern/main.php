<?php
include_once 'UserRepository.php';
include_once 'UserController.php';

$dsn = "mysql:host=localhost;dbname=sandbox_php-repository-pattern";
try {
    $pdo = new PDO($dsn, "root", "");
} catch (Exception $e) {
    error_log($e->getMessage());
    exit('Something weird happened'); //something a user can understand
}

// Create the "repostory" object
$users = new UserRepository($pdo);

// Create the "controller"
$userController = new UserController($users);

// Create new User
$params = array(
    'username' => 'user1',
    'password' => 'password',
);
$userController->addUser($params);

// Fetch the user from the database
$params = array('username' => 'user1');
$user = $userController->getUser($params);
var_export($user);

// Modify the user
$params = array(
    'username' => 'user1',
    'oldPassword' => 'password',
    'newPassword' => 'password1',
);
$userController->changePassword($params);

// Fetch the user from the database
$params = array('username' => 'user1');
$user = $userController->getUser($params);
var_export($user);