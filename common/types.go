package common

import (
	"encoding/binary"
	"io"
)

type Request struct {
	Addr string
	Port uint16
}

func (r *Request) Write(w io.Writer) error {
	_, err := w.Write([]byte{byte(len(r.Addr))})
	if err != nil {
		return err
	}
	_, err = w.Write([]byte(r.Addr))
	if err != nil {
		return err
	}
	err = binary.Write(w, binary.BigEndian, &r.Port)
	return err
}

func (r *Request) ReadFrom(reader io.Reader) error {
	buf := make([]byte, 1)
	_, err := io.ReadFull(reader, buf)
	if err != nil {
		return err
	}

	buf = make([]byte, buf[0])
	_, err = io.ReadFull(reader, buf)
	if err != nil {
		return err
	}

	r.Addr = string(buf)

	err = binary.Read(reader, binary.BigEndian, &r.Port)
	return err
}
