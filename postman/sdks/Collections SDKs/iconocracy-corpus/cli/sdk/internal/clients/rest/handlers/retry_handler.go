package handlers

import (
	"errors"
	"math"
	"math/rand"
	"time"

	"example.com/iconocracy-corpus-sdk/sdk/internal/clients/rest/httptransport"
)

// rng is seeded at package init to ensure non-deterministic jitter across Go versions.
// The global math/rand source is only auto-seeded from Go 1.20 onward.
var rng = rand.New(rand.NewSource(time.Now().UnixNano()))

// calculateDelay returns the backoff duration before the next retry attempt.
// Uses exponential backoff capped at maxDelay, plus optional random jitter.
func calculateDelay(attempt int, base, max, jitter time.Duration, factor float64) time.Duration {
	delay := float64(base) * math.Pow(factor, float64(attempt))
	if delay > float64(max) {
		delay = float64(max)
	}
	if jitter > 0 {
		delay += float64(rng.Int63n(int64(jitter)))
	}
	return time.Duration(delay)
}

// RetryHandler automatically retries failed requests with configurable backoff.
// Retries HTTP 5xx errors and 408/429 by default; specific status codes can be configured.
// Non-HTTP errors (network, serialization) are not retried. T is the response type, E is the error type.
type RetryHandler[T any, E any] struct {
	nextHandler Handler[T, E]
}

// NewRetryHandler creates a new retry handler. Retry configuration is read from the
// request's Config on each call, allowing per-call overrides via RequestOption.
func NewRetryHandler[T any, E any]() *RetryHandler[T, E] {
	return &RetryHandler[T, E]{}
}

// shouldRetry determines if a failed request should be retried.
// Only HTTP errors on retryable methods with retryable status codes trigger a retry.
// Non-HTTP errors (network failures, serialization errors) are not retried.
func (h *RetryHandler[T, E]) shouldRetry(errResp *httptransport.ErrorResponse[E], method string, httpMethods []string, statusCodes []int) bool {
	if !errResp.IsHTTPError {
		return false
	}

	methodAllowed := false
	for _, m := range httpMethods {
		if m == method {
			methodAllowed = true
			break
		}
	}
	if !methodAllowed {
		return false
	}

	if len(statusCodes) > 0 {
		for _, code := range statusCodes {
			if code == errResp.StatusCode {
				return true
			}
		}
		return false
	}
	return errResp.StatusCode >= 500 || errResp.StatusCode == 408 || errResp.StatusCode == 429
}

// Handle processes a request with automatic retry logic on retryable HTTP failures.
// Uses exponential backoff with jitter between attempts. Returns the first successful response
// or the final error after all attempts are exhausted.
func (h *RetryHandler[T, E]) Handle(request httptransport.Request) (*httptransport.Response[T], *httptransport.ErrorResponse[E]) {
	if h.nextHandler == nil {
		return nil, httptransport.NewErrorResponse[E](errors.New("Handler chain terminated without terminating handler"), nil)
	}

	retryConfig := request.Config.Retry
	if retryConfig.MaxAttempts <= 0 {
		retryConfig.MaxAttempts = 1
	}
	for attempt := 0; attempt < retryConfig.MaxAttempts; attempt++ {
		resp, err := h.nextHandler.Handle(request.Clone())
		if err == nil {
			return resp, nil
		}

		if !h.shouldRetry(err, request.Method, retryConfig.HTTPMethodsToRetry, retryConfig.HTTPCodesToRetry) {
			return nil, err
		}

		if attempt == retryConfig.MaxAttempts-1 {
			return nil, err
		}

		time.Sleep(calculateDelay(attempt, retryConfig.RetryDelay, retryConfig.MaxDelay, retryConfig.RetryDelayJitter, retryConfig.BackOffFactor))
	}

	return nil, httptransport.NewErrorResponse[E](errors.New("max retries exceeded"), nil)
}

// HandleStream processes a streaming request with automatic retry logic on retryable HTTP failures.
// Retries failed stream connections with exponential backoff.
func (h *RetryHandler[T, E]) HandleStream(request httptransport.Request) (*httptransport.Stream[T], *httptransport.ErrorResponse[E]) {
	if h.nextHandler == nil {
		return nil, httptransport.NewErrorResponse[E](errors.New("Handler chain terminated without terminating handler"), nil)
	}

	retryConfig := request.Config.Retry
	if retryConfig.MaxAttempts <= 0 {
		retryConfig.MaxAttempts = 1
	}
	for attempt := 0; attempt < retryConfig.MaxAttempts; attempt++ {
		stream, err := h.nextHandler.HandleStream(request.Clone())
		if err == nil {
			return stream, nil
		}

		if !h.shouldRetry(err, request.Method, retryConfig.HTTPMethodsToRetry, retryConfig.HTTPCodesToRetry) {
			return nil, err
		}

		if attempt == retryConfig.MaxAttempts-1 {
			return nil, err
		}

		time.Sleep(calculateDelay(attempt, retryConfig.RetryDelay, retryConfig.MaxDelay, retryConfig.RetryDelayJitter, retryConfig.BackOffFactor))
	}

	return nil, httptransport.NewErrorResponse[E](errors.New("max retries exceeded"), nil)
}

// SetNext sets the next handler in the chain.
func (h *RetryHandler[T, E]) SetNext(handler Handler[T, E]) {
	h.nextHandler = handler
}
