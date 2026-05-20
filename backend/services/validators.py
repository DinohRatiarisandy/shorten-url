from urllib.parse import urlparse


def is_valid_url(url: str) -> bool:
    """Vérifie si une URL est valide (format de base)."""
    try:
        result = urlparse(url)
        return all([result.scheme in ["http", "https"], result.netloc])
    except Exception:
        return False
