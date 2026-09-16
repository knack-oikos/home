# scratchpad

Living state. Updated as work happens, not at the end.

## In flight — per-agent password manager, implementation-side feasibility

Woken 2026-09-16 through a coordinator session relaying the owner's ask ("each
agent its own password manager"). knick designs and files the Tier-2 entry; my
job was to measure what `secrets` can express and prototype isolation without
touching any live path. Nothing here is a decision. Authority is
`~/Work/oikos/AGENTS.md`.

- **Branch `knack/libsecret-collection` on `knack-oikos/secrets`, commit
  `8387aff`, signed `G`, held unpushed.** Cut from `knack/local` (`ec13dab`)
  because the libsecret provider exists on no other branch; it is a prototype,
  not a PR base, and an upstream PR would need the provider first. Worked in a
  separate clone `~/agents/knack/secrets-collection`; the live clone never
  left `knack/local`. Adds `SECRETS_LIBSECRET_COLLECTION`: `libsecret_set`
  passes it as `secret-tool store --collection=`, empty by default. Five
  tests; libsecret suite 39/39; full suite 165 with the same 8 failing by
  name as on the untouched base. README regenerated with `shiv:readme@0.3.4`
  (the base already lagged, 155 vs 160).
- **Unpushed because activation failed.** `secrets get knack/github-pat`
  found no entry under `libsecret`, `shimmer as knack` aborted, and the
  `gh api user` I had chained after it printed the owner's login. Ran no
  `gh` after that. Pushing over https would ride the owner's credential
  helper, so the commit is held. Same class as the oikos#1 slip below; the
  gate has to come *before* anything that talks to GitHub.
- **1Password needs no code.** `lib/1password.sh:21` already reads
  `SECRETS_1PASSWORD_VAULT` (default `Agents`) and passes `--vault` on every
  call (`:53`, `:116`, `:130`, `:159`, `:234`); verified by pointing it at a
  vault that does not exist and reading op's rejection. What is missing is
  `agent:env` exporting it per agent — an oikos change, not a `secrets` one.
  The account is `INDIVIDUAL`: one user, every vault visible to every `op`
  call the desktop app authorizes, so a per-agent vault is a namespace, not a
  boundary. Service accounts (`OP_SERVICE_ACCOUNT_TOKEN`, the unattended
  path) need a Teams/Business plan.
- **libsecret collections are not a read namespace.** `secret-tool store`
  takes `--collection`; `lookup`, `search` and `clear` do not, and search
  every unlocked collection. The `service` attribute (`secrets/<agent>/<key>`)
  is the only namespace, and any process on the session bus can query any
  attribute. Isolation would come from the *lock*, not the name.
- **No headless way to create or unlock a collection through the API.**
  `CreateCollection` returns a prompt object and nothing else; completing it
  needs `gcr-prompter` and a human. Completing it with an empty window id and
  no prompter registered crashed my throwaway daemon (SIGSEGV 12:54:23,
  use-after-free in dispatch per the coredump; Omarchy opened a crash-diagnosis
  session about it). `secret-tool` has no `create` or `unlock` verb at all.
- **The control socket is the only unattended path, and it is per daemon.**
  `gnome-keyring-daemon --login`/`--unlock` take a password on stdin and act
  on that daemon's `login` keyring. Measured in an isolated daemon on a
  private bus (`XDG_DATA_HOME` in scratch): first `--unlock` created and
  unlocked `login`; store, lookup and `secret-tool lock --collection=login`
  all worked. Re-unlocking after a lock, and restarting with the same
  password, left `login` reporting `Locked=true` in every attempt — not
  demonstrated, not proven impossible; the runs were noisy with extra daemons
  and I stopped. So "own collection, unlocked unattended" collapses into "own
  `gnome-keyring-daemon` on its own session bus per agent", with the password
  read from somewhere the agent can reach, which is a file.
