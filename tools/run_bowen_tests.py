"""Run Bowen's backend tests and the existing arithmetic regressions."""
import argparse
from pathlib import Path
import shutil
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--iverilog", default=shutil.which("iverilog"))
    parser.add_argument("--vvp", default=shutil.which("vvp"))
    args = parser.parse_args()
    if not args.iverilog or not args.vvp:
        parser.error("put iverilog/vvp on PATH or pass their executable paths")
    root = Path(__file__).resolve().parents[1]
    build = root / "build"
    build.mkdir(exist_ok=True)
    sources = sorted(p for p in root.glob("*.v") if not p.name.endswith("_tb.v"))
    sources += sorted((root / "cache").glob("*.v"))
    failed = False
    for name in ("rs", "fp_rs", "fcsr", "hart_fp_commit", "fpu", "fpu_round", "alu", "decoder"):
        sim = build / (name + "_sim")
        cmd = [args.iverilog, "-g2005", "-s", name + "_tb", "-o", str(sim),
               str(root / (name + "_tb.v")), *map(str, sources)]
        compiled = subprocess.run(cmd, cwd=root, capture_output=True, text=True, timeout=60)
        output = compiled.stdout + compiled.stderr
        if compiled.returncode == 0:
            run = subprocess.run([args.vvp, "-n", str(sim)], cwd=build,
                                 capture_output=True, text=True, timeout=180)
            output += run.stdout + run.stderr
            ok = run.returncode == 0 and "ALL TESTS PASSED" in run.stdout
        else:
            ok = False
        (build / (name + ".log")).write_text(output, encoding="utf-8")
        tally = [line for line in output.splitlines() if "passed," in line and "failed" in line]
        print(f"{'PASS' if ok else 'FAIL'} {name}: {tally[-1] if tally else 'see build/' + name + '.log'}", flush=True)
        if not ok:
            print(output[-6000:])
        failed |= not ok
    # Elaborate the legacy shell too: it consumes the revised stateless FPU.
    check = subprocess.run([args.iverilog, "-g2005", "-s", "hart", "-o",
                            str(build / "hart_compile"), *map(str, sources)],
                           cwd=root, capture_output=True, text=True, timeout=60)
    print(f"{'PASS' if check.returncode == 0 else 'FAIL'} hart elaboration")
    if check.returncode:
        print(check.stdout + check.stderr)
    return int(failed or check.returncode != 0)


if __name__ == "__main__":
    sys.exit(main())
