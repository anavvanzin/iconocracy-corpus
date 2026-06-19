package implementedapi

import (
	"encoding/json"
	"example.com/iconocracy-corpus-sdk/root"
	"example.com/iconocracy-corpus-sdk/sdk/implementedapi"
	sdkutil "example.com/iconocracy-corpus-sdk/sdk/param"
	"fmt"
	"github.com/spf13/cobra"
	"os"
)

var searchCorpusAnalysisCmd = &cobra.Command{
	Use: "search-corpus-analysis",
	RunE: func(cmd *cobra.Command, args []string) error {
		attr, err := cmd.Flags().GetString("attr")
		if err != nil {
			fmt.Fprintln(os.Stderr, err)
			return err
		}
		figure, err := cmd.Flags().GetString("figure")
		if err != nil {
			fmt.Fprintln(os.Stderr, err)
			return err
		}

		params := implementedapi.SearchCorpusAnalysisRequestParams{}
		if cmd.Flags().Changed("attr") {
			attrParam := sdkutil.Nullable[string]{Value: attr}
			params.Attr = &attrParam
		}
		if cmd.Flags().Changed("figure") {
			figureParam := sdkutil.Nullable[string]{Value: figure}
			params.Figure = &figureParam
		}
		client := root.CreateSdkClient()
		response, err := client.ImplementedAPI.SearchCorpusAnalysis(cmd.Context(), params)
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
	searchCorpusAnalysisCmd.Flags().StringP("attr", "", "", "")
	searchCorpusAnalysisCmd.Flags().StringP("figure", "", "", "")
}
