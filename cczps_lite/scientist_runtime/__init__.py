"""Minimum supervised human-AI scientist interaction runtime.

This package is deliberately local, tiny-synthetic, deterministic and
non-scientific.  It exercises ClimateOS governance objects; it does not model
or describe an environmental system.
"""

from .runtime import ScientistRuntime, RuntimeBoundaryError, RuntimeStateError

__all__ = ["ScientistRuntime", "RuntimeBoundaryError", "RuntimeStateError"]
