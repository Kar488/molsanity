"""Generate the Colab full-run notebook as valid .ipynb JSON.

Kept as a script (not hand-written JSON) so the notebook is reproducible and the
source is diff-friendly. Run: ``python notebooks/make_notebook.py``.
"""
from __future__ import annotations

import json
from pathlib import Path

OWNER, REPO = "Kar488", "molsanity"
BRANCH = "claude/molsanity-scaffold-mutag-uayx7a"


def md(*lines: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": _join(lines)}


def code(*lines: str) -> dict:
    return {"cell_type": "code", "metadata": {}, "execution_count": None,
            "outputs": [], "source": _join(lines)}


def _join(lines):
    # nbformat wants each element newline-terminated except the last.
    out = []
    for i, ln in enumerate(lines):
        out.append(ln + ("\n" if i < len(lines) - 1 else ""))
    return out


cells = [
    md(
        "# MolSanity — full-scale audit run on a free Colab GPU\n",
        "\n",
        "Runs the complete `configs/full.yaml` sweep (150 epochs, 50 IG steps, 100 audited\n",
        "molecules/cell, scaffold **and** random splits) across every reachable dataset ×\n",
        "backbone × attributor — the publication-scale numbers the CPU dev box only\n",
        "approximated.\n",
        "\n",
        "### How to run\n",
        "1. **Runtime → Change runtime type → T4 GPU** (free tier is enough — the models are\n",
        "   ~43k params, <2 GB VRAM).\n",
        "2. **Runtime → Run all.**\n",
        "\n",
        "The pipeline is **resumable**: trained checkpoints + stage `.done` markers are\n",
        "reused, so if the Colab session drops, just re-run the *Run the sweep* cell and it\n",
        "continues where it left off (no retraining).\n",
        "\n",
        "Datasets needing the pre-2.5 PyG stack (ShapeGGen/GraphXAI) stay blocked-tolerant\n",
        "and are skipped + logged, never faked.",
    ),
    md("## 1. Verify the GPU"),
    code(
        "import torch, subprocess",
        "smi = subprocess.run(['nvidia-smi'], capture_output=True, text=True).stdout",
        "print(smi or 'nvidia-smi not found')",
        "if not torch.cuda.is_available():",
        "    raise SystemExit(",
        "        'No GPU detected. Set Runtime > Change runtime type > T4 GPU, then Run all.'",
        "    )",
        "print('CUDA:', torch.cuda.get_device_name(0), '| torch', torch.__version__)",
    ),
    md(
        "## 2. Clone the repo\n",
        "\n",
        "If the repository is **private**, create a GitHub personal access token (repo\n",
        "scope) and paste it into `GITHUB_TOKEN` below. Leave it blank for a public repo.",
    ),
    code(
        "import os, subprocess",
        "GITHUB_TOKEN = ''  # <- paste a token here only if the repo is private",
        f"OWNER, REPO, BRANCH = '{OWNER}', '{REPO}', '{BRANCH}'",
        "",
        "auth = f'{GITHUB_TOKEN}@' if GITHUB_TOKEN else ''",
        "url = f'https://{auth}github.com/{OWNER}/{REPO}.git'",
        "if not os.path.isdir(REPO):",
        "    subprocess.run(['git', 'clone', '--branch', BRANCH, '--depth', '1', url, REPO],",
        "                   check=True)",
        "os.chdir(REPO)",
        "print('cwd:', os.getcwd())",
        "subprocess.run(['git', 'log', '--oneline', '-1'])",
    ),
    md(
        "## 3. Install dependencies\n",
        "\n",
        "Colab ships a CUDA build of PyTorch; PyG (2.5+), RDKit, and Captum are pure-Python\n",
        "wheels that need no compiled extensions. PyTDC (for DILI/hERG/Tox21) is installed\n",
        "with a minimal footprint so it doesn't fight Colab's pinned numpy/pandas.",
    ),
    code(
        "%pip install -q torch-geometric rdkit captum pyyaml",
        "# Minimal PyTDC: avoid its heavy optional deps (transformers/scanpy/...).",
        "%pip install -q --no-deps PyTDC huggingface_hub httpx fuzzywuzzy",
        "print('deps installed')",
    ),
    code(
        "%pip install -q -e .",
        "print('molsanity installed (editable)')",
    ),
    md("## 4. Smoke check — imports + a real dataset load"),
    code(
        "import molsanity",
        "from molsanity.data.datasets import load_dataset",
        "ld = load_dataset('MUTAG')",
        "print('MUTAG:', len(ld.dataset), 'graphs — pipeline ready')",
    ),
    md(
        "## 5. Run the sweep\n",
        "\n",
        "This trains every backbone on the GPU and computes the full audit battery. On a\n",
        "free T4 expect roughly 1–2 hours. **Resumable** — re-run this cell if the session\n",
        "drops.",
    ),
    code(
        "import time, subprocess",
        "t0 = time.time()",
        "proc = subprocess.run(",
        "    ['python', '-m', 'molsanity.run_all', '--config', 'configs/full.yaml'],",
        "    text=True,",
        ")",
        "print(f'\\nfinished in {(time.time()-t0)/60:.1f} min (exit {proc.returncode})')",
    ),
    md("## 6. Results"),
    code(
        "from pathlib import Path",
        "for name in ['RESULTS.md', 'BENCHMARK.md']:",
        "    p = Path(name)",
        "    if p.exists():",
        "        print('=' * 80, '\\n', name, '\\n', '=' * 80)",
        "        print(p.read_text())",
    ),
    md(
        "## 7. Download the outputs\n",
        "\n",
        "Bundles the reports, run logs, checkpoints, and figures so you can pull the\n",
        "full-scale results (and the retrained GPU checkpoints) off Colab.",
    ),
    code(
        "import shutil, os",
        "shutil.make_archive('molsanity_full_run', 'zip', root_dir='.',",
        "                    base_dir=None)  # zips the repo tree",
        "# Trim to the artifacts that matter if the full zip is large:",
        "print('zip size (MB):', round(os.path.getsize('molsanity_full_run.zip')/1e6, 1))",
        "try:",
        "    from google.colab import files",
        "    files.download('molsanity_full_run.zip')",
        "except Exception as e:",
        "    print('Not on Colab or download blocked:', e)",
    ),
]

nb = {
    "cells": cells,
    "metadata": {
        "accelerator": "GPU",
        "colab": {"provenance": [], "toc_visible": True},
        "kernelspec": {"display_name": "Python 3", "name": "python3"},
        "language_info": {"name": "python"},
    },
    "nbformat": 4,
    "nbformat_minor": 0,
}

out = Path(__file__).with_name("molsanity_full_run_colab.ipynb")
out.write_text(json.dumps(nb, indent=1) + "\n")
print("wrote", out, "(", len(cells), "cells )")
