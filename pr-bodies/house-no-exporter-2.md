No existing house changes: `init` copies and never links, so a house made before this lands is untouched. A definition already exported is a file outside the house and stays where it is.

Re-lands #22 (PR (4) of the four the issue splits into — harness), which was merged as `0c5070b` and reverted by the maintainer as `062f8c4` on 2026-09-18 so that #21 (rules) could land first. Refs #15; (1) was #18, (2) is #21, merged at `4100b06`, and (3) is nothing (#18's decision 2 deleted the presets). Cut fresh from `main` at `4100b06` — after #21 — as one signed commit, `840d410`, which is `8718bba` reapplied against the tree #21 left. This is the last of the four.

## What changes

- `harness/claude-code/` (three `.md.tmpl`), `.mise/tasks/export/claude-code` and `test/export.bats` (5 tests) are deleted. With `templates/` gone the exporter had no source but the three files moved out whole; the two consistent endpoints were a runner asserted by the framework or no exporter at all, the first contradicts the harness-agnostic rule, and the maintainer took the second.
- The two `next: house export …` lines go: `init`'s and `agent add`'s.
- The contract-only "Harnesses" statement is what remains, in three places. `README.md`'s "Harnesses" section: what a runner needs is already in the house (`roster.tsv`, each home's `AGENTS.md` as the brief, the housekeeper's file named after the house), its definition is written outside the house by the owner, the contract makes it Tier 2, nothing in this repository writes one, and the framework names no runner. The scaffold contract's Tooling bullet "A harness, if any" says the same without `house export <harness>`. The housekeeper's note checks a harness's definitions "where a harness is in use" as the owner's, written outside the house.
- `HOUSE_DEFINITIONS_DIR` stays in `test/test_helper.bash`, and the `[ -z "$(ls -A "$DEFINITIONS_DIR")" ]` assertions in `test/init.bats` and `test/agent_add.bats` stay, as the negative guard the issue asked for: the directory a runner would be written to is asserted empty after `init` and `agent add`. `test/doctor.bats`'s "never looks for a harness" case is unchanged.
- The last runner name in the tree was the guard in `test/agent_add.bats` that greps a fresh house and home for it. It moves to `lib/lineage-names` as a `runner` line — the one file names may live in — and the test reads it from there. `lineage_names()` and `doctor` read only the `house` lines, so a generated house is not checked for it; the repo-wide sweep in `test/own_house.bats` reads every line, so the name is now refused anywhere else in this repository.
- `lib/house.sh` loses `capitalize`; the exporter was its only reader.
- Tests: `test/own_house.bats` gains `[ ! -e harness ]` beside #21's `[ ! -e rules ]`, a repo-wide `find` for `*.tmpl` (pruning `.git` only), and extends the sweep of `scaffold/`, `lib/` and `.mise/` to `house export`, `HOUSE_DEFINITIONS_DIR` and `harness/` alongside #21's `house:rules` and `rules add`. `test/surface.bats` lists `agent:add`, `doctor`, `init`, `test` (hidden), `version`. `test/test_helper.bash`'s task arm is `agent` alone.
- Docs, against the tree as this PR leaves it: `README.md` loses "One exporter still ships", "and every exporter" in the roster row, "Exported definitions are kept the same way", `export <harness>` from the surface sentence, and says what `HOUSE_DEFINITIONS_DIR` is for in the tests; the housekeeper paragraph reads "a runner's definition for it, where one exists, is named after the house". `AGENTS.md`'s strangers bullet says where the runner name lives and that no harness is named anywhere else; the housekeeper bullet drops "each harness's `definition.housekeeper`"; the harness-agnostic bullet says nothing here writes a runner's files and "do not add an exporter"; the never-overwritten bullet drops the exporter; the "last menu in the tree" bullet is deleted. `CONTRIBUTING.md`'s closing line ("or to run any particular agent harness") was already true and stays.

## What differs from #22, because #21 is now in

#22's body predicted "both deletions" conflicts in `AGENTS.md`, `README.md`, `test/own_house.bats`, `test/surface.bats` and `test/test_helper.bash`, and those are the five files that needed a hand on the reapply. Each resolution is what its decision 3 said the second of the two would do:

- **The `.tmpl` check is the whole tree.** #22 pruned `rules/` from the repo-wide `find` because `rules/` still held four `.md.tmpl` until #21 landed. It has; the prune is dropped. `find . -name '*.tmpl'` on this branch is empty.
- **The "last menu" bullet goes.** #22 repointed `AGENTS.md`'s "Working here" bullet at `rules/` "awaiting #21", and #21 repointed it at `harness/` awaiting this. With both gone there is nothing left to name, so the bullet is deleted rather than kept pointing at an empty set.
- **`test/surface.bats`** lists neither `rules:add` (gone in #21) nor `export` (gone here); its title says so.
- **`test/test_helper.bash`'s task arm** is `agent` alone, not `agent|rules` (#22) or `agent|export` (#21).
- **`README.md`** keeps #21's wording for the `AGENTS.md` row ("a Domain rules section for you to write into") and drops "and every exporter" from the roster row; the surface sentence reads `init`, `doctor`, `version` and `agent add`.

Everything else in `8718bba` applied without conflict. Decisions 1, 2, 4 and 5 of #22 stand as written; decision 3 is discharged above.

## Gates

- `mise run test` at `840d410`: bats `1..55`, 55 ok (60 at `4100b06`, −5 `export.bats`); scaffold syntax pass ok. The BW01 warning from `test/environment.bats` (a `run` that expects exit 127) is on `main` too and is not this change's.
- `git diff --check`: clean.
- The extended gate was shown to fail on a sentinel and pass on the clean tree: an empty `harness/` directory recreated, and a `.tmpl` file under `scaffold/` — both caught by the one test now that nothing is pruned but `.git`.
- Outside bats: `house init y --owner 'Your Name'`, then `house agent add builder --role implementation --owns src/`, then `house doctor --house y` prints `doctor: healthy` and exits 0; neither `next:` list mentions an export, and `HOUSE_DEFINITIONS_DIR` is still empty afterwards.
- `find . -name '*.tmpl'` on the branch is empty; `harness/`, `rules/`, `templates/` and `examples/` are all absent.
- Measured from a plain clone, for the reason #21's body gives: in a `git worktree`, `.git` is a file and the lineage sweep at `test/own_house.bats:16` reads its `gitdir:` line.

## The owner's step after this merges

`v0.2.0`. This is the last of the four: this PR removes a documented command (`export claude-code`); #21 removed `rules add`; #18 removed `--style`, `--with`, `--no-housekeeper`, `--kind`, `--no-home` and `examples`. Tagged and released by the maintainer, with the removals named in the notes; the issue closes with the tag.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
