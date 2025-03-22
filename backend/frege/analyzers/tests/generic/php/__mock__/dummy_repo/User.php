<?php

class User
{
    private $id;
    private $username;
    private $password;
    private $first_name;
    private $last_name;

    public function __construct($username, $password)
    {
        $this->setUsername($username);
        $this->setPassword($password);
    }

    // Getters
    public function getUsername()
    {
        return $this->username;
    }

    public function getPassword()
    {
        return $this->password;
    }

    public function getFirst_name()
    {
        return $this->first_name;
    }

    public function getLast_name()
    {
        return $this->last_name;
    }

    public function getFullName()
    {
        if (isset($this->first_name) && isset($this->last_name)) {
            return $this->getFirstName() . ' ' . $this->getLastName();
        } else {
            return null;
        }
    }

    // Setters
    public function setId($id)
    {
        $this->id = $id;
    }

    public function setUsername($username)
    {
        $this->username = $username;
    }

    public function setPassword($password)
    {
        $this->password = $password;
    }

    public function setFirst_name($first_name)
    {
        $this->first_name = $first_name;
    }

    public function setLast_name($last_name)
    {
        $this->last_name = $last_name;
    }

    public function canChangePassword($oldPassword, $newPassword)
    {
        // put some business logic
        return true;
    }

    public function changePassword($oldPassword, $newPassword)
    {
        if (!$this->canChangePassword($oldPassword, $newPassword)) {
            throw new Exception("Cannot change password");
        }

        $this->password = $newPassword;
    }
}
