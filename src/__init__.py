"""Package initialization for :mod:`src`."""

__version__ = "0.1.0"

# Re-export the main components for convenience
from .agent import TutorAgent

__all__ = ["TutorAgent", "__version__"]
