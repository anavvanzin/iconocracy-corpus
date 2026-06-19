package post

import (
	"encoding/json"
	"example.com/iconocracy-corpus-sdk/sdk/internal/unmarshal"
	"example.com/iconocracy-corpus-sdk/sdk/param"
)

type PostDataRequest struct {
	Name *param.Nullable[string] `json:"name,omitempty"`
}

func (p PostDataRequest) String() string {
	jsonData, err := json.MarshalIndent(p, "", "  ")
	if err != nil {
		return "error converting struct: PostDataRequest to string"
	}
	return string(jsonData)
}

func (p *PostDataRequest) UnmarshalJSON(data []byte) error {
	return unmarshal.UnmarshalNullable(data, p)
}
