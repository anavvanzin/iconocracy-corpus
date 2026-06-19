package get

import (
	"example.com/iconocracy-corpus-sdk/root"
	"github.com/spf13/cobra"
)

var Cmd = &cobra.Command{
	Use: "get",
}

func init() {
	Cmd.AddCommand(getDataCmd)
	root.AddCommand(Cmd)
}
