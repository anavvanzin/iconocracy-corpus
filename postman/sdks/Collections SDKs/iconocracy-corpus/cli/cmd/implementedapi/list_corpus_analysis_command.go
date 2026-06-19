package implementedapi

import (
	"encoding/json"
	"example.com/iconocracy-corpus-sdk/root"
	"fmt"
	"github.com/spf13/cobra"
)

var listCorpusAnalysisCmd = &cobra.Command{
	Use: "list-corpus-analysis",
	RunE: func(cmd *cobra.Command, args []string) error {

		client := root.CreateSdkClient()
		response, err := client.ImplementedAPI.ListCorpusAnalysis(cmd.Context())
		if err != nil {
			return err
		}

		if len(response) == 0 {
			fmt.Println("[empty response]")
		} else if json.Valid(response) {
			jsonData, err := json.MarshalIndent(json.RawMessage(response), "", "  ")
			if err != nil {
				fmt.Println(string(response))
			} else {
				fmt.Println(string(jsonData))
			}
		} else {
			fmt.Println(string(response))
		}

		return nil
	},
}

func init() {
}
