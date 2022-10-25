package com.example.restwebserver;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;

@Entity
class Movie
{
    private @GeneratedValue @Id Long id;
    private String name;
    private String author;

    public Movie()
    {
    }

    public Movie(String name, String author)
    {
        this.name = name;
        this.author = author;
    }

    public Long getId()
    {
        return id;
    }

    public String getName()
    {
        return name;
    }

    public String getAuthor()
    {
        return author;
    }

    public void setId(Long id)
    {
        this.id = id;
    }

    public void setName(String name)
    {
        this.name = name;
    }

    public void setAuthor(String author)
    {
        this.author = author;
    }

    @Override
    public String toString()
    {
        return "Movie{id=" + this.id + ", name='" + this.name + "', author='" + this.author + "'}";
    }
}
