package main

import (
	"encoding/gob"
	"net"

	"github.com/hsnprsd/migmig/common"
)

func main() {
	conn, err := net.Dial("tcp", ":8080")
	if err != nil {
		panic(err)
	}

	request := &common.Request{
		Addr: "google.com",
		Port: 443,
	}

	err = gob.NewEncoder(conn).Encode(request)
	if err != nil {
		panic(err)
	}
}
