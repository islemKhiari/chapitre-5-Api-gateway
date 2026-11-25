package com.awd.candidat;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;



@RestController
@RequestMapping("/mic3/candidat")
public class CandidatRestApi {

        @Value("${server.port}")
    private String port;

    @GetMapping("/hello")
    public String sayHello() {
        return "Hello Im microservice 2! Port : " + port;
    }
}