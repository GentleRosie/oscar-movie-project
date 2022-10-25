package com.example.restwebserver;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
class GreetingController
{
    private static final String template = "Hello, %s!";

    GreetingController()
    {
    }

    @GetMapping("/hello")
    String hello()
    {
        return "Hello World!";
    }

    @GetMapping("/greeting")
    @ResponseBody
    Greeting greeting(@RequestParam(name = "name", defaultValue = "World") String name)
    {
        return new Greeting(String.format(template, name));
    }
}
