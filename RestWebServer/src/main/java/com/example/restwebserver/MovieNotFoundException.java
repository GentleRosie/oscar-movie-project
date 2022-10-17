package com.example.restwebserver;

class MovieNotFoundException extends RuntimeException
{
    MovieNotFoundException(Long id)
    {
        super("Could not find employee " + id);
    }
}
