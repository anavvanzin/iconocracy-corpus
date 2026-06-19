/**
 * Available API environments with their base URLs.
 * Use these constants to configure the SDK for different environments (production, staging, etc.).
 */
export enum Environment {
  /** DEFAULT environment base URL */
  DEFAULT = 'https://postman-echo.com',
  /** POSTMAN_ECHO environment base URL */
  POSTMAN_ECHO = 'https://postman-echo.com',
  /** LOCALHOST8787 environment base URL */
  LOCALHOST8787 = 'http://localhost:8787',
}
