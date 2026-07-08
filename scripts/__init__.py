"""Marks scripts/ as a real package so ``from scripts.run_ablations import ...``
resolves to this directory. Without it, an unrelated regular ``scripts`` package
in site-packages shadows this namespace directory during pytest's import scan
(PEP 420: a regular package elsewhere on sys.path beats a namespace portion),
breaking test_ablation_self_consistency.py. Scripts are still invoked in script
mode (``python scripts/foo.py``), which this does not affect."""
