"""Utility helpers for logging and reproducibility."""

import logging

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

__all__ = ["logging"]
