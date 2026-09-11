"""Reference implementation for the resolve-config challenge."""

from __future__ import annotations

from copy import deepcopy
from typing import Any


def resolve_config(
    base: dict[str, Any],
    environment: dict[str, Any],
    overrides: dict[str, Any],
    protected_keys: list[str],
) -> dict[str, Any]:
    """Resolve configuration layers into a sorted, detached dictionary."""
    layers = {"base": base, "environment": environment, "overrides": overrides}
    for name, layer in layers.items():
        if not isinstance(layer, dict):
            raise ValueError(f"{name} must be a dictionary")
        if any(not isinstance(key, str) or not key for key in layer):
            raise ValueError(f"{name} keys must be non-empty strings")

    if not isinstance(protected_keys, list) or any(
        not isinstance(key, str) or not key for key in protected_keys
    ):
        raise ValueError("protected_keys must be a list of non-empty strings")
    if len(protected_keys) != len(set(protected_keys)):
        raise ValueError("protected_keys must not contain duplicates")

    protected = set(protected_keys)
    attempted = protected & (environment.keys() | overrides.keys())
    if attempted:
        raise ValueError(f"protected keys cannot be overridden: {sorted(attempted)}")

    resolved = deepcopy(base)
    for layer in (environment, overrides):
        for key, value in layer.items():
            if value is None:
                resolved.pop(key, None)
            else:
                resolved[key] = deepcopy(value)

    return {key: resolved[key] for key in sorted(resolved)}
