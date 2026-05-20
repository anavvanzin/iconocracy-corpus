from pathlib import Path


DEFAULT_SSD_ROOT = Path("/Volumes/ICONOCRACIA/corpus/imagens")
FALLBACK_RELATIVE_PATH = Path("data/raw/.staging")


def resolve_storage_root(repo_root, ssd_root=DEFAULT_SSD_ROOT):
    """Resolve the preferred binary staging root and its storage tier."""

    repo_root = Path(repo_root)
    ssd_root = Path(ssd_root)

    if ssd_root.is_dir():
        return ssd_root, "ssd"

    fallback_root = repo_root / FALLBACK_RELATIVE_PATH
    fallback_root.mkdir(parents=True, exist_ok=True)
    return fallback_root, "repo-staging"
