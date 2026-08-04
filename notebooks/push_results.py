"""Recover-and-push: get results/ onto GitHub when the run finished but the
push did not.

Written to be pasted into a fresh Colab cell. It assumes nothing about the
notebook's Python state -- the failure it exists for is a kernel restart, which
wipes REPO_DIR and every other variable while leaving the files alone. It finds
the repo, restores results/ from the Drive mirror if the local copy is gone,
and pushes.

The token comes from Colab Secrets, never from this file.
"""
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

OWNER, REPO, BRANCH = 'Kar488', 'molsanity', 'main'
DRIVE_RESULTS = Path('/content/drive/MyDrive/molsanity_runs/results')

# --- 1. Drive, for the mirrored results ------------------------------------
if not Path('/content/drive/MyDrive').exists():
    from google.colab import drive
    drive.mount('/content/drive')

# --- 2. Find the repo, or clone it fresh -----------------------------------
# Local disk only. A clone on Drive is worse than no clone: Drive is a FUSE
# mount whose caching breaks git's bookkeeping ('fatal: shallow file has
# changed since we read it'), and copying results/ into it is a Drive-to-Drive
# copy of ~1700 files. The first version of this script searched all of
# /content, found a stale Drive-hosted clone, and started down exactly that
# path. Cloning fresh to local disk costs seconds.
candidates = [q.parent for q in Path('/content').glob('*/.git')
              if q.is_dir() and q.parent.name == REPO]
repo = candidates[0] if candidates else None
if repo:
    print(f'found local clone: {repo}')
else:
    repo = Path('/content') / REPO
    if repo.exists():
        shutil.rmtree(repo)
    print(f'cloning fresh to local disk: {repo}')
    subprocess.run(['git', 'clone', '--branch', BRANCH,
                    f'https://github.com/{OWNER}/{REPO}.git', str(repo)], check=True)
assert not str(repo).startswith('/content/drive'), (
    f'refusing to run git in a Drive-hosted repo: {repo}')
os.chdir(repo)

# --- 3. results/ must be the run's, not the repo's stale copy --------------
local = repo / 'results'
if DRIVE_RESULTS.is_dir():
    n_drive = sum(1 for _ in DRIVE_RESULTS.rglob('*') if _.is_file())
    n_local = sum(1 for _ in local.rglob('*') if _.is_file()) if local.is_dir() else 0
    print(f'Drive mirror: {n_drive} files   local results/: {n_local} files')
    if n_drive > n_local:
        print('restoring results/ from the Drive mirror')
        if local.is_dir():
            shutil.rmtree(local)
        shutil.copytree(DRIVE_RESULTS, local)
else:
    print('WARNING: no Drive mirror found; pushing whatever results/ is on disk')

# --- 4. Token, from Secrets only ------------------------------------------
GH_TOKEN = None
try:
    from google.colab import userdata
    GH_TOKEN = userdata.get('GH_TOKEN')
except Exception as exc:  # noqa: BLE001
    raise SystemExit(
        f'no usable GH_TOKEN in Colab Secrets ({exc}).\n'
        '  - the browser tab must be OPEN AND FOCUSED when this runs\n'
        '  - the key icon in the sidebar must show GH_TOKEN with\n'
        '    "Notebook access" toggled ON for THIS notebook\n'
        'results/ is restored locally, so re-running this cell is all that is left.')


def scrub(text):
    text = text.replace(GH_TOKEN, '***') if GH_TOKEN else text
    return re.sub(r'(gh[pousr]_|github_pat_)[A-Za-z0-9_]+', r'\1***', text or '')


def git(*args, check=True):
    r = subprocess.run(['git', *args], capture_output=True, text=True)
    if check and r.returncode != 0:
        raise SystemExit('git ' + ' '.join(args) + ' failed:\n' + scrub(r.stderr or r.stdout))
    return r


# --- 5. Commit and push ---------------------------------------------------
git('config', 'user.email', 'colab@molsanity.local')
git('config', 'user.name', 'MolSanity Colab run')
git('add', '-A', 'results')
if not git('diff', '--cached', '--quiet', check=False).returncode:
    print('nothing to commit -- results/ already matches the repo')
else:
    n_rows = 0
    rp = repo / 'results' / 'RESULTS.md'
    if rp.exists():
        n_rows = sum(1 for line in rp.read_text().splitlines()
                     if line.startswith('|') and not line.startswith('| ---')) - 2
    git('commit', '-m', f'Results from the Colab sweep ({n_rows} audited rows)')

origin = git('remote', 'get-url', 'origin').stdout.strip()
auth = re.sub(r'^https://([^@]*@)?', f'https://{GH_TOKEN}@', origin)
git('remote', 'set-url', 'origin', auth)
try:
    git('fetch', 'origin', BRANCH, check=False)
    git('rebase', f'origin/{BRANCH}', check=False)
    r = git('push', 'origin', f'HEAD:{BRANCH}', check=False)
    print(scrub(r.stdout + r.stderr))
    print('PUSHED' if r.returncode == 0 else 'PUSH FAILED -- see above')
finally:
    git('remote', 'set-url', 'origin', origin)  # never leave the token in .git/config
