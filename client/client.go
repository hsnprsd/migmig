package main

import (
	"fmt"
	"io"
	"net"
)

func main() {
	conn, err := net.Dial("tcp", ":8080")
	if err != nil {
		panic(err)
	}

	message, err := io.ReadAll(conn)
	if err != nil {
		panic(err)
	}
	fmt.Println(string(message))
}