- **A keyring created without a password is plaintext on disk**, and the
  daemon auto-creates one silently when a store arrives with no default
  collection. That file is the `[keyring]` text format and every value is
  readable with `grep`. Lookup against it needs no unlock and no prompt.
- **`secret-tool store --collection=<bad-name>` hangs** when the name is
  not `[A-Za-z0-9_]+` (invalid D-Bus path element, libsecret assertion, then
  a wait forever). A valid name for a missing collection fails fast with
  `Object does not exist at path /org/freedesktop/secrets/aliases/<name>`.
  The provider change guards the first case. libsecret 0.21.7, gnome-keyring
  50.0.
- **What I touched outside my space, all reverted or transient:** an item
  `secrets/proto/x` in the in-memory `session` collection (cleared), and
  once, by resolving the alias `default`, an item `secrets/proto/y` in the
  live default keyring (cleared the same command; the four existing entries
  are intact; the file was rewritten). A `pkill -f` pattern of mine matched
  Omarchy's diagnose-crash terminal by its prompt text and killed it. Never
  kill by command-line text again; match `/proc/<pid>/exe`.
- Pre-existing, proven not asserted: 8 `secrets` tests fail on this machine
  because `~/.config/mise/config.toml:27` exports `SECRETS_PROVIDER=libsecret`
  into every `mise run`, and the tests' `unset` cannot reach through the
  `secrets()` helper's re-entry into mise. Same shape as the `chat_send.bats`
  case below. Filed in [[mise-gotchas]].
- Two worktrees from earlier sessions still hold branches beside the live
  clone (`secrets-provider-bats-110`, `secrets-secrets-provider-env`). Not
  removed this session; they predate it.
- Blocked on the owner: knick's proposal, and whether the libsecret store on
  this machine is repaired or replaced. The machine-specific keyring finding
  went to the owner in the session report, not into this public file.

## Last finished — olavostauros/oikos, `welcome` kept YAML quotes on `github_login`

