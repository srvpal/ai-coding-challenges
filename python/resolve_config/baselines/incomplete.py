"""Baseline that handles layer precedence but omits two specification rules."""


def resolve_config(base, environment, overrides, protected_keys):
    result = dict(base)
    result.update(environment)
    result.update(overrides)
    return dict(sorted(result.items()))
