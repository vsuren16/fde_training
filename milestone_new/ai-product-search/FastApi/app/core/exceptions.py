class ResourceNotFoundError(Exception):
    """Raised when a requested resource does not exist."""


class RecommendationUnavailableError(Exception):
    """Raised when recommendation path cannot provide semantic output."""
