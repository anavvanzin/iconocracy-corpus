package util

import (
	"fmt"
	"strconv"
)

func convertStringSlice[T any](input []string, parse func(string) (T, error), flagName string) ([]T, error) {
	result := make([]T, len(input))
	for i, s := range input {
		v, err := parse(s)
		if err != nil {
			return nil, fmt.Errorf("invalid value for %s[%d]: %w", flagName, i, err)
		}
		result[i] = v
	}
	return result, nil
}

func ConvertToInt64Slice(input []string, flagName string) ([]int64, error) {
	return convertStringSlice(input, func(s string) (int64, error) {
		return strconv.ParseInt(s, 10, 64)
	}, flagName)
}

func ConvertToFloat64Slice(input []string, flagName string) ([]float64, error) {
	return convertStringSlice(input, func(s string) (float64, error) {
		return strconv.ParseFloat(s, 64)
	}, flagName)
}

func ConvertToBoolSlice(input []string, flagName string) ([]bool, error) {
	return convertStringSlice(input, strconv.ParseBool, flagName)
}