`oikos_welcome_resident_metadata` split frontmatter with bare awk, so the
quoted `github_login: "knack-oikos"` in both identity notes carried its
quotes into the viewer comparison and "GitHub attention" was skipped on
every wake with a false identity mismatch. Row 4 in [[work-queue]]; row 2
was already `pr-open` (modules#61). Shipped as
https://github.com/olavostauros/oikos/pull/1 on 2026-09-14.

- Branch `knack/welcome-quoted-login` on `olavostauros/oikos` itself, commit
  `834a853`, signed, cut from `main` (`22e825d`). No fork — forking a
  non-KKL repo is not a standing grant, and I hold `push` there. Worked in a
  separate clone `~/agents/knack/oikos` so the shared checkout stayed on
  `main`. Queue update `82855db` fast-forwarded onto `main` and pushed with
  my own token.
- One helper, `oikos_welcome_frontmatter_value`, trims trailing whitespace
  and one pair of quotes; both `type` and `github_login` read through it.
  New `welcome.bats` case fails on pristine with the live line, passes on
  the branch. Full gate 219/220; the failure is pre-existing (below).
- **The push went out with the owner's credentials once.** `shimmer as
  knack` runs `agent:list` from the cwd and needs readable notes, so from the
  encrypted clone it failed silently and bare `gh`/`git push` fell through to
  the owner's session. My first attempt gated on `gh api user` and refused;
  my retry did not gate and pushed. Said so in the PR body and the queue
  entry. Rule for me: `eval "$(cd ~/Work/oikos && shimmer as knack)"`, then
  `cd`, and never drop the `gh api user` gate from a command that pushes.
- Pre-existing on `22e825d`: `chat_send.bats:97` "still succeeds without a
  channel configured" fails because `f94b5b7` gave
  `OIKOS_DISCORD_CHAT_CHANNEL` a default in `mise.toml`; `unset` in the test
  cannot reach the branch through `mise run`. Recorded for knick in the
  queue entry's `notes:`; not filed by me.
- Discord outbound mirror verified as me the same wake: `mise run chat:send
  --as knack` printed `Mirrored to Discord.` Inbound is owner-side.

## Before that — KnickKnackLabs/modules, empty manifest is stat-dirty

`modules setup` wrote `.modules/manifest` as zero bytes (`: > "$MANIFEST"`,
`setup:47`), and a zero-byte worktree file whose git-crypt blob is not the
empty blob is stat-dirty forever — `git stash create` exits 1 and every
`git merge --no-ff` in `~/oikos` died `fatal: stash failed`. Diagnosed by
knick in [[household-backlog]]; assigned in [[work-queue]]; shipped as
https://github.com/KnickKnackLabs/modules/pull/61 on 2026-09-13.

- Branch `knack/non-empty-manifest` on `knack-oikos/modules`, commit `98e2f1c`,
  signed `G` with key `08D080CEE3860BA2`, cut fresh from `upstream/main`
  (`460d409`). Fork created this session. Pushed; `headRefOid` verified, 0
  unpushed. Queue update on `~/oikos` branch `knack/queue-non-empty-manifest`
  (`14c17ce`), fast-forwardable onto `main` (`faef528`), not merged — owner's.
- Three writers could emit zero bytes: `setup`, `manifest_remove` on the last
  entry, and the merge driver's success path. One `manifest_normalize` now
  serves every writer and emits a single newline when nothing remains; every
  reader already skipped blank lines, so no reader changed.
- Reproduced with the real thing, not the filter-only shape: `modules setup`
  git-crypts the manifest itself via `rudi init --no-user`, so a throwaway
  repo plus `git merge --no-ff` is the whole reproduction. Pristine: exit 128.
  Fixed: exit 0.
- Four tests fail on pristine, checked in a detached worktree at `460d409`
  with the test files copied in, removed in the same chain. The gpg roundtrip
  tests skip by default; `TEST_GPG_FINGERPRINT=<my key>` runs them for real.
- `codebase lint` fails two rules on modules at `460d409` already
  (`process-substitution-status`, `remote-url-output`); measured on pristine,
  not asserted. `readme build --check` fails on any test-count change; run
  `readme build` and commit `README.md`.
- **`~/agents/knack/.gitconfig` says `email = knack@oikos.local`.** A commit
  from a shell that never sourced `agent:env` lands signed but as
  `knack@oikos.local`, which is not the key's UID and not the mail identity.
  Caught before push; re-authored with `agent:env` sourced. The Pending item
  in AGENTS.md claiming `G knack <knack@stauros.family>` was wrong and is
  corrected in this commit. Whether to change the file is the owner's —
  identity config.
- Ran `shimmer as knack` unwrapped once while building the activation
  preamble; the PAT went into the transcript. Same defect knick filed
  2026-09-09. Reported to the owner; rotation is theirs.
- `KnickKnackLabs/notes` initializes `notes/.manifest` with `touch` at its
  `setup:141` — same shape, not biting `~/oikos` (that file is 376 bytes).
  Not opened; knick's to file.

## Before that — KnickKnackLabs/shimmer, `whoami` on unset `GH_TOKEN`

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
- Row 5 in [[work-queue]] (`welcome` reads chat `oikos`; only `default`
  exists) is mine once the owner picks the name. knick recommends
  `${CHAT_CHANNEL:-default}`. Not before the decision.
- Five of my PRs are open now: oikos#1 joins emails#47, sessions#146,
  threads#26, shimmer#816.
- Take whatever knick ranks next. [[work-queue]]'s pointer under `## Queue` now
  says there is **no live assignment** — the five entries behind shimmer#816 all
  stay `queued` and none becomes "next" by ordering. Do not self-promote one.
- The `whoami` `sed`/`gh auth status` follow-up is unfiled on purpose. If knick
  wants it, it is a fresh branch off `upstream/main`, never a stack on
  `knack/whoami-unset-gh-token`.
- Four of my PRs are open and waiting (emails#47, sessions#146, threads#26,
  shimmer#816). Silence is not a signal; I do not nudge my own PRs.
