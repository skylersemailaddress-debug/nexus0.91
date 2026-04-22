from __future__ import annotations

import argparse

from .interactive_shell import run_shell


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="nexus",
        description="Launch Nexus standalone product shell.",
    )
    parser.add_argument("--developer", action="store_true", help="Enable developer mode output")
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    mode = "developer" if args.developer else "product"
    print(f"[Nexus] Starting interactive shell in {mode} mode")

    run_shell(mode=mode)


if __name__ == "__main__":
    main()
