package config

import (
	"example.com/iconocracy-corpus-sdk/root"
	"fmt"
	"github.com/spf13/cobra"
	"github.com/spf13/viper"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
)

// Config keys and their descriptions.
// These keys map to environment variables with the prefix ICONOCRACY_CORPUS_SDK_
// (e.g. base_url → ICONOCRACY_CORPUS_SDK_BASE_URL).
//
// Available configuration keys:
//
//	base_url  - Base URL for all API requests
var configKeys = []string{
	"base_url",
}

var Cmd = &cobra.Command{
	Use:   "config",
	Short: "Manage iconocracy-corpus-sdk CLI configuration",
	Long: `Manage CLI configuration settings.

Configuration is resolved in the following order (highest priority first):
  1. Environment variables (ICONOCRACY_CORPUS_SDK_<KEY>, e.g. ICONOCRACY_CORPUS_SDK_BASE_URL)
  2. Config file (./config/config.yaml, relative to where the CLI is invoked)
  3. Saved credentials (~/.iconocracy-corpus-sdk/credentials, managed by setup-auth)
  4. Built-in defaults

Available keys:
  base_url             Base URL for all API requests
`,
}

var setCmd = &cobra.Command{
	Use:   "set <key> <value>",
	Short: "Set a configuration value",
	Long:  "Set a configuration value in the local config file.",
	Args:  cobra.ExactArgs(2),
	RunE: func(cmd *cobra.Command, args []string) error {
		key, value := args[0], args[1]
		if !isValidKey(key) {
			return fmt.Errorf("unknown config key %q\n\nRun 'iconocracy-corpus-sdk config --help' to see available keys", key)
		}
		if err := ensureConfigFile(); err != nil {
			return fmt.Errorf("could not create config file: %w", err)
		}
		viper.Set(key, value)
		return viper.WriteConfig()
	},
}

var getCmd = &cobra.Command{
	Use:   "get <key>",
	Short: "Get a configuration value",
	Long:  "Get a configuration value, showing the resolved value from any source.",
	Args:  cobra.ExactArgs(1),
	RunE: func(cmd *cobra.Command, args []string) error {
		key := args[0]
		if !isValidKey(key) {
			return fmt.Errorf("unknown config key %q\n\nRun 'iconocracy-corpus-sdk config --help' to see available keys", key)
		}
		value := viper.GetString(key)
		if value == "" {
			fmt.Fprintf(cmd.OutOrStdout(), "%s is not set\n", key)
		} else {
			fmt.Fprintf(cmd.OutOrStdout(), "%s = %s\n", key, value)
		}
		return nil
	},
}

var listCmd = &cobra.Command{
	Use:   "list",
	Short: "List all configuration settings",
	Long:  "List all configuration settings and their current resolved values.",
	RunE: func(cmd *cobra.Command, args []string) error {
		for _, key := range configKeys {
			value := viper.GetString(key)
			if value == "" {
				fmt.Fprintf(cmd.OutOrStdout(), "%s = (not set)\n", key)
			} else {
				fmt.Fprintf(cmd.OutOrStdout(), "%s = %s\n", key, value)
			}
		}
		return nil
	},
}

var editCmd = &cobra.Command{
	Use:   "edit",
	Short: "Edit the config file in your $EDITOR",
	Long:  "Open the config file in your $EDITOR. The file is created if it does not exist.",
	RunE: func(cmd *cobra.Command, args []string) error {
		if err := ensureConfigFile(); err != nil {
			return fmt.Errorf("could not create config file: %w", err)
		}
		configFile := viper.ConfigFileUsed()
		editor := os.Getenv("EDITOR")
		if editor == "" {
			editor = os.Getenv("VISUAL")
		}
		if editor == "" {
			return fmt.Errorf("no editor found: set $EDITOR or $VISUAL (e.g. export EDITOR=vim)")
		}
		editorParts := strings.Fields(editor)
		c := exec.Command(editorParts[0], append(editorParts[1:], configFile)...)
		c.Stdin = os.Stdin
		c.Stdout = os.Stdout
		c.Stderr = os.Stderr
		return c.Run()
	},
}

// ensureConfigFile creates ./config/config.yaml in the current working directory
// if it does not exist, then points viper at it so WriteConfig succeeds.
func ensureConfigFile() error {
	dir := filepath.Join(".", "config")
	if err := os.MkdirAll(dir, 0o755); err != nil {
		return err
	}
	configFile := filepath.Join(dir, "config.yaml")
	if _, err := os.Stat(configFile); os.IsNotExist(err) {
		f, err := os.Create(configFile)
		if err != nil {
			return err
		}
		defer f.Close()
	}
	if viper.ConfigFileUsed() == "" {
		viper.SetConfigFile(configFile)
		// An empty file is not valid YAML so viper will error — that is fine and expected.
		// Any other error (e.g. malformed YAML) is propagated to prevent silently
		// overwriting the user's config and losing existing values.
		if err := viper.ReadInConfig(); err != nil {
			if s, statErr := os.Stat(configFile); statErr == nil && s.Size() > 0 {
				return fmt.Errorf("error reading config file %q: %w", configFile, err)
			}
		}
	}
	return nil
}

func isValidKey(key string) bool {
	for _, k := range configKeys {
		if k == key {
			return true
		}
	}
	return false
}

func init() {
	Cmd.AddCommand(setCmd, getCmd, listCmd, editCmd)
	root.AddCommand(Cmd)
}
