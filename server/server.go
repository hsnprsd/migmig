package main

import (
	"log"
	"net"
)

func serveConn(conn net.Conn) {
	defer conn.Close()
	_, err := conn.Write([]byte("hello world"))
	if err != nil {
		panic(err)
	}
}

func main() {
	s, err := net.Listen("tcp", ":8080")
	if err != nil {
		panic(err)
	}

	for {
		conn, err := s.Accept()
		if err != nil {
			log.Printf("could not accept a new connection: %v\n", err)
		}

		go serveConn(conn)
	}
}
