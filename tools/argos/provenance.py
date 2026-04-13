from datetime import datetime, timezone
from urllib.parse import urlparse


def _utc_timestamp():
    return datetime.now(timezone.utc).replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")


def _source_domain(source_url):
    if not source_url:
        return None
    return urlparse(source_url).netloc.lower() or None


def build_provenance(
    *,
    fetched_by,
    protocol,
    storage_tier,
    source_url=None,
    record_id=None,
    extra_metadata=None,
):
    """Build a normalized provenance payload for ARGOS fetch operations."""

    metadata = {
        "source_url": source_url,
        "source_domain": _source_domain(source_url),
        "record_id": record_id,
    }
    if extra_metadata:
        metadata.update(extra_metadata)

    metadata = {key: value for key, value in metadata.items() if value is not None}

    return {
        "fetched_at": _utc_timestamp(),
        "fetched_by": fetched_by,
        "protocol": protocol,
        "storage_tier": storage_tier,
        "metadata": metadata,
    }
