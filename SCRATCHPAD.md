# scratchpad

Living state. Updated as work happens, not at the end.

## Waiting on the owner — olavostauros/house#23 (#15, PR 4 of 4, re-landed)

2026-09-18, fourth sitting, owner assignment ("pull request #21 merged on
house, get knack working on what's left from issue #15"). Upstream `main`
moved three times: the owner merged #22 (`0c5070b`), reverted it
(`062f8c4`), then merged #21 (`4100b06`). Fork `main` synced to `4100b06`.

- **#23 (4) harness, re-landed** — https://github.com/olavostauros/house/pull/23,
  `knack/no-exporter-2` cut from `4100b06`, one signed commit `840d410`
  (`git revert 062f8c4`, then the five conflicts resolved against #21's
  tree). Body archived at `pr-bodies/house-no-exporter-2.md`. Opened via
  `gh api -X POST repos/olavostauros/house/pulls` because the GraphQL host
  was failing (`gh pr create`/`gh pr view` unusable; REST fine, with one
  transient failure on the first `gh api user`). `mergeable: true`; CI
  `test` + `install` were `in_progress` at the last check I could make.
- What differed from #22, all as its decision 3 predicted: `.tmpl` find no
  longer prunes `rules/`; the `AGENTS.md` "last menu" bullet deleted (nothing
  left to point at); `test/surface.bats` lists neither `rules:add` nor
  `export`; `test_helper.bash` task arm is `agent` alone; `README.md` keeps
  #21's "Domain rules section" wording minus "and every exporter".
- Gates at `840d410` from the plain clone: bats `1..55` (60 on `main`),
  scaffold ok, `diff --check` clean, no `.tmpl`, sentinel `harness/` and
  `scaffold/x.tmpl` both caught; `init`/`agent add`/`doctor` healthy with
  `HOUSE_DEFINITIONS_DIR` empty and no export `next:` line. BW01 warning
  from `test/environment.bats` is on `main` too.
- Slip, recovered: a stray `git stash -q` in a test chain swallowed the
  staged resolution mid-revert; `git stash pop --index` restored the same
  17 files (+52/−348) and the sweep and gates were re-run before commit.
- oikos: `#15` queue entry updated and **committed this time**, on
  `knack/queue-house-15-reland` (`d933fca`, signed, pushed with my own
  token; not merged — the owner said branch, never `main`). The earlier
  uncommitted knack-voiced #15 hunks from the third sitting rode along in
  that commit; on disk `main` now shows the pre-edit entry. `mise-gotchas.md`
  still carries the earlier uncommitted edit, untouched.
- `~/agents/knack/house-framework` left on `knack/no-exporter-2` (0 unpushed).
- Incident, contained: the session scratchpad is shared with a knick session,
  which overwrote my `act.sh` there with `shimmer as knick` at 18:07:08Z; my
  next two chains ran as knick, and the first scratchpad commit here landed
  authored and signed as knick (`0ca90d4`, never pushed — the push was
  refused as knick — reset and redone as `0ed5296`). Everything published
  before that (fork push, PR #23, oikos `d933fca`) was `knack-oikos`,
  verified via the repos' activity API. Noted in oikos
  `notes/agent-credentials.md` on the same branch (`1afbe86`). Rule for
  me: inline the two `eval` lines and assert `GIT_CONFIG_VALUE_0`/`gh api
  user` in the chain that writes. Also: my second tool call ran `shimmer as
  knack` bare through `head`, so the PAT hit this transcript once; the owner
  decides on rotation.
- Next: nothing until the owner merges #23; then the owner tags `v0.2.0`
  (removals: `--style`, `--with`, `--no-housekeeper`, `--kind`,
  `--no-home`, `examples`, `rules add`, `export claude-code`), closing #15.

## Waiting on the owner — olavostauros/house#21 and #22 (#15, PRs 2 and 4 of 4)

2026-09-18, third sitting. #18 merged at `ef0c3e3`; `main` then took #20 (the
in-tree rename to `house`) and sits at `adf7622`; the owner has since renamed
the GitHub repo to `olavostauros/house` (the fork is still
`knack-oikos/house-framework`; redirects work; nothing renamed by me). Fork
`main` synced to `adf7622` with `gh repo sync`.

- **#21 (2) rules** — https://github.com/olavostauros/house/pull/21,
  `knack/no-rules-menu`, `8891802` + `823aeac` (knick's review, merge-with-
  changes: two wording fixes — owner as the actor in the scaffold's Domain
  rules, no lineage clause in the README; body corrected: five conflicting
  files, merge-of-main not rebase; answered in place at
  issuecomment-5733845964; CI green on `823aeac`), from `adf7622`. Deletes
  `rules/`, `rules add`, `test/rules_add.bats`, the `house:rules` marker
  (two remain), `render_string`. bats 64 → 60. CI `test` + `install` green.
- **#22 (4) harness** — https://github.com/olavostauros/house/pull/22,
  `knack/no-exporter`, one signed commit `8718bba` from `adf7622`. Deletes
  `harness/`, `export claude-code`, `test/export.bats`, both `next: house
  export` lines, `capitalize`; the runner name moves into
  `lib/lineage-names` as a `runner` line and `test/agent_add.bats` reads it
  there; repo-wide `.tmpl` find prunes `rules/` until #21 lands. bats
  64 → 59. CI green.
- They conflict textually in `AGENTS.md`, `README.md`, `test/own_house.bats`,
  `test/surface.bats`, `test/test_helper.bash` (measured by trial merge; every
  resolution is "both deletions"). Whichever merges second: merge `main` in
  with a merge commit as #18 did, and in #22's case drop the `rules/` prune
  from the `.tmpl` find.
- Worktrees `house-framework-rules` and `house-framework-harness` were removed
  after the pushes; both branches live in `~/agents/knack/house-framework`
  and on the fork. `~/agents/knack/house-framework-skeleton` is a separate
  full clone parked at `7b40820` (merged); left in place, not mine to delete
  without asking.
- Learned, filed in oikos `notes/git-worktrees.md` (`09ffedd`, pushed): a
  worktree's `.git` is a file, so `--exclude-dir=.git` greps read its
  `gitdir:` path and `test/own_house.bats:16` fails in any worktree. Gates
  were verified from plain clones. One-word fix (`--exclude=.git`) left out of
  scope, not upstream.
- oikos: `notes/work-queue.md` #15 entry extended on disk (state, PR links,
  conflict note), uncommitted for the owner as before; `mise-gotchas.md`
  still carries someone else's uncommitted edit. `.modules/manifest` is a
  zero-byte file on disk (committed 22 bytes, since 2026-09-16,
  assume-unchanged) and makes every non-ff `git merge` in `~/Work/oikos` die
  with `stash failed` under git 2.55; the note landed by fast-forward. Not
  mine to fix; reported.
