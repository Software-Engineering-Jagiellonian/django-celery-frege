<?php

interface IUserRepository
{
    public function add(User $user);
    public function findByUsername($username): User;
    public function update(User $user);
    public function remove(User $user);
}