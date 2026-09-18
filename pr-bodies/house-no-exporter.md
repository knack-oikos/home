No existing house changes: `init` copies and never links, so a house made before this lands is untouched. A definition already exported is a file outside the house and stays where it is.

PR (4) of the four the issue splits into — harness. Refs #15; (1) was #18, (2) rules is #21, its sibling cut from the same `main`, and (3) is nothing (#18's decision 2 deleted the presets). Cut from `main` at `adf7622` (the merge of #20). This PR and #21 both touch `README.md`, `AGENTS.md`, `test/surface.bats`, `test/test_helper.bash` and `test/own_house.bats` on neighbouring lines; whichever merges second brings `main` in with a merge commit, and neither depends on the other.

## What changes

- `harness/claude-code/` (three `.md.tmpl`), `.mise/tasks/export/claude-code` and `test/export.bats` (5 tests) are deleted. With `templates/` gone the exporter had no source but the three files moved out whole; the two consistent endpoints were a runner asserted by the framework or no exporter at all, the first contradicts the harness-agnostic rule, and the maintainer took the second.
- The two `next: house export …` lines go: `init`'s and `agent add`'s.
- The contract-only "Harnesses" statement is what remains, in three places. `README.md`'s "Harnesses" section: what a runner needs is already in the house (`roster.tsv`, each home's `AGENTS.md` as the brief, the housekeeper's file named after the house), its definition is written outside the house by the owner, the contract makes it Tier 2, nothing in this repository writes one, and the framework names no runner. The scaffold contract's Tooling bullet "A harness, if any" says the same without `house export <harness>`. The housekeeper's note checks a harness's definitions "where a harness is in use" as the owner's, written outside the house.
- `HOUSE_DEFINITIONS_DIR` stays in `test/test_helper.bash`, and the `[ -z "$(ls -A "$DEFINITIONS_DIR")" ]` assertions in `test/init.bats` and `test/agent_add.bats` stay, as the negative guard the issue asked for: the directory a runner would be written to is asserted empty after `init` and `agent add`. `test/doctor.bats`'s "never looks for a harness" case is unchanged.
- The last runner name in the tree was the guard in `test/agent_add.bats` that greps a fresh house and home for it. It moves to `lib/lineage-names` as a `runner` line — the one file names may live in — and the test reads it from there. `lineage_names()` and `doctor` read only the `house` lines, so a generated house is not checked for it; the repo-wide sweep in `test/own_house.bats` reads every line, so the name is now refused anywhere else in this repository.
- `lib/house.sh` loses `capitalize`; the exporter was its only reader.
- Tests: `test/own_house.bats` gains `[ ! -e harness ]`, a repo-wide `find` for `*.tmpl` (pruning `.git` and `rules/`), and extends the sweep of `scaffold/`, `lib/` and `.mise/` to `house export`, `HOUSE_DEFINITIONS_DIR` and `harness/`. `test/surface.bats` lists `agent:add`, `doctor`, `init`, `rules:add`, `test` (hidden), `version`. `test/test_helper.bash`'s task arm is `agent|rules`.
- Docs, against the tree as this PR leaves it: `README.md` loses "One exporter still ships", "and every exporter" in the roster row, "Exported definitions are kept the same way", `export <harness>` from the surface sentence, and says what `HOUSE_DEFINITIONS_DIR` is for in the tests; the housekeeper paragraph reads "a runner's definition for it, where one exists, is named after the house". `AGENTS.md`'s strangers bullet says where the runner name lives and that no harness is named anywhere else; the housekeeper bullet drops "each harness's `definition.housekeeper`"; the harness-agnostic bullet says nothing here writes a runner's files and "do not add an exporter"; the never-overwritten bullet drops the exporter; the "last menus" bullet names `rules/` alone, awaiting #21. `CONTRIBUTING.md`'s closing line ("or to run any particular agent harness") was already true and stays.

## Decisions the issue left to judgement

1. **The runner name goes into `lib/lineage-names`, not out of the tree.** The alternative was to delete the assertion in `test/agent_add.bats`, which weakens a guard. A `runner` kind in the file the repo already reserves for names keeps the guard, and turns "no harness is named outside these two directories" into "no harness is named anywhere but this file", tested repo-wide.
2. **`doctor` does not reject the runner name in a house.** `lineage_names()` keeps reading `house` lines only. A house whose owner runs it under that runner may say so in its own notes; that is the owner's text, not the framework's leftover.
3. **The `.tmpl` check prunes `rules/`.** Each of the two remaining PRs must stand alone on `main` in either order, and `rules/` still holds four `.md.tmpl` until #21 lands. Once both have merged the prune is dead and the check is the whole tree; whichever of the two lands second drops it in its merge of `main`.
4. **`capitalize` goes**, as `render_string` does in #21: no other reader.
5. **The scaffold contract's Tier 2 bullet "The agent definitions a harness reads" stays as written.** It names no runner and no exporter; it is the contract's own statement that a definition is Tier 2, and the Harnesses section points at it.

## Gates

- `mise run test` at `8718bba`: bats `1..59`, 59 ok (64 at `adf7622`, −5 `export.bats`); scaffold syntax pass ok.
- `git diff --check`: clean.
- The extended gate was shown to fail on a sentinel and pass on the clean tree: an empty `harness/` directory recreated; a `.tmpl` file under `scaffold/`; a `house export` line appended to a scaffold note; the runner name written into a scaffold note (the repo-wide sweep).
- Outside bats: `house init y --owner 'Your Name'`, then `house agent add builder --role implementation --owns src/`, then `house doctor --house y` prints `doctor: healthy` and exits 0; neither `next:` list mentions an export, and `HOUSE_DEFINITIONS_DIR` is still empty afterwards.
- `find . -name '*.tmpl'` on the branch lists the four under `rules/` and nothing else.
- Measured from a plain clone of the branch, for the reason #21's body gives: in a `git worktree`, `.git` is a file and the lineage sweep at `test/own_house.bats:16` reads its `gitdir:` line.

## The owner's step after the last of the four merges

`v0.2.0`. This PR removes a documented command (`export claude-code`); #21 removes `rules add`; #18 removed `--style`, `--with`, `--no-housekeeper`, `--kind`, `--no-home` and `examples`. Tagged and released by the maintainer, with the removals named in the notes; the issue closes with the tag, not with any one of the four.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

