from __future__ import annotations

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


def fetch_direct(url: str, dest_path: Path, timeout: int = 60, retries: int = 3) -> dict:
    """Fetch a direct image URL with lightweight retry and SSL fallback behavior."""

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
                total_size = _stream_to_path(response, dest_path)

            if total_size < MIN_VALID_BYTES:
                dest_path.unlink(missing_ok=True)
                return _build_result(
                    dest_path,
                    error=f"File too small ({total_size} bytes)",
                    failure_class="content_too_small",
                )

            return _build_result(dest_path, success=True, bytes_written=total_size)
        except urllib.error.HTTPError as error:
            if error.code in {403, 429} and attempt < retries - 1:
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
                    total_size = _stream_to_path(response, dest_path)

                if total_size < MIN_VALID_BYTES:
                    dest_path.unlink(missing_ok=True)
                    return _build_result(
                        dest_path,
                        error=f"File too small ({total_size} bytes)",
                        failure_class="content_too_small",
                    )

                return _build_result(dest_path, success=True, bytes_written=total_size)
            except Exception as error:
                dest_path.unlink(missing_ok=True)
                return _build_result(dest_path, error=f"SSL fallback failed: {error}", failure_class="ssl_error")
        except Exception as error:
            if "IncompleteRead" in str(error) and dest_path.exists():
                partial_size = dest_path.stat().st_size
                if partial_size > 10000:
                    return _build_result(dest_path, success=True, bytes_written=partial_size)
                dest_path.unlink(missing_ok=True)

            if attempt < retries - 1:
                time.sleep(3 * (attempt + 1))
                continue

            dest_path.unlink(missing_ok=True)
            return _build_result(dest_path, error=str(error), failure_class="request_error")

    dest_path.unlink(missing_ok=True)
    return _build_result(dest_path, error="Max retries exceeded", failure_class="retry_exhausted")
