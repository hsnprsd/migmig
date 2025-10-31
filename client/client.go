package main

import (
	"fmt"
	"io"
	"net"

	"github.com/hsnprsd/migmig/common"
)

func main() {
	conn, err := net.Dial("tcp", ":8080")
	if err != nil {
		panic(err)
	}
	defer conn.Close()

	request := &common.Request{
		Addr: "icanhazip.com",
		Port: 80,
	}

	err = request.Write(conn)
	if err != nil {
		panic(err)
	}

	// send http request
	_, err = conn.Write([]byte("GET / HTTP/1.1\r\nHost: icanhazip.com\r\nConnection: close\r\nContent-Length: 0\r\n\r\n"))
	if err != nil {
		panic(err)
	}

	response, err := io.ReadAll(conn)
	if err != nil {
		panic(err)
	}

	fmt.Println(string(response))
}
