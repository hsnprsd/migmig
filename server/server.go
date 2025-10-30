package main

import (
	"encoding/gob"
	"log"
	"net"

	"github.com/hsnprsd/migmig/common"
)

func serveConn(conn net.Conn) {
	defer conn.Close()

	request := new(common.Request)
	err := gob.NewDecoder(conn).Decode(request)
	if err != nil {
		panic(err)
	}
	log.Printf("request from %s -> %s:%d\n", conn.LocalAddr().String(), request.Addr, request.Port)
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
