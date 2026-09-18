No existing house changes: `init` copies and never links, so a house made before this lands is untouched. A house that carries the old `house:rules` marker keeps it; `doctor` simply stops looking for it, and a rule set already inserted stays where it is.

PR (2) of the four the issue splits into — rules. Refs #15; (1) was #18, (3) is nothing (#18's decision 2 deleted the presets), and (4) harness is its sibling, cut from the same `main`. Cut from `main` at `adf7622` (the merge of #20). This PR and (4) both touch `README.md`, `AGENTS.md`, `test/surface.bats` and `test/test_helper.bash` on neighbouring lines; whichever merges second rebases, and neither depends on the other.

## What changes

- `rules/` (four `.md.tmpl`), `.mise/tasks/rules/add` and `test/rules_add.bats` (4 tests) are deleted. The shipped text was one household's answers, and the repository's own rule forbids shipping those; the ruling makes it final and removes the reason to keep a task whose only job was copying a file the framework no longer has.
- The `<!-- house:rules -->` marker goes with the task that inserted at it. `.mise/tasks/doctor` and `scaffold/house/test/roster.bats` check two markers, `house:roster` and `house:read-first`, both used by `agent add`. `scaffold/house/AGENTS.md` no longer carries the marker line.
- The scaffold contract's "Domain rules" section stays as an assertion and loses the `house rules add <set>` sentence: a rule set binds the agent whose charge it names, is written into the contract when an agent's mistakes would be permanent or expensive, and takes one shape — a heading that names the set, a line that names the agent it binds, then five or six lines each a constraint the code can be checked against. "The framework ships none; it does not know your domain, and a rule nobody can check is noise."
- `lib/house.sh` loses `render_string`; `rules add` was its only reader.
- Tests: `test/own_house.bats` gains `[ ! -e rules ]` and extends the repo sweep of `scaffold/`, `lib/` and `.mise/` to `house:rules` and `rules add`; the lineage test no longer runs `house rules add money`, and the contract test lists two markers. `test/doctor.bats`'s "marker or authority section gone" case deletes `house:read-first` instead. `test/surface.bats` lists `agent:add`, `doctor`, `export:claude-code`, `init`, `test` (hidden), `version`. `test/test_helper.bash`'s task arm is `agent|export`.
- Docs, against the tree as this PR leaves it: `README.md`'s "Domain rules" section says where a rule set goes and that none ships, the `init` table row reads "a Domain rules section for you to write into", and the surface sentence drops `rules add`; `AGENTS.md`'s "three markers" bullet is "two markers" and its "last menus" bullet names `harness/` alone, awaiting (4). `CONTRIBUTING.md` had nothing to change.

## Decisions the issue left to judgement

1. **The section names the shape.** With no command to produce a rule set, the contract's paragraph is the only place a reader learns what one looks like, so it states the shape in one sentence — heading, binding line, five or six checkable lines — instead of pointing at a task.
2. **`render_string` goes.** The issue lists the task and its test; the helper had no other caller, and #18 followed the same rule for the preset helpers.
3. **`doctor` does not fail a house that still has the marker.** The check is for what must be present, not for what must be absent; an old house keeps its marker and stays healthy.
4. **The `.tmpl` sweep stays scoped to `scaffold/`.** `harness/claude-code/` still carries three `.md.tmpl` until (4); the repo-wide "no `.tmpl` anywhere" guard belongs there.

## Gates

- `mise run test` at `8891802`: bats `1..60`, 60 ok (64 at `adf7622`, −4 `rules_add.bats`); scaffold syntax pass ok.
- `git diff --check`: clean.
- The extended gate was shown to fail on a sentinel and pass on the clean tree: an empty `rules/` directory recreated; a `<!-- house:rules -->` line appended to a scaffold note.
- Outside bats: `house init x --owner 'Your Name' && house doctor --house x` prints `doctor: healthy` and exits 0; the rendered contract contains no `house:rules`.
- Measured from a plain clone of the branch. In a `git worktree`, `.git` is a file, and the lineage sweep in `test/own_house.bats:16` (`--exclude-dir=.git`) reads its `gitdir:` line and fails on the path; that is the test's, not this change's, and a one-word `--exclude=.git` would fix it. Left out here as outside the issue's scope.

## The owner's step after the last of the four merges

`v0.2.0`. This PR removes a documented command (`rules add`); #18 removed `--style`, `--with`, `--no-housekeeper`, `--kind`, `--no-home` and `examples`; (4) removes `export`. Tagged and released by the maintainer, with the removals named in the notes; the issue closes with the tag, not with any one of the four.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

