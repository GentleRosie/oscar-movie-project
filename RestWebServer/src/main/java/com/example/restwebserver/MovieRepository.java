package com.example.restwebserver;

import org.springframework.data.jpa.repository.JpaRepository;

interface MovieRepository extends JpaRepository<Movie, Long>
{
}
