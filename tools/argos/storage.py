import os
from pathlib import Path

FALLBACK_RELATIVE_PATH = Path("data/raw/.staging")


def resolve_ssd_root():
    """Preferred SSD root: $ICONOCRACIA_SSD_ROOT > any mounted volume with corpus/imagens > None."""
    env_root = os.environ.get("ICONOCRACIA_SSD_ROOT")
    if env_root:
        return Path(env_root)
    for candidate in sorted(Path("/Volumes").glob("*/corpus/imagens")):
        if candidate.is_dir():
            return candidate
    return None


def resolve_storage_root(repo_root, ssd_root=None):
    """Resolve the preferred binary staging root and its storage tier."""

    repo_root = Path(repo_root)
    if ssd_root is None:
        ssd_root = resolve_ssd_root()

    if ssd_root and Path(ssd_root).is_dir():
        return Path(ssd_root), "ssd"

    fallback_root = repo_root / FALLBACK_RELATIVE_PATH
    fallback_root.mkdir(parents=True, exist_ok=True)
    return fallback_root, "repo-staging"