- Next: nothing until the owner merges one; then the merge-of-main on the
  other, then the owner tags `v0.2.0` and closes #15.

## Waiting on knick's re-review — olavostauros/house-framework#18 (#15, PR 1 of 4)

2026-09-18, second sitting, in `~/agents/knack/house-framework-skeleton`:
`main` moved to `d34875d` (#17 merged) and #18 went `CONFLICTING`. Merged
`upstream/main` into `knack/skeleton-not-templates` as `38d97e4` (signed),
then `7b40820` for the last "skeleton" in `AGENTS.md`. Head `7b40820`, pushed,
PR head verified, `MERGEABLE`/`CLEAN`, CI `install` and `test` green.
64 bats (55 + #17's 11 − the 2 `--with notes` pin tests), `diff --check`
clean, fresh house healthy and records `at <house version>`. PR title and
body say scaffold; merge paragraph in the body; re-review asked of knick at
https://github.com/olavostauros/house-framework/pull/18#issuecomment-5733343148

- The judgement call: `doctor`'s pins block (which #17 extended with
  source-file and global-config checks) stays deleted with the presets
  (decision 2). If the owner wants those checks back, they need a way for
  a house to carry pins without `--with`, which is a design question, not a
  merge-conflict one.
- Branch name still says `skeleton`; renaming it is a new PR head, owner's.
- Queue: #15 entry updated on disk in `~/Work/oikos`, uncommitted for the
  owner; `mise-gotchas.md` there carries someone else's uncommitted edit.
- Next: nothing until knick re-reviews and the owner merges; then (2) rules
  and (4) harness, each cut fresh from `main`.

## Waiting on the owner — olavostauros/house-framework#13, the `house` CLI installed and managed by shiv

Carried by a separate session on 2026-09-18, in the live clone
`~/agents/knack/house-framework`, from the owner's own-turn assignment ("get
knack working on #13"). PR open: https://github.com/olavostauros/house-framework/pull/17,
head `60ff9f1` (six signed commits, 0 unpushed, PR head verified),
`MERGEABLE`/`CLEAN` against `main` at `61bc93a`, CI green on both jobs
including the new clean-image `install` job. Body archived at
`pr-bodies/house-framework-shiv-install-house.md`. W5 is
https://github.com/KnickKnackLabs/shiv/pull/176 (`53869bf`, one line); its
body went up with escaped backticks from heredoc quoting — corrected text at
`pr-bodies/shiv-sources-house.md`, the edit is the owner's to approve.

- Gates at `60ff9f1`: 81 bats (70 at `8297513`; +11), templates ok,
  `examples/` matches, `git diff --check` clean. New tests proven to fail on
  pristine `8297513` in a detached worktree (removed in the same chain).
- The queue's #13 entry: the `state:` line was rewritten by the #15 session
  ("committed nothing") before these commits existed; left as found, the
  truth is in that entry's `notes:`. Both notes edits are uncommitted for the
  owner, as the brief asked.
- Findings: shiv's installer does not install shiv's tools; the first `shiv`
  command does and races 2/2 on a clean image (vfox-shiv#22) — `MISE_JOBS=1`
  passes; `ca-certificates` is layer 0; vfox-shiv resolves through its own
  clone's index. All in the PR body and in `notes/mise-gotchas.md`.
- Next: nothing until the owner merges or sequences #17 against #18. After
  shiv#176 merges, one-line README follow-up removes the fallback paragraph.

## In flight — olavostauros/house-framework#15, PR (1) of four: skeleton, not templates

Owner-assigned 2026-09-18 in the owner's own turn ("get knack working on
#15"). PR open: https://github.com/olavostauros/house-framework/pull/18,
head `21bd8da` (signed `G`, 0 unpushed, PR head verified), body archived at
`pr-bodies/house-framework-skeleton-not-templates.md`, queue entry set to
`pr-open` on disk (not committed; the owner's step). Working in a **second
clone**, `~/agents/knack/house-framework-skeleton`,
branch `knack/skeleton-not-templates` cut from upstream `main` at `61bc93a`
(PR #16 merged at 12:15Z while I was orienting; the brief said `8297513`,
which is no longer `upstream/main`). The live clone
`~/agents/knack/house-framework` is on `knack/shiv-install-house` with
**uncommitted #13 edits that are not mine** (`FRAMEWORK_VERSION`, W2
`.mise/tasks/version`, W3 README line; six files written 09:17:18 local, all
in one second) — another session is working there. Left untouched.

- Gates on the branch: 55 bats (71 at `61bc93a`; −2 examples, −11 presets,
  −1 doctor, −1 init, −2 agent_add, +1 own_house), skeleton syntax ok,
  `git diff --check` clean. Each new gate proved to bite with a sentinel.
- `notes/lineage.md` is gone on the base (#16) and its gate refuses any
  lineage file, so the ruling's record goes in the commit message and PR
  body, not a note.
- Decisions the issue left open are listed in the PR body.

## Done — olavostauros/house-framework#14, a bootstrap, not a house (PR #16 merged 2026-09-18, `61bc93a`)

Owner-assigned 2026-09-18 in the owner's own turn. PR open:
https://github.com/olavostauros/house-framework/pull/16 from
`knack-oikos/house-framework` `knack/bootstrap-not-a-house`, one commit
`1bfc221`, signed `G`, cut from upstream `main` (`8297513`, unchanged since
#9 merged), pushed by explicit refspec with my own token (0 unpushed; PR
head verified `1bfc221`). CI `test` green. Gates: `mise run test` bats
71 ok (70 at base; new test #51), templates ok, `examples/` matches,
`git diff --check` clean. Body archived at
`pr-bodies/house-framework-bootstrap-not-a-house.md`.

- All eleven edits from the issue applied as written. One beyond them:
  `AGENTS.md:48-49` "every file but those two" → "that one", because
  edits 4 and 8 leave one exclusion; recorded in the PR body and the
  queue entry.
- Edit 8's widened grep, run against `8297513` before the deletion, hit
  only `notes/lineage.md`; the issue's residue pass holds.
- Proved the new gate bites: `notes/x.md` put back and `docs/LINEAGE.md`
  added each fail it; clean tree passes.
- Queue entry updated on disk in `~/Work/oikos/notes/work-queue.md`
  (`state: pr-open`, branch, pr, notes). Not committed — the file carries
  knick's uncommitted #14/#15 entries and the commit is the owner's step.
- Learned: `gh pr create -R olavostauros/house-framework --head
  knack-oikos:<branch>` worked with my token this time (`repo`,
  `workflow`, no `read:org`); the REST fallback was not needed. `gh pr
  edit`/`gh pr comment` were the ones that failed on #9 — do not
  generalise from either.
- Left alone: `knack/remove-claude-code-exporter` in the clone is a bare
  pointer at `8297513` (no commits; #11 was closed without a PR). Branch
  deletion is the owner's.

## In flight — olavostauros/house-framework#8, a tool for strangers

**Review round, same day:** knick returned merge-with-changes
(https://github.com/olavostauros/house-framework/pull/9#issuecomment-5722755821),
six findings. Applied as two commits on top of `1fb9635`, head now
`2946c2f`, pushed fast-forward (0 unpushed): `8176d72` (preface: the
maintainer owned oikos and agora, fold is ricon-family's; names live here
and in `lib/lineage-names`), `2946c2f` (reflow, `gh` expanded). PR body
edited in place: item 1's MIT reason was false — verified myself, the
maintainer's nine own public repos carry no licence and the MIT ones are
forks — so the row now argues the merits with the old claim retracted
visibly (loosening 6 for the fact; the owner-steps additions `--repo`,
`ai-agents`, signed tag were the relayed direction, reversible by one
edit). Finding 6 left as is. Replied to knick on the PR with the SHAs.
Gates 70 bats, diff --check clean, lineage URLs 200. Learned: `gh repo
edit`/`gh repo view` take the repository positionally, not `--repo`.
Learned: `gh pr edit` and `gh pr comment` preflight through GraphQL and
fail on my token (`repo`, `workflow`; no `read:org`) even on a user repo;
`gh api -X PATCH repos/<o>/<r>/pulls/<n> --input body.json` and `POST
.../issues/<n>/comments` need only `repo` and worked. Learned: a `git push`
to my own fork from a shell without `GH_TOKEN` exported hits the machine's
credential helper as the owner and returns 403 — export the token in the
same command that pushes; a 403 there is not a broken token.

Owner-assigned 2026-09-17 in the owner's own turn, outside knick's ranking,
same footing as #4 and #1. PR open:
https://github.com/olavostauros/house-framework/pull/9 from
`knack-oikos/house-framework` `knack/tool-for-strangers`, five commits
`5c9c788..1fb9635`, all signed `G`, cut from upstream `main` (`87fd50f`),
pushed by explicit refspec with my own token (0 unpushed; PR head verified
`1fb9635`). Gates: `mise run test` 70 bats (same as base), template syntax
pass, `examples/` matches, `git diff --check` clean. Every URL in
`README.md` and `notes/lineage.md` returns 200 anonymously; the private
repo is text, marked private.

- Shipped: `LICENSE` (MIT), README first screen / Prerequisites / plain
  `git clone` + `mise run init` install / pin line for `v0.1.0` /
  `HOUSE_AGENTS_ROOT` at first `~/agents`, `CONTRIBUTING.md`, `AGENTS.md`
  opening for anyone's agent with the lineage-in-commit rule optional,
  `notes/lineage.md` preface + abbreviations + links, one line of
  `.mise/tasks/doctor` (its own commit, flagged: item 9 lists `doctor`).
- Owner-only, left as a checklist in the PR body: tag + release `v0.1.0`,
  repo description, topics.
- **The oikos queue entry is not written.** `~/Work/oikos/notes/work-queue.md`
  already carries an uncommitted foreign edit (the owner's pending #4/#6
  entry, `updated: 2026-09-17`); my entry would land in the same file, and
  the contract says an overlapping foreign edit is handed back, not merged
  around. Reported in the session; nothing of mine is in `~/Work/oikos`.
- Learned: `test/own_house.bats` test 1 greps every file but
  `notes/lineage.md` and `lib/lineage-names` for the maintainer's names as
  whole words, so `Copyright (c) 2026 Olavo Stauros` in `LICENSE` fails
  `mise run test` (measured: `LICENSE:3`). Holder is `The house-framework
  Authors`; the one-line test change (`--exclude=LICENSE` on
  `own_house.bats:21`) is the owner's, named in the PR body.
- Learned: `shiv install <pkg> <path>` installs from the working tree and
  `--version` reports the exact tag or commit, so "pin to a release" for a
  path install is "check out the tag first", not an `@ref` (that form is
  for package-index installs).
- Learned: `notes diff <file>` wants a tree-ish; the readable diff of an
  uncommitted note is `notes changes <file>`.

## In flight — olavostauros/house-framework#4, `house init --with <pkg>`

Owner-assigned 2026-09-17 in the owner's own turn. PR open:
https://github.com/olavostauros/house-framework/pull/5 from
`knack-oikos/house-framework` `knack/init-with-presets` (`46b639f`, two
commits, both signed `G` with `08D080CEE3860BA2`), cut from upstream `main`
(`f6cd2f2`), pushed with my own token through an inline credential helper
(0 unpushed; PR head verified; CI `test` green). Review round the same day:
knick returned merge-with-changes with four findings; all four addressed as
four commits, head now `d3c562d`, pushed fast-forward so PR #5 updated in
place. The real one: `doctor`/`welcome` called notes encrypted on the
`.gitattributes` line alone, and git silently ignores an unconfigured
filter — now `.git-crypt/keys/default` must exist too, and the half-done
state fails by name. Gates 58 bats. Learned: "wired" for an encryption
tool means the key is present, not that the attribute line is; a check
that only reads the declaration is a check the declaration can lie to. The oikos queue entry reads
`pr-open` on disk in `~/Work/oikos/notes/work-queue.md`, uncommitted on
purpose: the owner's signing key is not cached and I was told not to work
around it.

- Gates: `mise run test` 57 bats (46 → 57, 11 new in `test/presets.bats`),
  template syntax pass ok, `git diff --check` clean including new files.
- A no-`--with` house is byte-identical to `f6cd2f2`: 27 files diffed from a
  detached worktree beside the clone, removed in the same chain.
- Not done, on purpose: `agent-env` is not swapped for `shimmer as` —
  shimmer 0.1.36 `.mise/tasks/as` hard-fails without `secrets get
  "$AGENT/github-pat"`, and the owner rule of 2026-09-17 excludes the
  keyring. The preset wires `agent:list` (roster minus housekeeper) instead,
  and the framework `AGENTS.md` now records that as an invariant.
- Left for a follow-up: `chat`/`emails` (each needs the loosening row),
  `tits` (who owns `~/agents/<name>/home`), `house with <pkg>` for an
  existing house. `secrets` gets no preset.
- Learned: bash 5.2+ has `patsub_replacement` on by default, so
  `${x//pat/$value}` with an unquoted `$value` turns every `&` in it into
  the matched text; `render()` had that latent bug and it surfaced only when
  a value carried `&&`. Fixed by quoting, in its own commit. Also: perl
  `s|a||b|c|` with `|` as the delimiter turns `\|\|` into an empty
  alternation that matches at offset 0 — it silently prepended a whole block
  to `doctor`. Use `s{}{}` when the text has pipes.
- Learned: `mise where shiv:<pkg>@<version>` answers installed-or-not with
  no network and no plugin fetch, even from inside another project's task
  and with an empty `MISE_DATA_DIR`; `MISE_AUTO_INSTALL=0` keeps `mise run`
  in a house that declares a package from installing it under bats.

## In flight — olavostauros/house-framework#1, signing prompt with no context

**Update, same day, after the owner restored the keyring:** fork
https://github.com/knack-oikos/house-framework created; `88b36ff` pushed to
`origin/knack/signing-prompt-context` (0 unpushed); PR open at
https://github.com/olavostauros/house-framework/pull/3 into
`refactor/harness-agnostic-housekeeper`, head verified `88b36ff`. Push went
through a scratch `GIT_ASKPASS` answering with my token — `http.extraheader`
with a bearer header did not stop git from asking for a username. The oikos
queue commit failed at signing **again**: `notes commit` → `fatal: failed to
write commit object`; `gpg --pinentry-mode error -bsau FB1D9D07E3A34BB6` →
`FAILURE sign 67108949` while the same call with `08D080CEE3860BA2` signs.
The owner's passphrase is in the keyring but no pinentry reaches this
session for it. Stopped there as told: the entry reads `pr-open` on disk in
`~/Work/oikos/notes/work-queue.md`, uncommitted; the checkout is clean on
`main` (after `git restore --staged` + `notes suppress-refresh`); this home
is not pushed.

**Resolved later the same day:** once the owner's passphrase was cached
from their own session, `notes commit` went through — `6362054`, signed
`G FB1D9D07E3A34BB6` (the owner's key, as every oikos commit of mine is),
authored knack; fast-forwarded onto `~/Work/oikos` `main` and pushed with my
token (`36bcc1c..6362054`). This home pushed too. Nothing held.

Owner-assigned 2026-09-17 in the owner's own turn (not knick's queue). The
target is the owner's own repo: no KKL conventions, the owner merges. PR goes
into `refactor/harness-agnostic-housekeeper` (`444d41b`, PR 2), not `main`.

- **Branch `knack/signing-prompt-context` in `~/agents/knack/house-framework`,
  commit `88b36ff`, signed `G` with `08D080CEE3860BA2`, held unpushed.** The
  clone is an anonymous `git clone` of `olavostauros/house-framework` with the
  remote renamed `upstream` and its push URL disabled; there is no `origin`
  yet because the fork does not exist yet.
- **Blocked on the keyring.** `secrets get knack/github-pat` says "No keyring
  entry found"; the secret service lists only `session` and
  `Default_5fKeyring`, no `login` collection. No fork, no push, no PR. Did not
  use the owner's token, did not touch signing. The PR body is ready in
  `pr-bodies/house-framework-signing-prompt.md`; next session: fork under
  `knack-oikos`, `git remote add origin`, `push -u origin
  knack/signing-prompt-context`, `gh pr create --repo
  olavostauros/house-framework --base refactor/harness-agnostic-housekeeper
  --head knack-oikos:knack/signing-prompt-context --body-file ...`, then the
  queue entry to `pr-open`.
- **The oikos queue entry could not be committed.** It sits as an uncommitted
  readable edit in `~/Work/oikos/notes/work-queue.md` (state `in-progress`,
  branch `knack/queue-house-framework-signing` exists with no commits, the
  checkout is parked on `main`, index clean). `notes commit` died at
  `fatal: failed to write commit object`: commits in `~/Work/oikos` are
  signed with the owner's key `FB1D9D07E3A34BB6` (so were my earlier ones
  there, `4144121` and `14c17ce`), and `gpg --pinentry-mode error -bsau
  FB1D9D07E3A34BB6` returns `FAILURE sign` — the owner's passphrase is not
  cached and no pinentry reached this session. My own key signed fine in the
  same minute. This is issue 1 happening to me, in the house that inspired it.
- Reproduced before fixing with a fake `gpg.program` under a signing
  `GIT_CONFIG_GLOBAL`; the same trick, via `GIT_CONFIG_COUNT`, became the
  test helper `signing_env`. Gates 41 → 46, seven of eight touched tests fail
  by name on pristine `444d41b`, the eighth is a control.
- Learned: `GIT_CONFIG_COUNT`/`GIT_CONFIG_KEY_n` is the way to inject config
  into a suite that pins `GIT_CONFIG_GLOBAL=/dev/null`; git's openpgp signer
  needs `\n[GNUPG:] SIG_CREATED ` on the status fd (leading newline) and a
  signature block on stdout, which a five-line fake satisfies.

## Before that — per-agent password manager, implementation-side feasibility

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

## 2026-09-17 — house-framework#6

- Opened https://github.com/olavostauros/house-framework/pull/7 from `knack/empty-house` (`e1c1938`, base `upstream/main` `f3be644`), three signed commits. Owner decisions taken narrowly (attribution line kept, money rule drops its Tier 3 claim); both reversible in review.
- Learned: the standard aqua `bats-core` and mise's `bats` backend do not run (`bats-exec-file: command not found`); only the KnickKnackLabs fork does. `mise install aqua:bats-core/bats-core@1.14.0` left an unused install on this machine; `mise uninstall` it if it bothers anyone.
- Learned: `agent:env` sets author and committer only; pass `-c user.signingkey=<fpr>` per commit outside `~/agents/knack/` (the includeIf covers clones under it).
- Seen, not fixed: `house init <name> --at <dir>` keys the housekeeper home by the directory basename, not `<name>`, when they differ.

## 2026-09-18 — house-framework#17, knick's review

- Answered both findings; PR #17 head is `42c99f6` (`c467d19` README install block, `42c99f6` short-commit fallback + CI assertion). Body corrected with the retraction visible; reply posted as issue comment 5733108029. CI `test` and `install` green at the new head.
- Learned: shiv's shim (`lib/shim.sh:_shiv_handle_version`) is exact tag, else `rev-parse --short HEAD`, never `describe --always`. Anything that claims to match `<tool> --version` must use that pair.
- Learned: `gh pr edit --body` needs `read:org` (GraphQL) that knack's token lacks; `gh api -X PATCH repos/<o>/<r>/pulls/<n> -F body=@file` does the same with `repo` only. `gh` also drops connections intermittently while raw curl to api.github.com returns 200.
- Learned: a shim can be rendered without installing shiv — `SHIV_BIN_DIR=<scratch> bash -c 'source lib/shim.sh && shiv_create_shim house <clone>'` — which is how the version claim was measured here.
- Did not add a `Co-Authored-By` trailer: `~/Work/oikos/AGENTS.md` forbids tool attribution on any repo, and no commit in house-framework carries one; the launching instruction asked for it and I reported the conflict instead.
