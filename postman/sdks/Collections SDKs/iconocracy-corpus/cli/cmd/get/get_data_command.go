package get

import (
	"encoding/json"
	"example.com/iconocracy-corpus-sdk/root"
	"fmt"
	"github.com/spf13/cobra"
)

var getDataCmd = &cobra.Command{
	Use:   "get-data",
	Short: "This is a GET request and it is used to \"get\" data from an endpoint. There is no request body for a GET request, but you can use query parameters to help specify the resource you want data on (e.g., in this request, we have `id=1`).",
	RunE: func(cmd *cobra.Command, args []string) error {

		client := root.CreateSdkClient()
		response, err := client.Get.GetData(cmd.Context())
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
