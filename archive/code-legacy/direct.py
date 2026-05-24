from __future__ import annotations

import http.client
import ssl
import time
import urllib.error
import urllib.request
from pathlib import Path


USER_AGENT = "ARGOS/1.0 (+iconocracy-research; ana.vanzin@ufsc.br)"
MIN_VALID_BYTES = 500
SSL_UNVERIFIED = ssl.create_default_context()
SSL_UNVERIFIED.check_hostname = False
SSL_UNVERIFIED.verify_mode = ssl.CERT_NONE


def classify_http_failure(status_code: int) -> str:
    """Map HTTP failures to stable ARGOS labels."""

    if status_code == 403:
        return "403_block"
    if status_code == 404:
        return "404_not_found"
    if status_code == 408:
        return "408_timeout"
    if status_code == 410:
        return "410_gone"
    if status_code == 429:
        return "429_rate_limited"
    if 500 <= status_code <= 599:
        return "5xx_upstream"
    if 400 <= status_code <= 499:
        return f"{status_code}_client_error"
    return f"{status_code}_http_error"


def _build_result(dest_path: Path, **extra) -> dict:
    result = {
        "success": False,
        "protocol": "direct",
        "dest_path": str(dest_path),
        "bytes_written": 0,
        "status_code": None,
        "failure_class": None,
        "error": None,
        "notes": [],
        "ssl_verification": "verified",
    }
    result.update(extra)
    return result


def _retry_delay(error: urllib.error.HTTPError, attempt: int) -> float:
    retry_after = error.headers.get("Retry-After") if getattr(error, "headers", None) else None
    if retry_after:
        try:
            return max(float(retry_after), 0.0)
        except ValueError:
            pass
    if error.code == 429:
        return float((attempt + 1) * 5)
    return float(2 * (attempt + 1))


def _stream_to_path(response, dest_path: Path) -> int:
    total_size = 0
    with dest_path.open("wb") as handle:
        while True:
            chunk = response.read(65536)
            if not chunk:
                break
            handle.write(chunk)
            total_size += len(chunk)
    return total_size


def _is_retryable_http_error(status_code: int) -> bool:
    return status_code in {403, 408, 429} or 500 <= status_code <= 599


def _response_content_type(response) -> str | None:
    headers = getattr(response, "headers", None)
    if not headers:
        return None
    if hasattr(headers, "get_content_type"):
        content_type = headers.get_content_type()
        if content_type:
            return content_type.lower()
    content_type = headers.get("Content-Type")
    if not content_type:
        return None
    return content_type.split(";", 1)[0].strip().lower()


def _reject_unexpected_content_type(dest_path: Path, content_type: str | None, *, ssl_fallback_used: bool) -> dict | None:
    if not content_type:
        return None
    if content_type.startswith("image/") or content_type == "application/octet-stream":
        return None
    if "html" not in content_type and not content_type.startswith("text/"):
        return None

    dest_path.unlink(missing_ok=True)
    note = f"Rejected response with content-type {content_type}"
    if ssl_fallback_used:
        note = f"{note} after unverified SSL fallback"
    return _build_result(
        dest_path,
        error=f"Unexpected content type: {content_type}",
        failure_class="unexpected_content_type",
        notes=[note],
        ssl_verification="unverified" if ssl_fallback_used else "verified",
    )


def _finalize_success(dest_path: Path, total_size: int, *, ssl_fallback_used: bool, content_type: str | None) -> dict:
    unexpected_type = _reject_unexpected_content_type(
        dest_path,
        content_type,
        ssl_fallback_used=ssl_fallback_used,
    )
    if unexpected_type:
        return unexpected_type

    if total_size < MIN_VALID_BYTES:
        dest_path.unlink(missing_ok=True)
        notes = []
        if ssl_fallback_used:
            notes.append("Downloaded using unverified SSL fallback")
        return _build_result(
            dest_path,
            error=f"File too small ({total_size} bytes)",
            failure_class="content_too_small",
            notes=notes,
            ssl_verification="unverified" if ssl_fallback_used else "verified",
        )

    notes = []
    if ssl_fallback_used:
        notes.append("Downloaded using unverified SSL fallback")
    return _build_result(
        dest_path,
        success=True,
        bytes_written=total_size,
        notes=notes,
        ssl_verification="unverified" if ssl_fallback_used else "verified",
    )


