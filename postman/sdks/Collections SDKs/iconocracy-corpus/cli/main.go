package main

import (
	_ "example.com/iconocracy-corpus-sdk/cmd/get"
	_ "example.com/iconocracy-corpus-sdk/cmd/implementedapi"
	_ "example.com/iconocracy-corpus-sdk/cmd/post"
	_ "example.com/iconocracy-corpus-sdk/config"
	"example.com/iconocracy-corpus-sdk/root"
)

func main() {
	root.Execute()
}
