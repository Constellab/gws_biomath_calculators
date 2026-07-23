# Dependencies

This document lists the dependencies of the `gws_biomath_calculators` brick: the Constellab bricks it requires, and the external Python packages used by its tasks.

## Constellab bricks

Declared in [`settings.json`](./settings.json):

| Brick | Version |
|---|---|
| `gws_core` | >= 0.20.7 |

## Python packages (pip)

`settings.json` declares no pip packages. In practice, one task imports an external library that isn't declared anywhere:

| Package | Used by | Status |
|---|---|---|
| `plotly` | `biomath_calcul/gc_content_calculator/_gc_content_calculator.py` | **Not declared in `settings.json`** — required at runtime but missing from the dependency manifest |

## Known issues found while documenting

- `biomath_calcul/ligation_molar_ratio/ligation_molar_ratio.py` imports `MSAVisShellProxyHelper` from `gws_omix.base_env.msaviz_env_task` — `gws_omix` is not declared as a dependency of this brick anywhere in `settings.json`. This looks like a leftover/stray import (possibly copy-pasted) rather than an intentional cross-brick dependency; worth checking whether it's actually used by the task.
