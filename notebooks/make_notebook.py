"""Generate the Colab full-run notebook as valid .ipynb JSON.

Kept as a script (not hand-written JSON) so the notebook is reproducible and the
source is diff-friendly. Run: ``python notebooks/make_notebook.py``.
"""
from __future__ import annotations

import json
from pathlib import Path

OWNER, REPO = "Kar488", "molsanity"
BRANCH = "main"

# The keep-alive JS is assembled from a list so this file never has to nest
# triple-quoted strings inside the generated cell source.
KEEPALIVE_JS = [
    "  function keepAlive() {",
    "    const btn = document.querySelector('colab-connect-button');",
    "    if (btn) { btn.click(); console.log('keep-alive', new Date().toISOString()); }",
    "  }",
    "  if (window._molsanityKeepAlive) { clearInterval(window._molsanityKeepAlive); }",
    "  window._molsanityKeepAlive = setInterval(keepAlive, 60 * 1000);",
]


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
        "# MolSanity — full-scale audit run on a free Colab GPU",
        "",
        "Runs the complete `configs/full.yaml` sweep (150 epochs, 50 IG steps, 100",
        "audited molecules/cell, scaffold **and** random splits) across every reachable",
        "dataset × backbone × attributor — the publication-scale numbers the CPU dev box",
        "only approximated.",
        "",
        "### How to run",
        "1. **Runtime → Change runtime type → T4 GPU** (free tier is enough — the models",
        "   are ~43k params, <2 GB VRAM).",
        "2. **The repo is private** → paste a GitHub token into the clone cell (step 4).",
        "   Without it the clone fails and nothing downstream can work.",
        "3. **Runtime → Run all.**",
        "",
        "Steps 2 (keep-alive) and 3 (Drive) guard a long run against Colab disconnects.",
        "The pipeline is **resumable**: checkpoints and stage `.done` markers are reused,",
        "so after a drop you re-run the setup cells plus *Run the sweep* and it continues",
        "instead of retraining.",
    ),
    md("## 1. Verify the GPU"),
    code(
        "import subprocess",
        "",
        "import torch",
        "",
        "smi = subprocess.run(['nvidia-smi'], capture_output=True, text=True).stdout",
        "print(smi or 'nvidia-smi not found')",
        "if not torch.cuda.is_available():",
        "    raise SystemExit(",
        "        'No GPU detected. Set Runtime > Change runtime type > T4 GPU, then Run all.'",
        "    )",
        "print('CUDA:', torch.cuda.get_device_name(0), '| torch', torch.__version__)",
    ),
    md(
        "## 2. Keep the session alive",
        "",
        "Colab disconnects an *idle* runtime after ~90 minutes. This clicks the connect",
        "button on a timer so a long unattended run is not killed for inactivity.",
        "",
        "**What it does not do** — the honest limits:",
        "",
        "- it does **not** survive closing the browser tab (the JS dies with the page);",
        "- it does **not** extend Colab's hard max-runtime cap (~12 h on the free tier);",
        "- it does **not** stop Colab reclaiming a GPU when demand is high.",
        "",
        "So treat it as insurance against *idle* timeout only. The durable protection is",
        "step 3 (persist to Drive) plus the pipeline's resumability.",
    ),
    code(
        "from IPython.display import Javascript, display",
        "",
        "_js = '\\n'.join([",
        *[f"    {json.dumps(line)}," for line in KEEPALIVE_JS],
        "])",
        "display(Javascript(_js))",
        "print('Keep-alive armed — pings once a minute while this tab stays open.')",
    ),
    md(
        "## 3. (Recommended) Persist outputs to Google Drive",
        "",
        "If the runtime dies mid-sweep, anything under `/content` is gone. Working inside",
        "Drive means trained checkpoints survive, so a re-run **resumes** rather than",
        "retraining from scratch. Set `USE_DRIVE = False` for a throwaway run.",
    ),
    code(
        "USE_DRIVE = True",
        "",
        "import os",
        "",
        "WORKDIR = '/content'",
        "if USE_DRIVE:",
        "    try:",
        "        from google.colab import drive",
        "",
        "        drive.mount('/content/drive')",
        "        WORKDIR = '/content/drive/MyDrive/molsanity_runs'",
        "        os.makedirs(WORKDIR, exist_ok=True)",
        "    except Exception as exc:",
        "        print('Drive unavailable, falling back to ephemeral /content:', exc)",
        "        WORKDIR = '/content'",
        "os.chdir(WORKDIR)",
        "print('working directory:', os.getcwd())",
    ),
    md(
        "## 4. Clone the repo",
        "",
        f"`{OWNER}/{REPO}` is **private**, so a GitHub personal access token with `repo`",
        "scope is required — create one at <https://github.com/settings/tokens>.",
        "",
        "If the clone fails this cell now raises immediately. An earlier version of this",
        "notebook carried on regardless, which is how a run once ended up packaging",
        "Colab's stock `/content` folder instead of any results.",
    ),
    code(
        "import os",
        "import subprocess",
        "",
        "GITHUB_TOKEN = ''  # <- REQUIRED: this repo is private",
        f"OWNER, REPO, BRANCH = {OWNER!r}, {REPO!r}, {BRANCH!r}",
        "",
        "if not GITHUB_TOKEN:",
        "    raise SystemExit(",
        "        'GITHUB_TOKEN is empty and the repo is private, so the clone would fail. '",
        "        'Create a token (repo scope) at https://github.com/settings/tokens, '",
        "        'paste it above, and re-run this cell.'",
        "    )",
        "",
        "url = f'https://{GITHUB_TOKEN}@github.com/{OWNER}/{REPO}.git'",
        "if not os.path.isdir(REPO):",
        "    r = subprocess.run(",
        "        ['git', 'clone', '--branch', BRANCH, '--depth', '1', url, REPO],",
        "        capture_output=True, text=True,",
        "    )",
        "    if r.returncode != 0:",
        "        # Scrub the token before showing git's error.",
        "        raise SystemExit('git clone failed:\\n' + r.stderr.replace(GITHUB_TOKEN, '***'))",
        "os.chdir(REPO)",
        "",
        "# Assert we really are in the repo before anything downstream runs.",
        "for marker in ('molsanity', 'configs/full.yaml'):",
        "    if not os.path.exists(marker):",
        "        raise SystemExit(f'Not at the repo root — missing {marker!r} in {os.getcwd()}')",
        "REPO_DIR = os.getcwd()",
        "print('repo:', REPO_DIR)",
        "subprocess.run(['git', 'log', '--oneline', '-1'])",
    ),
    md(
        "## 5. Install dependencies",
        "",
        "Colab ships a CUDA build of PyTorch; PyG (2.5+), RDKit, and Captum are",
        "pure-Python wheels that need no compiled extensions. PyTDC (for DILI / hERG /",
        "Tox21) is installed with a minimal footprint so it does not fight Colab's pinned",
        "numpy/pandas.",
    ),
    code(
        "%pip install -q torch-geometric rdkit captum pyyaml",
        "# Minimal PyTDC: skip its heavy optional deps (transformers/scanpy/...).",
        "%pip install -q --no-deps PyTDC huggingface_hub httpx fuzzywuzzy",
        "print('deps installed')",
    ),
    code(
        "%pip install -q -e .",
        "print('molsanity installed (editable)')",
    ),
    md("## 6. Smoke check — imports plus a real dataset load"),
    code(
        "import molsanity  # noqa: F401",
        "from molsanity.data.datasets import load_dataset",
        "",
        "ld = load_dataset('MUTAG')",
        "print('MUTAG:', len(ld.dataset), 'graphs — pipeline ready')",
    ),
    md(
        "## 7. Run the sweep",
        "",
        "Trains every backbone on the GPU and computes the full audit battery. On a free",
        "T4 expect roughly 1–2 hours. **Resumable** — if the session drops, re-run the",
        "setup cells and then this one; finished work is skipped.",
    ),
    code(
        "import os",
        "import subprocess",
        "import time",
        "",
        "os.chdir(REPO_DIR)  # guard: never run the sweep from the wrong directory",
        "t0 = time.time()",
        "proc = subprocess.run(",
        "    ['python', '-m', 'molsanity.run_all', '--config', 'configs/full.yaml'],",
        "    text=True,",
        ")",
        "print(f'\\nfinished in {(time.time() - t0) / 60:.1f} min (exit {proc.returncode})')",
    ),
    md("## 8. Results"),
    code(
        "from pathlib import Path",
        "",
        "for name in ['RESULTS.md', 'BENCHMARK.md', 'BENCHMARK_GT.md']:",
        "    p = Path(name)",
        "    if p.exists():",
        "        print('=' * 80, '\\n', name, '\\n', '=' * 80)",
        "        print(p.read_text())",
    ),
    md(
        "## 9. Download the results",
        "",
        "Packages **only the run outputs** — reports, figures, checkpoints, audit records,",
        "logs — into a zip written *outside* the staged tree, so the archive can never",
        "contain itself. It refuses to build an archive when the expected outputs are",
        "missing, rather than handing back a plausible-looking but empty zip.",
    ),
    code(
        "import os",
        "import shutil",
        "from pathlib import Path",
        "",
        "os.chdir(REPO_DIR)",
        "STAGE = Path('/content/_molsanity_out')",
        "ZIP_BASE = '/content/molsanity_full_run'  # outside STAGE, so it can't self-include",
        "",
        "WANTED = [",
        "    'RESULTS.md', 'BENCHMARK.md', 'BENCHMARK_GT.md', 'BENCHMARK_GT.json',",
        "    'PROGRESS.md', 'LIMITATIONS.md', 'figures', 'logs',",
        "    'artifacts/checkpoints', 'artifacts/audit', 'artifacts/run_manifest.json',",
        "]",
        "",
        "if STAGE.exists():",
        "    shutil.rmtree(STAGE)",
        "STAGE.mkdir(parents=True)",
        "",
        "copied = []",
        "for rel in WANTED:",
        "    src = Path(rel)",
        "    if not src.exists():",
        "        continue",
        "    dest = STAGE / rel",
        "    dest.parent.mkdir(parents=True, exist_ok=True)",
        "    shutil.copytree(src, dest) if src.is_dir() else shutil.copy2(src, dest)",
        "    copied.append(rel)",
        "",
        "if not any(c in copied for c in ('RESULTS.md', 'figures')):",
        "    raise SystemExit(",
        "        'No run outputs found to package — the sweep produced nothing. '",
        "        f'cwd={os.getcwd()}, found={copied}. Fix the run before downloading.'",
        "    )",
        "",
        "zip_path = shutil.make_archive(ZIP_BASE, 'zip', root_dir=STAGE)",
        "print('packaged:', copied)",
        "print('zip:', zip_path, f'({os.path.getsize(zip_path) / 1e6:.1f} MB)')",
        "",
        "try:",
        "    from google.colab import files",
        "",
        "    files.download(zip_path)",
        "except Exception as exc:",
        "    print('Not on Colab or download blocked — grab it from the file browser:', exc)",
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
