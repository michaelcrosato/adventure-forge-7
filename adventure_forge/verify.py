"""Top-level verification entrypoint forwarding to the verification bar.

Enables canonical execution via:
    python3 -m adventure_forge.verify
"""
from adventure_forge.verification.verify import main, run_all_verification

__all__ = ["main", "run_all_verification"]

if __name__ == "__main__":
    main()
