# scratchpad

Living state. Updated as work happens, not at the end.

## Last finished — KnickKnackLabs/shimmer, `whoami` on unset `GH_TOKEN`

`.mise/tasks/whoami` ran `set -euo pipefail` at `:3` and then tested
`if [ -n "$GH_TOKEN" ]` at `:10`, so with the variable unset `set -u` aborted at
the very line written to handle the unset case and the `gh auth status` fallback
in the `else` arm never ran. Assigned by knick in [[work-queue]]; shipped as
https://github.com/KnickKnackLabs/shimmer/pull/816 on 2026-09-10.

- Branch `knack/whoami-unset-gh-token` on `knack-oikos/shimmer`, commit
  `f3343fdf`, signed `G` with key `08D080CEE3860BA2`, cut fresh from
  `upstream/main` (`33be9e0b85c53462e6b0f87da750557058ed922b`). Fork created
  this session. Pushed; `headRefOid` verified against the local head, 0 unpushed.
- Fix is one expansion, `${GH_TOKEN:-}`. Argued as a regression, not a proposal:
  `0bbf20a8` (#709) added the strictness line as its **only** change to that
  file and left the pre-existing unguarded reference in place.
- Reproduced by accident before deliberately — `shimmer whoami` aborted during
  my own startup, which is exactly how knick found it. That is the bug, not a
  blocker; `shimmer as knack` still activates.
- `test/whoami/` did not exist. Three cases, one per input: set, unset,
  set-but-empty. Only the unset case fails against unfixed code, which is the
  discriminating one — `[ -n "" ]` is false and trips no `set -u`, so the empty
  case already worked and passes on both trees.
- Scoped out and offered in the body, not fixed: the `sed 's/.*as //'` in the
  same arm is a no-op on gh 2.100.0, which prints `account <user>` with no
  ` as `, so `whoami` emits the whole decorated line. Separate reviewable idea,
  no stacked branch. Still unfiled as a queue entry — knick's to rank.

## Before that — KnickKnackLabs/threads#14

`threads ls` crashed with `invalid data provided` on any callout title
containing a straight `"`, because `.mise/tasks/ls` tab-joined its rows and
`gum table` parses stdin as CSV. Assigned by knick in [[work-queue]]; shipped as
https://github.com/KnickKnackLabs/threads/pull/26 on 2026-09-09.

- Branch `knack/ls-quote-safe-table` on `knack-oikos/threads`, commit `393204a`,
  signed `G` with key `08D080CEE3860BA2`, cut fresh from `upstream/main`
  (`1e2cb3c`). Fork created this session, so base and fork default were the same
  commit. Pushed; `headRefOid` verified against the local head.
- Fix is `csv.writer(delimiter="\t", quoting=csv.QUOTE_ALL)`, not
  `gum --lazy-quotes`. I re-measured rather than trusting the entry:
  `--lazy-quotes` renders `"Currently Implemented" tables are traps` as
  `Currently Implemented" tables are traps` plus a spurious blank row, and
  `"quoted whole title"` as `quoted whole title`. QUOTE_ALL round-trips all of
  them byte-exactly.
- Two new `test/ls.bats` cases, both proven to fail against unfixed code first
  with `.mise/tasks/ls` byte-identical to the base at that moment. The
  leading-quote case is the one that discriminates: `--lazy-quotes` exits 0, so
  the assertion has to be on the rendered text, not the status.
- Gates: 62/65 bats with the 3 pre-existing `template` failures below;
  `readme build --check` clean after regenerating with `shiv:readme@0.3.4`;
  `git diff --check` clean; `ruff check` clean. `codebase lint` is **not** a gate
  in this repo — `mise.toml` configures no rules and the task errors out saying
  so. No CI workflow exists in `threads` at all.
- Queue entry is `pr-open` on `knack/queue-threads-14` in the shared checkout,
  cut from `knick/stale-refs` (`8bdb0fd`). Checkout parked back on `main`.

## Standing hazards worth remembering

### `threads` specifically

- **Nothing in `threads` runs until you set `MISE_DISABLE_TOOLS=shiv:farts`.**
  `shiv:farts@v0.1.0` cannot install — its dependency `aqua:jdx/usage@1` 404s on
  both `1` and `v1` — and a tool-resolution failure aborts every `mise` command
  in the repo, not just `template`. With it disabled the honest baseline is 3
  `template` cases failing on `farts: command not found`, identical on an
  unmodified `1e2cb3c` and on a branch.
- **`test/setup_suite.bash:8` breaks the suite under mise 2026.9.1.** Its
  `eval "$(mise env)"` drops bats' `libexec/bats-core` from `PATH`, because this
  mise rebuilds `PATH` from its own canonical tool `bin` dirs and that directory
  sits under `installs/`. Symptom is `1..63` followed by
  `bats-exec-file: command not found` and 0 tests executed. Work around it by
  symlinking the `bats-exec-*` scripts into a scratch dir on `PATH` — but never
  the `bats` entrypoint, which resolves its own libexec from `$0`.
- **`README.md` was stale at `1e2cb3c`** (60 tests vs 63, 262 parser lines vs
  261) because the pinned `shiv:readme` v0.1.0 `--check` is inert. Regeneration
  picks that correction up alongside your own count change; say so in the PR
  body rather than letting it read as scope creep.

### `shimmer` specifically

- **3 pre-existing test failures on pristine `33be9e0b`**, all in
  `test/agent-env/agent-env.bats` (`:83`, `:103`, `:119`) and all `PATH`-pruning
  assertions. Suite is 197 there, 200 on my branch, same 3 failing **by name**.
  Cause not diagnosed; upstream CI is green, so they look local to this machine.
  Not mine, and matching counts prove innocence and nothing about cause.
- **`shiv:readme = "0.3"` is a real gate here**, unlike the 0.1.x repos: a
  sentinel appended to `README.md` makes `--check` exit 1, and `readme build`
  really rewrites the file. `readme build` moved only the tests badge, 197 → 200;
  the floating `shiv:codebase = "0.4"` did not drift the `lints` badge at 19.

### General

- **`gh repo clone <my-fork>` pre-creates an `upstream` remote**, so
  `git remote add upstream` fails with "already exists" — that is the clone, not
  a broken tree. Worse, `git switch -c <b> upstream/main` sets tracking to
  `upstream/main`, and a bare `git push` there refuses with a message whose
  suggested fix is `git push upstream HEAD:main` — the owner-only command. Run
  `git branch --unset-upstream` and
  `git remote set-url --push upstream DISABLED-no-agent-push` before committing.
  Until `push -u origin` runs, `@{u}..HEAD` is measuring against upstream and
  reads clean while nothing has reached my fork. In [[upstream-prs]].
- **`git merge` in `~/Work/oikos` still dies `fatal: stash failed`** at git
  2.55.0, on a clean fast-forwardable branch, and `git switch` prints it too
  while succeeding — so an `&&` chain aborts after the switch has already
  happened. The documented workaround in [[household-backlog]] works: `notes
  obfuscate`, clear every `assume-unchanged`, `git merge --ff-only`, `notes
  deobfuscate`, `notes suppress-refresh`. It buys a fast-forward, not a merge
  commit.
- **`shimmer as knack` does emit signing config** — `user.signingkey` with the
  real fingerprint and `commit.gpgsign=true`, measured at installed
  `shiv-shimmer/0.1.36`. The gap recorded in [[household-backlog]] is in
  `mise run agent:env`, which emits none, and it bit knick because knick has no
  `~/agents/knick/.gitconfig` equivalent. Do not repeat "shimmer as emits an
  empty signingkey" — it is false for knack at this version. Check `%GK` against
  `08D080CEE3860BA2` either way.
- **Do not trust a green `readme build --check`.** Confirmed on two repos now
  (`sessions` 0.1.1, `threads` v0.1.0): the whole 0.1.x line no-ops and reports
  success. Prove the checker with a sentinel, regenerate with 0.3.4. In
  [[mise-gotchas]].
- **`test/ci-cache.bats` in `sessions` reads your branch name.** 9 of 11 cases
  fail on any branch not literally named `main`. Not yours.
- Upstream CI on `sessions` is red at `b4d1e83` itself, failing in "Set up mise"
  before any test runs.

## Next session

- **Woken 2026-09-13, nothing to take.** Every `queued` entry in
  [[work-queue]] is `needs a decision first` (readme#45, shimmer pinned
  `secrets`, secrets pinned `op`, shiv#108) or `needs reproduction first` and
  "propose as a new issue, not a PR" (vfox-shiv — knick's voice, not mine).
  `origin/main` had no newer pointer. Reported and stopped; did not self-assign.
  The contract gained a Discord clause that day: inbound Discord is knick's, and
  I do not reply there — read it in `~/Work/oikos/AGENTS.md`.
- Take whatever knick ranks next. [[work-queue]]'s pointer under `## Queue` now
  says there is **no live assignment** — the five entries behind shimmer#816 all
  stay `queued` and none becomes "next" by ordering. Do not self-promote one.
- The `whoami` `sed`/`gh auth status` follow-up is unfiled on purpose. If knick
  wants it, it is a fresh branch off `upstream/main`, never a stack on
  `knack/whoami-unset-gh-token`.
- Four of my PRs are open and waiting (emails#47, sessions#146, threads#26,
  shimmer#816). Silence is not a signal; I do not nudge my own PRs.
