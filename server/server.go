package main

import (
	"fmt"
	"io"
	"log"
	"net"

	"github.com/hsnprsd/migmig/common"
)

func serveConn(conn net.Conn) {
	defer conn.Close()
	defer log.Printf("client disconnected: %s\n", conn.RemoteAddr().String())

	request := new(common.Request)
	err := request.ReadFrom(conn)
	if err != nil {
		panic(err)
	}

	log.Printf("request from %s -> %s:%d\n", conn.RemoteAddr().String(), request.Addr, request.Port)

	remoteConn, err := net.Dial("tcp", fmt.Sprintf("%s:%d", request.Addr, request.Port))
	if err != nil {
		panic(err)
	}
	defer remoteConn.Close()

	closed := make(chan struct{}, 2)
	go func() {
		defer log.Println("client conn closed")
		io.Copy(remoteConn, conn)
		closed <- struct{}{}
	}()
	go func() {
		defer log.Println("remote conn closed")
		io.Copy(conn, remoteConn)
		closed <- struct{}{}
	}()

	<-closed
	remoteConn.Close()
	conn.Close()
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