def fetch_direct(url: str, dest_path: Path, timeout: int = 60, retries: int = 3) -> dict:
    """Fetch a direct image URL with lightweight retry and explicit SSL fallback metadata."""

    dest_path = Path(dest_path)
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "image/jpeg,image/png,image/*,*/*",
    }

    for attempt in range(retries):
        try:
            request = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(request, timeout=timeout) as response:
                content_type = _response_content_type(response)
                total_size = _stream_to_path(response, dest_path)

            return _finalize_success(dest_path, total_size, ssl_fallback_used=False, content_type=content_type)
        except urllib.error.HTTPError as error:
            if _is_retryable_http_error(error.code) and attempt < retries - 1:
                time.sleep(_retry_delay(error, attempt))
                continue
            dest_path.unlink(missing_ok=True)
            return _build_result(
                dest_path,
                status_code=error.code,
                failure_class=classify_http_failure(error.code),
                error=f"HTTP {error.code}: {error.reason}",
            )
        except ssl.SSLCertVerificationError:
            try:
                request = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(request, timeout=timeout, context=SSL_UNVERIFIED) as response:
                    content_type = _response_content_type(response)
                    total_size = _stream_to_path(response, dest_path)

                return _finalize_success(dest_path, total_size, ssl_fallback_used=True, content_type=content_type)
            except urllib.error.HTTPError as error:
                dest_path.unlink(missing_ok=True)
                return _build_result(
                    dest_path,
                    status_code=error.code,
                    failure_class=classify_http_failure(error.code),
                    error=f"SSL fallback HTTP {error.code}: {error.reason}",
                    notes=["Attempted unverified SSL fallback after certificate verification failure"],
                    ssl_verification="unverified",
                )
            except urllib.error.URLError as error:
                dest_path.unlink(missing_ok=True)
                return _build_result(
                    dest_path,
                    error=f"SSL fallback failed: {error.reason}",
                    failure_class="ssl_error",
                    notes=["Attempted unverified SSL fallback after certificate verification failure"],
                    ssl_verification="unverified",
                )
            except OSError as error:
                dest_path.unlink(missing_ok=True)
                return _build_result(
                    dest_path,
                    error=f"SSL fallback failed: {error}",
                    failure_class="ssl_error",
                    notes=["Attempted unverified SSL fallback after certificate verification failure"],
                    ssl_verification="unverified",
                )
        except http.client.IncompleteRead as error:
            if dest_path.exists():
                partial_size = dest_path.stat().st_size
                if partial_size > 10000:
                    return _build_result(dest_path, success=True, bytes_written=partial_size)
                dest_path.unlink(missing_ok=True)

            if attempt < retries - 1:
                time.sleep(3 * (attempt + 1))
                continue

            dest_path.unlink(missing_ok=True)
            return _build_result(dest_path, error=str(error), failure_class="request_error")
        except urllib.error.URLError as error:
            if attempt < retries - 1:
                time.sleep(3 * (attempt + 1))
                continue

            dest_path.unlink(missing_ok=True)
            reason = getattr(error, "reason", error)
            return _build_result(dest_path, error=str(reason), failure_class="request_error")
        except OSError as error:
            if attempt < retries - 1:
                time.sleep(3 * (attempt + 1))
                continue

            dest_path.unlink(missing_ok=True)
            return _build_result(dest_path, error=str(error), failure_class="request_error")

    dest_path.unlink(missing_ok=True)
    return _build_result(dest_path, error="Max retries exceeded", failure_class="retry_exhausted")
