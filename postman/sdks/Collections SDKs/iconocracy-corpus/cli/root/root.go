package root

import (
	iconocracycorpussdk "example.com/iconocracy-corpus-sdk/sdk"
	"example.com/iconocracy-corpus-sdk/sdk/iconocracycorpussdkconfig"
	"fmt"
	"github.com/spf13/cobra"
	"github.com/spf13/viper"
	"os"
)

var rootCmd = &cobra.Command{
	Use:   "iconocracy-corpus-sdk",
	Short: "iconocracy-corpus-sdk CLI",
}

var authConfigurators []func(client any)

func Execute() {
	if err := rootCmd.Execute(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}

func AddCommand(cmd *cobra.Command) {
	rootCmd.AddCommand(cmd)
}

func RegisterAuthConfigurator(fn func(client any)) {
	authConfigurators = append(authConfigurators, fn)
}

func CreateSdkClient() *iconocracycorpussdk.IconocracyCorpusSDK {
	sdkConfig := iconocracycorpussdkconfig.NewConfig()

	if baseUrl := viper.GetString("base_url"); baseUrl != "" {
		sdkConfig.SetBaseURL(baseUrl)
	}

	client := iconocracycorpussdk.NewIconocracyCorpusSDK(sdkConfig)

	// Apply credentials file values (lower priority than env vars / config file).
	for _, configure := range authConfigurators {
		configure(client)
	}

	// Re-apply viper values last so env vars and config file always win over
	// any values loaded from the credentials file above.
	return client
}

func init() {
	viper.SetConfigName("config")
	viper.SetConfigType("yaml")
	viper.AddConfigPath("./config")
	viper.SetEnvPrefix("ICONOCRACY_CORPUS_SDK")
	viper.AutomaticEnv()

	if err := viper.ReadInConfig(); err != nil {
		if _, ok := err.(viper.ConfigFileNotFoundError); !ok {
			fmt.Fprintf(os.Stderr, "Warning: error reading config file: %v\n", err)
		}
	}
}
