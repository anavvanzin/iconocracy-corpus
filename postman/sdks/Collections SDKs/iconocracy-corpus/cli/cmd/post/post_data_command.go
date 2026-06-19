package post

import (
	"encoding/json"
	"example.com/iconocracy-corpus-sdk/root"
	"example.com/iconocracy-corpus-sdk/sdk/post"
	"fmt"
	"github.com/spf13/cobra"
	"os"
)

var postDataCmd = &cobra.Command{
	Use:   "post-data",
	Short: "This is a POST request, submitting data to an API via the request body. This request submits JSON data, and the data is reflected in the response.",
	Long:  "This is a POST request, submitting data to an API via the request body. This request submits JSON data, and the data is reflected in the response.\n\nA successful POST request typically returns a `200 OK` or `201 Created` response code.\n\nBody schema:\n  {\n    \"name\": \"Add your name in the body\"\n  }\n\nExamples:\n  --body '{\"name\":\"Add your name in the body\"}'\n  --body-file ./body.json",
	RunE: func(cmd *cobra.Command, args []string) error {
		bodyStr, err := cmd.Flags().GetString("body")
		if err != nil {
			fmt.Fprintf(os.Stderr, "Error: failed to get body param: %v\n", err)
			return err
		}
		bodyFile, err := cmd.Flags().GetString("body-file")
		if err != nil {
			fmt.Fprintf(os.Stderr, "Error: failed to get body-file param: %v\n", err)
			return err
		}

		var bodyContent []byte
		if bodyFile != "" {
			bodyContent, err = os.ReadFile(bodyFile)
			if err != nil {
				return err
			}
		} else {
			bodyContent = []byte(bodyStr)
		}

		var requestBody post.PostDataRequest
		if len(bodyContent) > 0 {
			if err := json.Unmarshal(bodyContent, &requestBody); err != nil {
				return err
			}
		}

		client := root.CreateSdkClient()
		response, err := client.Post.PostData(cmd.Context(), requestBody)
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
	postDataCmd.Flags().String("body", "", "Request body as inline JSON, e.g. '{\"name\":\"Add your name in the body\"}'")
	postDataCmd.Flags().String("body-file", "", "Path to a file containing the request body")
	postDataCmd.MarkFlagsMutuallyExclusive("body", "body-file")
}
