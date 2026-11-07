from __future__ import annotations
import argparse
from pathlib import Path
from .simulator import TransportWorld
from .benchmark import run_benchmark


def main():
    parser = argparse.ArgumentParser(prog="worldcast")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("simulate", "benchmark"):
        cmd = sub.add_parser(name)
        cmd.add_argument("--steps", type=int, default=1000)
        cmd.add_argument("--cities", type=int, default=20)
        cmd.add_argument("--seed", type=int, default=7)
    sim = sub.choices["simulate"]
    sim.add_argument("--out", type=Path, default=Path("data/world.csv"))
    args = parser.parse_args()
    frame = TransportWorld(cities=args.cities, seed=args.seed).run(args.steps)
    if args.command == "simulate":
        args.out.parent.mkdir(parents=True, exist_ok=True)
        frame.to_csv(args.out, index=False)
        print(f"Wrote {len(frame):,} rows to {args.out}")
    else:
        print(run_benchmark(frame).to_string(index=False))


if __name__ == "__main__":
    main()
