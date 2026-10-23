# -*- coding: utf-8 -*-
"""Publish the Bellver guide everywhere in one go, so no site or clone can fall behind.

   python3 publish.py -m "What changed"     -> build + commit + push BOTH sites, then wait for GitHub to publish them
   python3 publish.py --build-only          -> build both sites locally (for a preview), no commit, no push

What it does, in order:
  1. checks both repositories are up to date with GitHub (stops if someone else pushed, so nothing is overwritten)
  2. builds musathegiant.com/cards/bellvercards (+ team pages there)          [python3 build.py]
  3. builds bellveraffiliates.com (MTG at the root + every clone at /<slug>/)  [BV_TARGET=bva python3 build.py]
  4. commits and pushes each repository that changed
  5. waits for GitHub Pages to finish both, and reports the result

Rule (MTG): only run the full publish after MTG approved the preview."""
import os, subprocess, sys, time, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
MTG_REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))                       # musathegiant
BVA_REPO = os.path.abspath(os.environ.get('BV_OUT', '/home/claude/bellveraffiliates'))  # bellveraffiliates
BVA_URL = 'https://github.com/mtglegacyai/bellveraffiliates'
REPOS = [('musathegiant.com', MTG_REPO, 'mtglegacyai/musathegiant', ['cards/bellvercards', 'bellvercards']),
         ('bellveraffiliates.com', BVA_REPO, 'mtglegacyai/bellveraffiliates', ['.'])]


def sh(cmd, cwd, env=None, check=True, quiet=False):
    r = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True)
    if check and r.returncode:
        raise SystemExit(f'FAILED in {cwd}: {" ".join(cmd)}\n{r.stdout[-2000:]}\n{r.stderr[-2000:]}')
    return r.stdout.strip()


def step(t):
    print(f'\n== {t}', flush=True)


def ensure_bva():
    if not os.path.isdir(os.path.join(BVA_REPO, '.git')):
        step('cloning bellveraffiliates (first run in this workspace)')
        sh(['git', 'clone', '--depth', '1', BVA_URL, BVA_REPO], cwd=os.path.dirname(BVA_REPO))


def up_to_date():
    step('1. checking both repositories are up to date')
    for name, repo, _, _ in REPOS:
        sh(['git', 'checkout', '-q', 'main'], repo)
        sh(['git', 'fetch', '-q', 'origin', 'main'], repo)
        behind = sh(['git', 'rev-list', '--count', 'HEAD..origin/main'], repo)
        if behind != '0':
            r = subprocess.run(['git', 'pull', '-q', '--rebase', 'origin', 'main'], cwd=repo, capture_output=True, text=True)
            if r.returncode:
                raise SystemExit(f'{name}: GitHub has {behind} newer commit(s) that clash with local changes. Resolve first, then publish again.')
            print(f'  {name}: pulled {behind} newer commit(s) from GitHub')
        else:
            print(f'  {name}: up to date')


def build():
    step('2. building musathegiant.com (MTG + team pages)')
    sh([sys.executable, 'build.py'], HERE)
    print('  done')
    step('3. building bellveraffiliates.com (MTG at the root + every clone)')
    env = dict(os.environ, BV_TARGET='bva', BV_OUT=BVA_REPO)
    sh([sys.executable, 'build.py'], HERE, env=env)
    sys.path.insert(0, HERE); import team
    clones = [m['slug'] for m in team.members('bva') if os.path.isfile(os.path.join(BVA_REPO, m['slug'], 'index.html'))]
    print(f'  done: {len(clones)} clone(s): ' + ', '.join(sorted(clones)))


def push(msg):
    pushed = []
    step('4. committing and pushing')
    for name, repo, gh, paths in REPOS:
        sh(['git', 'add', '-A', '--'] + paths, repo)
        if not sh(['git', 'status', '--porcelain', '--'] + paths, repo):
            print(f'  {name}: nothing changed'); continue
        sh(['git', 'commit', '-q', '-m', msg], repo)
        sha = sh(['git', 'rev-parse', 'HEAD'], repo)
        sh(['git', 'push', '-q', 'origin', 'main'], repo)
        print(f'  {name}: pushed {sha[:7]}'); pushed.append((name, gh, sha))
    return pushed


def wait(pushed):
    if not pushed:
        return
    step('5. waiting for GitHub Pages')
    left = dict((sha, (name, gh)) for name, gh, sha in pushed)
    t0 = time.time()
    while left and time.time() - t0 < 600:
        for sha, (name, gh) in list(left.items()):
            out = sh(['gh', 'run', 'list', '-R', gh, '-L', '5', '--json', 'status,conclusion,headSha',
                      '-q', f'.[] | select(.headSha=="{sha}") | "\\(.status) \\(.conclusion)"'], HERE, check=False)
            done = [l for l in out.splitlines() if l.startswith('completed')]
            if done:
                print(f'  {name}: {done[0].split()[1]}'); del left[sha]
        if left:
            time.sleep(10)
    for sha, (name, gh) in left.items():
        print(f'  {name}: still publishing after 10 minutes, check GitHub')


if __name__ == '__main__':
    a = argparse.ArgumentParser()
    a.add_argument('-m', '--message', help='commit message (required to publish)')
    a.add_argument('--build-only', action='store_true', help='build both sites locally, no commit or push')
    o = a.parse_args()
    if not o.build_only and not o.message:
        raise SystemExit('Give a commit message with -m, or use --build-only for a preview.')
    ensure_bva()
    up_to_date()
    build()
    if o.build_only:
        print('\nBuilt both sites locally. Nothing committed or pushed.')
    else:
        wait(push(o.message))
        print('\nPublished: musathegiant.com/cards/bellvercards and bellveraffiliates.com (with every clone).')
