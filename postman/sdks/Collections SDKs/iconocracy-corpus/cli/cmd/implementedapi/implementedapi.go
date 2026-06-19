package implementedapi

import (
	"example.com/iconocracy-corpus-sdk/root"
	"github.com/spf13/cobra"
)

var Cmd = &cobra.Command{
	Use: "implemented-api",
}

func init() {
	Cmd.AddCommand(getDiaryCmd)
	Cmd.AddCommand(getScoutDataCmd)
	Cmd.AddCommand(getCorpusStatsCmd)
	Cmd.AddCommand(getCorpusCountriesCmd)
	Cmd.AddCommand(searchCorpusAnalysisCmd)
	Cmd.AddCommand(listCorpusAnalysisCmd)
	Cmd.AddCommand(listCorpusItemsCmd)
	Cmd.AddCommand(getCorpusItemCmd)
	root.AddCommand(Cmd)
}
