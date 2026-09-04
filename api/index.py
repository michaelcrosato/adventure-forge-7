"""Vercel Serverless Function entry point for AdventureForge."""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure the repository root is in sys.path so modules like adventure_forge and app are importable
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app import app  # noqa: E402

__all__ = ["app"]
