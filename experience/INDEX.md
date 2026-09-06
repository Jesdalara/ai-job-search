# Experience index — router

`/apply` Step 2 reads this file, matches the posting's requirement list against the table below, and
then reads **only the one or two experience files that match**. Reading the whole folder defeats the
purpose: these files are deliberately unsummarised, and a model given all of them writes vaguer
bullets than one given the right subset.

> **This file ships as a placeholder.** It has no real role files behind it yet. Run `/setup`, or
> write `experience/NN-<employer>-<role>.md` files by hand using the skeleton in `experience/README.md`,
> then replace every `[BRACKETED]` row below with your own. `/recall` (`.claude/commands/recall.md`)
> keeps this router in sync afterward — when it resolves a fact to a file with no matching row here,
> it adds one instead of leaving the fact unreachable.

## The files

| File | Role | Period | Weight |
|---|---|---|---|
| `01-[employer]-[role-slug].md` | [JOB_TITLE_1] | [YEAR_START] – [YEAR_END] | [Why a drafter should default here — e.g. largest role by scope or duration] |
| `02-[employer]-[role-slug].md` | [JOB_TITLE_2] | [YEAR_START] – [YEAR_END] | [What this file is the best or only source for] |
| `03-[employer]-[role-slug].md` | [JOB_TITLE_3] | [YEAR_START] – [YEAR_END] | [What this file is the best or only source for] |

---

## Keyword router

Match on the posting's own terms. Where two files are listed, the first leads and the second
supports.

| If the posting asks for… | Read | Go straight to |
|---|---|---|
| [PRIMARY_SKILL_OR_STACK] | `01` | §[N] |
| [SECONDARY_SKILL] | `02`, `01` | `02` §[N] ([what it is evidence of]), `01` §[N] ([supporting detail]) |
| **[A CAPABILITY YOU LACK DIRECT EXPERIENCE IN]** | `0N` | **Start at `01-candidate-profile.md` → "[the section documenting how you acquire unfamiliar tools/frameworks]"**, then the file and section with the nearest genuine adjacency. Demonstrate the sequence honestly, never assert "fast learner", and never phrase it as "whatever the job required" |
| [DOMAIN_OR_INDUSTRY] | `0N`, `0M` | Both — name what each file uniquely supports |
| **[A THEME WORTH CALLING OUT EXPLICITLY]** | `0N` | §[N]. [One line on why this is a standout theme in the profile] |
| **[SOMETHING YOU DID ADJACENT TO BUT DID NOT OWN]** | `0N` | §[N]. **Always include the honest boundary:** [what you did not do, stated plainly] |

Add a row per capability, tool, or theme a posting is likely to ask about — one row is cheap; a
missing one means `/apply` reads the wrong file or skips the folder's best evidence entirely.

---

## Rules that apply to every read

1. **Provenance tags bind.** `[evidence]` and `[attested]` may be used. **`[to-confirm]` may not
   reach a CV or cover letter** — surface it to the user instead.
2. **`Do NOT say` sections bind.** Every file opens with one. Those are retired exaggerations still
   present in LinkedIn and older CVs; reintroducing one is a grounding failure.
3. **Depth ratings bind.** DEEP / WORKING / EXPOSURE. An EXPOSURE technology is never presented as
   owned.
4. **Honest boundaries are assets, not liabilities.** A file that states plainly what you did *not*
   do — the layer you didn't own, the system you extended rather than built — makes everything
   adjacent to that boundary more credible. Say those boundaries out loud where a posting touches
   them, rather than treating them as things to omit.
