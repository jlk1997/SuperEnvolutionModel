# -*- coding: utf-8 -*-
"""蚁算 product CLI: capture -> OCR -> office -> evidence (C115 hardened).
  python scripts/ant_capture_office.py [--outdir PATH] [--no-vl] [--dry-run]
  [--expected-paid N] [--lines-file PATH] [--title STR]
"""
from scripts.ant_capture_office_lib import main
if __name__ == "__main__":
    raise SystemExit(main())
