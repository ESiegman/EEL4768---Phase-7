# EEL4768---Phase-7
[![CI](https://github.com/ESiegman/EEL4768---Phase-7/actions/workflows/ci.yml/badge.svg)](https://github.com/ESiegman/EEL4768---Phase-7/actions/workflows/ci.yml)

Bowen's integer/FP reservation stations, dual FPU execution, and commit-time
FP CSR interfaces are documented in [documentation/bowen_backend.md](documentation/bowen_backend.md).

Run their tests and arithmetic regressions with `python tools/run_bowen_tests.py`
(Icarus Verilog and `vvp` on PATH), or run `make test` for all written testbenches.
