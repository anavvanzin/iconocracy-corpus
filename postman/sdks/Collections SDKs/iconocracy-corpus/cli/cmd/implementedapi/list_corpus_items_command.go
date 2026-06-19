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

var listCorpusItemsCmd = &cobra.Command{
	Use: "list-corpus-items",
	RunE: func(cmd *cobra.Command, args []string) error {
		country, err := cmd.Flags().GetString("country")
		if err != nil {
			fmt.Fprintln(os.Stderr, err)
			return err
		}
		regime, err := cmd.Flags().GetString("regime")
		if err != nil {
			fmt.Fprintln(os.Stderr, err)
			return err
		}
		q, err := cmd.Flags().GetString("q")
		if err != nil {
			fmt.Fprintln(os.Stderr, err)
			return err
		}

		params := implementedapi.ListCorpusItemsRequestParams{}
		if cmd.Flags().Changed("country") {
			countryParam := sdkutil.Nullable[string]{Value: country}
			params.Country = &countryParam
		}
		if cmd.Flags().Changed("regime") {
			regimeParam := sdkutil.Nullable[string]{Value: regime}
			params.Regime = &regimeParam
		}
		if cmd.Flags().Changed("q") {
			qParam := sdkutil.Nullable[string]{Value: q}
			params.Q = &qParam
		}
		client := root.CreateSdkClient()
		response, err := client.ImplementedAPI.ListCorpusItems(cmd.Context(), params)
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
	listCorpusItemsCmd.Flags().StringP("country", "", "", "")
	listCorpusItemsCmd.Flags().StringP("regime", "", "", "")
	listCorpusItemsCmd.Flags().StringP("q", "", "", "")
}
