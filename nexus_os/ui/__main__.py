from __future__ import annotations

from nexus_os.product.interactive_shell import run_shell


def main() -> None:
    print("[Nexus UI] Runtime-backed UI starting")
    print("Commands: pin <section>, unpin <section>, hover <section>, mode <mode>, palette")
    run_shell()


if __name__ == "__main__":
    main()
