package com.example.restwebserver;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;

@Entity
public class Greeting
{
    private @GeneratedValue @Id Long id;
    private String content;

    public Greeting()
    {
    }

    public Greeting(String content)
    {
        this.content = content;
    }

    public Long getId()
    {
        return id;
    }

    public String getContent()
    {
        return content;
    }

    public void setId(Long id)
    {
        this.id = id;
    }

    public void setContent(String content)
    {
        this.content = content;
    }

    @Override
    public String toString()
    {
        return "Greeting{id=" + this.id + ", content='" + this.content + "'}";
    }
}
