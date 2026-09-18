Closes #14. Cut from `main` at `8297513` (`v0.1.0`); every edit below is the issue's, applied against that commit.

## What changes

house-framework is the skeleton a house adopts, not a house. `notes/lineage.md` was the one file left wearing a house note's frontmatter under a house's directory, and the owner chose deletion over a root `LINEAGE.md`. After this PR, `lib/lineage-names` and git history are the only lineage artifacts, and a test keeps it so.

The eleven edits from the issue, in order:

1. `git rm notes/lineage.md`; `notes/` goes with it.
2. `AGENTS.md:3` — "no roster here, no queue and no `notes/`; a house's notes come only from `templates/`, and the households this shape was distilled from are named in `lib/lineage-names` and in git history, nowhere else." The paragraph is reflowed to fit.
3. `AGENTS.md:35-37` — "lives in git history, starting at the bootstrap commit".
4. `AGENTS.md:41-44` — "Personal names and lineage names appear in `lib/lineage-names` alone, the list `doctor` reads".
5. `AGENTS.md:114-116` — drop "(`notes/lineage.md`)".
6. `README.md:109-112` — the paragraph the issue gives.
7. `README.md:137-140` and `:245-248` — no change, as the issue says.
8. `test/own_house.bats:20-21` — test renamed; `--exclude=lineage.md` dropped, so the name grep now covers every file but `lib/lineage-names`.
9. New test "the framework is a bootstrap, not a house: no notes/, no lineage file", with the four assertions from the issue.
10. `.gitignore` — `.obsidian` removed.
11. The commit message the issue gives, signed.

Nothing under `templates/` or `examples/` changes.

## One edit beyond the issue's list

`AGENTS.md:48-49` (at `8297513`) said the repo-wide test "greps every file but those two" — the note and `lib/lineage-names`. Edit 4 removes the note from that sentence's antecedent and edit 8 removes it from the test, so "those two" would read false. Changed to "every file but that one". It is in the same bullet edit 4 rewrites and describes the test edit 8 changes, so it is within the issue's scope; listed here because it is not one of the eleven.

## Gates

- `mise run test`: bats `1..71`, 71 ok, 0 not ok (was 70 at `8297513`; the new test is #51); templates ok; `examples/` matches a fresh render.
- `git diff --check`: clean.
- The widened grep in edit 8 was run against `8297513` before the deletion: its only hits were inside `notes/lineage.md`, so the residue pass in the issue holds and nothing else needed an exclude.
- The new test was checked to fail with a `notes/x.md` put back and with a `docs/LINEAGE.md` added, and to pass on the branch.
