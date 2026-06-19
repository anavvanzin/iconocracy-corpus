package iconocracycorpussdkconfig

// Environment type defines the available API environments.
type Environment string

// Environment constants define the available base URLs for different deployment environments.
// Use these constants when configuring the SDK client.
const (
	DefaultEnvironment       Environment = "https://postman-echo.com"
	PostmanEchoEnvironment   Environment = "https://postman-echo.com"
	Localhost8787Environment Environment = "http://localhost:8787"
)
