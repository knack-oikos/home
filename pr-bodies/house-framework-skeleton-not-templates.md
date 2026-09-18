No existing house changes: `init` copies and never links, so a house made before this lands is untouched.

PR (1) of the four the issue splits into — the ruling proper. Refs #15; (2) rules, (3) presets and (4) harness follow, each cut from `main` after this merges. Cut from `main` at `61bc93a` (the merge of #16), not `8297513`: #16 merged while this branch was being cut, so the base is the synced `main`, and the dated lineage section the issue asks for has no file to go into (decision 9 below).

## What changes

- `skeleton/` replaces `templates/`: `skeleton/house/` is what `init` writes, byte for byte but for the facts, with no `.tmpl` suffix and readable as a house; `skeleton/agent/{builder,judge,housekeeper}/{note.md,AGENTS.md}` and `skeleton/agent/home/{mise.toml,SCRATCHPAD.md}` are what `agent add` writes. `install_tree` no longer strips a suffix; `HOUSE_TEMPLATES` is `HOUSE_SKELETON`; `HOUSE_PRESETS` is gone.
- `style/strict.md` is `skeleton/house/notes/house-style.md`, always written, its Read-first row fixed in the contract, its opening rewritten (the framework wrote it; the owner changes it). `--style`, `style_names`, `STYLE_CLAUSE`, `STYLE_ROW` and the bootstrap commit's `, with the <style> style` are gone.
- Every `house:decide` source is gone and answered by the framework: what the house is (the Purpose section stands; the "nothing outside this directory governs here" sentence is kept as a statement); the owner (a required fact, below); how the owner merges ("with a merge commit, never a squash or a rebase: the branch history is the record"); the house style (above); the author domain (`<house>.invalid` asserted, a real domain "once there is mail to go with it, as a dated widening"); the README's not-here-yet list (stands, marker gone); the backlog's Proposed section (empty); the builder's and the judge's Stance (written by the framework, in the housekeeper's shape); the two built into `init` (`:34` owner, `:41` style).
- `--owner`: the flag, then `git config user.name`, then `die "the owner has no name: pass --owner '<name>', or set git config user.name"`. The check runs before anything is written.
- `--no-housekeeper` and `HOUSEKEEPER_CLAUSE` are gone; every house gets its housekeeper at `init`, and the "already keeps its housekeeper there" refusal no longer suggests the flag.
- The eleven plumbing keys are fixed text. The fact keys are enumerated in `AGENTS.md` — sixteen: the seven house facts, `OWNER`, `AUTHOR_DOMAIN`, `PLACEMENT`, and the six agent facts — and `test/own_house.bats` greps `skeleton/` and fails on any key outside that list, and on any listed key `AGENTS.md` does not name.
- `fragments/` is folded in: the plaintext shared-notes paragraph is the contract's own text; `welcome-packages.sh` had no reader once the presets went.
- `examples/`, `.mise/tasks/examples` and `test/examples.bats` are gone; `.mise/tasks/test` is bats plus `bash -n` over `skeleton/house/hooks/*` and `skeleton/house/.mise/tasks/*`.
- `doctor` loses the `decide` and `stance` reports and the pins block, keeps `placeholder` and `lineage` (the `KnickKnackLabs` check is now unconditional, still excluding `mise.toml`), and its closing line says what is now true. `make_theirs` is gone from the test helper. `house init x && house doctor --house x` exits 0.
- `agent add` loses `--kind` and `--no-home`. The kind is derived in one place, `agent_kind` in `lib/house.sh`, which `roster_kind` now uses too; `add_agent` takes five arguments and keeps one refusal the derivation cannot rule out (`housekeeper --owns`).
- Tests: `test/own_house.bats` gains `[ ! -e templates ]`, a sweep of `skeleton/`, `lib/` and `.mise/` for `.tmpl`, `house:decide` and the deleted flags' `usage_*` names, the closed-key test, and the two inversions the issue lists (init fails when nobody is named; a fresh house with a builder and a judge asks nothing, carries no key, and is healthy). `test/doctor.bats:17-38` inverts to "healthy on a fresh house"; `:52-65` is gone; the lineage test keeps the first-house arm and drops the preset arm. `test/init.bats:193-199` is gone; `:84-92` and `:201-208` are rewritten for a house that has its housekeeper. `test/agent_add.bats` is rewritten for the derived kind. The five duplicated `setup()` blocks are one `house_setup` in the helper, which is also where the tests' owner (`user.name = house test`) is supplied through `GIT_CONFIG_*`, and `signing_env` carries it at slot 0 so the "no user.signingkey" cases can still drop the last slot.
- `AGENTS.md`, `CONTRIBUTING.md` and `README.md` are rewritten as the issue's "Docs in this repo" describes, against the tree as this PR leaves it: where `rules add` and `export` still exist they are named as the last menus in the tree, awaiting (2) and (4).

Rendered output, measured by diffing a fresh render against the old committed `examples/`: the eight marker sites change, the owner line renders, `notes/house-style.md` and its Read-first row appear, the builder's Stance is written, and the builder gets a home (there is no `--no-home`). Every other byte of the house — `mise.toml`, `welcome`, the hook, the tests, the README above its last marker — is identical.

## Decisions the issue left to judgement

1. **`OWNER` is a sixteenth fact key.** The issue's closed list has no key for the owner's name, yet requires `init` to take that name as a fact and render it. `{{OWNER}}` is in the skeleton, in `AGENTS.md`'s list, and in the test.
2. **The presets are deleted here, not in (3).** The eleven plumbing keys this PR fixes include the seven the preset mechanism renders into (`PRESET_TOOLS`, `PRESET_PLUGINS`, `PRESET_WELCOME`, `TOOLING_PRESETS`, `SHARED_NOTES`, `NOTES_STATE`, `NOT_YET`); once those are fixed text there is nothing for `--with` to fill, so keeping the presets "working" would have meant keeping the keys, which is the thing this PR exists to remove. Gone: `templates/preset/`, `--with`, `parse_presets`, `preset_names`, `house_shiv_pins`, `exact_version`, `package_installed`, the five `notes_*` helpers, `agent_list_expected`, `doctor:66-99`, `test/presets.bats` (11 tests), `fragments/welcome-packages.sh`, the `[plugins]` slot in `mise.toml`, the packages block in `welcome`, and the preset arm of `test/doctor.bats:78-106`. If the owner wants (3) to stand on its own, the alternative is to sequence it before this one; this PR cannot keep the presets alive without the keys.
3. **`rules/` and `harness/` are moved whole, not deleted.** `git mv templates/rules rules` and `git mv templates/harness harness`, one path each in `.mise/tasks/rules/add:13-14` and `.mise/tasks/export/claude-code:18`; `test/rules_add.bats` (4) and `test/export.bats` (5) pass unchanged in substance. Their files keep the `.md.tmpl` names on purpose, so (2) and (4) delete directories rather than renamed files. The three markers stay three until (2).
4. **`--kind` and `--no-home` go now.** `--no-home`'s only non-test caller was the examples task, which goes here; `--kind` only let the caller contradict a derivation `add_agent` then refused. Both sit in the issue's `agent add` paragraph and in none of (2)–(4).
5. **The Stances.** Builder: the failing case first, the smallest diff under its directory, a PR body that names any gate not run. Judge: the diff before the description, the gates before the verdict, one report per entry. Each ends with the housekeeper's closing sentence, "Narrowing this stance is X's; widening it is the owner's."
6. **The merge rule** is asserted as a merge commit with branch history as the record — what `style/strict.md` already said, and what the housekeeper's and builders' briefs already assume.
7. **`doctor`'s empty-roster and no-housekeeper warnings stay** — a hand-edited house can still reach them — and are tested by emptying the roster by hand; the same move keeps `test/export.bats`'s empty-roster case.
8. **The two `next: house export` lines stay** (`init`, `agent add`), since the exporter still ships; the issue lists both under (4).
9. **The lineage record.** #16 (`61bc93a`) deleted `notes/lineage.md` and added a test that fails on any `lineage*` file, so the dated section the issue asks for has nowhere to go but git history — which is where #16's own `AGENTS.md` now says lineage lives. The commit message carries it: the style-as-opt-in and the markers were 2026-09-17's answer to #6, and this replaces "ask the owner" with "assert".
10. **`assert_file_says`** joins lines before matching, because the Stance and house-style sentences wrap; `assert_file_contains` stays for everything else.

## Left for (2)–(4)

- **(2) rules:** `rules/` (four `.md.tmpl`), `.mise/tasks/rules/add`, `test/rules_add.bats`, the `house:rules` marker and its checks in `.mise/tasks/doctor`, `skeleton/house/test/roster.bats`, `test/own_house.bats` and `test/doctor.bats`, the `house rules add <set>` sentence in the skeleton contract's "Domain rules", `house rules add money` in the lineage test, the "Domain rules" section of the README and the `rules add` bullet of `AGENTS.md`.
- **(3) presets:** nothing — decision 2.
- **(4) harness:** `harness/claude-code/`, `.mise/tasks/export/claude-code`, `test/export.bats`, the `export` arm of `test_helper.bash:5`, the two `next: house export` lines, the harness bullet in the skeleton contract's Tooling and the housekeeper note's harness sentence, `HOUSE_DEFINITIONS_DIR` (kept as the negative guard), the README's "One exporter still ships" paragraph and the `harness/` mentions in `AGENTS.md`.

## Where the issue's references had drifted

Against `8297513` every line reference in the issue was accurate. Against the actual base `61bc93a`, `AGENTS.md` and `README.md` carried #16's lineage edits, `test/own_house.bats` had one more test (so its `:45`, `:69-88`, `:90-98`, `:100-118` sit seven lines lower), and `notes/lineage.md` no longer exists.

## Gates

- `mise run test`: bats `1..55`, 55 ok (71 at `61bc93a`: −2 `examples.bats`, −11 `presets.bats`, −1 `doctor.bats`, −1 `init.bats`, −2 `agent_add.bats`, +1 `own_house.bats`); skeleton syntax pass ok.
- `git diff --check`: clean.
- Each new gate was shown to fail on a sentinel and pass on the clean tree: a plumbing key appended to a skeleton file; `{{OWNER}}` removed from `AGENTS.md`'s list; a `templates/` directory recreated; a `house:decide` marker in the skeleton; a `usage_style` reference in `init`.
- Outside bats: `house init x --owner 'Your Name' && house doctor --house x` prints `doctor: healthy` and exits 0; `house init y` with no owner and no `user.name` fails before writing anything.

## The owner's step after the last of the four merges

`v0.2.0`. This PR removes documented flags and a task (`--style`, `--with`, `--no-housekeeper`, `--kind`, `--no-home`, `examples`); (2) and (4) remove `rules add` and `export`. Tagged and released by the maintainer, with the removals named in the notes.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
