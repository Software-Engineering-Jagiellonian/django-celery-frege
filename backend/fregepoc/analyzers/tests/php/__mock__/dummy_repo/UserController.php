<?php
include_once 'User.php';
include_once 'IUserRepository.php';
include_once 'UserRepository.php';

class UserController
{
    private $users;

    public function __construct(IUserRepository $users)
    {
        $this->users = $users;
    }

    public function addUser($params)
    {
        $user = new User($params['username'], $params['password']);
        $this->users->add($user);
    }

    public function getUser($params): User
    {
        return $this->users->findByUsername($params['username']);
    }

    public function changePassword($params)
    {
        $user = $this->getUser($params);
        $user->changePassword($params['oldPassword'], $params['newPassword']);
        $this->users->update($user);
    }
}
