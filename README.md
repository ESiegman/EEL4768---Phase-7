# EEL4768---Phase-7
[![CI](https://github.com/ESiegman/EEL4768---Phase-7/actions/workflows/ci.yml/badge.svg)](https://github.com/ESiegman/EEL4768---Phase-7/actions/workflows/ci.yml)

An out-of-order (Tomasulo-style) RV32I hart with the M and F extensions. The
assignment is [documentation/phase_7.pdf](documentation/phase_7.pdf), and the
LSU interface is described in [docs/lsu_interface.md](docs/lsu_interface.md).

`make test` runs every testbench, the `ece552` rule checker and the formal
check, and writes a summary to `results/local.txt`. Logs go to `build/`.
`make help` lists the other targets.

## Tools

- **Icarus Verilog** (`iverilog`, `vvp`): required. `brew install icarus-verilog`,
  `apt install iverilog`, or `conda env create -f environment.yaml`.
- **Rule checker** (`ece552`): `pip install ./lint`. Use Python 3.10 to 3.13;
  its `pyslang==9.1.0` dependency has no wheel for 3.14. CI uses 3.12.
- **Formal** (`sby`): the OSS CAD Suite on PATH, as in phase_7.pdf 6.3. CI pins
  the 2026-10-22 release.

A missing rule checker or `sby` shows as SKIP, not FAIL. CI installs all
three, so its run is the full check.
