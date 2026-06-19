package post

import (
	"example.com/iconocracy-corpus-sdk/root"
	"github.com/spf13/cobra"
)

var Cmd = &cobra.Command{
	Use: "post",
}

func init() {
	Cmd.AddCommand(postDataCmd)
	root.AddCommand(Cmd)
}
