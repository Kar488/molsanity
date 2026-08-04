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
# rsync, not rmtree+copytree. The first version copied all ~1683 files every
# time; over the Drive FUSE mount that ran past 12 minutes with no output, and
# ~1500 of those files were already byte-identical in the fresh clone. rsync
# skips them on size+mtime and copies only what the run actually added.
#
# Two passes, small things first, so the science is on GitHub in under a minute
# and the 400 MB of checkpoints follow rather than block.
local = repo / 'results'
local.mkdir(parents=True, exist_ok=True)

if not DRIVE_RESULTS.is_dir():
    print('WARNING: no Drive mirror found; pushing whatever results/ is on disk')
else:
    def rsync(extra, label):
        print(f'  syncing {label} ...', flush=True)
        r = subprocess.run(
            ['rsync', '-a', '--no-perms', '--no-owner', '--no-group',
             '--stats', *extra, f'{DRIVE_RESULTS}/', f'{local}/'],
            capture_output=True, text=True)
        if r.returncode != 0:
            print('    rsync failed, falling back to a plain copy:',
                  (r.stderr or '').strip()[:200])
            for src in DRIVE_RESULTS.rglob('*'):
                if not src.is_file():
                    continue
                dst = local / src.relative_to(DRIVE_RESULTS)
                if dst.exists() and dst.stat().st_size == src.stat().st_size:
                    continue
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
            return
        for line in (r.stdout or '').splitlines():
            if 'Number of regular files transferred' in line or 'Total transferred' in line:
                print('   ', line.strip())

    # Reports, audit records, figures, logs: small, and the only part the
    # analysis needs. Checkpoints are provenance and can lag by a minute.
    rsync(['--exclude', 'artifacts/checkpoints/'], 'reports, audit records, figures')

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
    # Checkpoints last: heavy, and nothing downstream is blocked on them.
    if DRIVE_RESULTS.is_dir() and r.returncode == 0:
        print('\nsyncing checkpoints (this is the slow part; the science is'
              ' already pushed) ...', flush=True)
        rsync([], 'checkpoints')
        git('add', '-A', 'results')
        if git('diff', '--cached', '--quiet', check=False).returncode:
            git('commit', '-m', 'Checkpoints from the Colab sweep')
            r2 = git('push', 'origin', f'HEAD:{BRANCH}', check=False)
            print(scrub(r2.stdout + r2.stderr))
            print('CHECKPOINTS PUSHED' if r2.returncode == 0 else 'checkpoint push failed')
finally:
    git('remote', 'set-url', 'origin', origin)  # never leave the token in .git/config
