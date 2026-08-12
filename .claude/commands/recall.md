# /recall - Capture a Remembered Fact into the Source of Truth

The user has remembered something about their experience and wants it recorded. The raw fact arrives
as `$ARGUMENTS` (or, if empty, ask for it).

**This is not an append operation.** Pasting a fact at the end of a file degrades the source of truth
a little each time — that is exactly what this command exists to prevent. A recorded fact must land in
the right file and section, carry a provenance tag, resolve or contradict what is already there
explicitly, and propagate to the summary layer when it belongs there.

Follow these steps **exactly in order**.

---

## Step 0: Get the fact

If `$ARGUMENTS` is empty, ask: *"What did you remember? Give it to me raw — I'll place it and tag it."*

Do not clean it up, shorten it, or turn it into a CV bullet at this stage. Preserve the user's own
words and detail; the whole point of `experience/` is that it is unsummarised.

---

## Step 1: Read before writing

Read, in parallel:
- `experience/README.md` — the provenance tags, depth ratings, and precedence rules
- `experience/INDEX.md` — to resolve which file the fact belongs to

Then read **only the experience file the fact concerns**. If the fact spans two roles, read both.

If the fact plainly concerns a role that has no file yet, say so and offer to create one from the
skeleton in `experience/README.md` rather than filing it somewhere it does not belong.

---

## Step 2: Classify the fact

Decide which of these it is. The answer determines everything downstream.

| Type | Meaning | Where it goes |
|---|---|---|
| **New** | Nothing in the file covers it | A new entry in the appropriate existing section |
| **Enriches** | Adds detail, a metric, or a name to something already recorded | Woven into the existing passage, not appended after it |
| **Resolves** | Answers an item in the file's §Open questions | Two edits — see Step 4 |
| **Contradicts** | Disagrees with something already in the file | **Stop. Ask the user.** See Step 3 |
| **Retires a claim** | Reveals that something said elsewhere (LinkedIn, an old CV, a past draft) is wrong | The file's §0 `Do NOT say` table, plus wherever the accurate version lives |

A single remembered fact is often two of these at once — commonly *New* plus *Resolves*. Handle both.

---

## Step 3: Surface contradictions, never resolve them silently

If the fact disagrees with what is already recorded, do not overwrite. Present it:

```
## Conflict

**Currently in experience/<file>.md, §<section>:**
<quote the existing text>
*(tagged `[<tag>]`, sourced from <source>)*

**What you just told me:**
<the new fact>

Which is right? Or is this a case where both are true and the existing wording is too narrow?
```

Wait for the answer. A contradiction against an `[evidence]`-tagged claim deserves extra care — the
evidence came from commits, work items or documents, so a memory disagreeing with it is worth pausing
on. Say so rather than assuming the newer statement wins.

---

## Step 4: Assign the tag, and propagate

**Tag the new material** per `experience/README.md`:
- `[evidence]` only if the user points at an artifact — a document, a report, a work item, a commit
- `[attested]` for a fact the user states from memory. **This is the default for `/recall`**
- `[to-confirm]` if the user is unsure of a number, date or scope, or says so

Never promote a fact to `[evidence]` because it sounds precise. Precision is not provenance.

**If the fact resolves an open question**, make both edits in the same turn:
1. Write the resolved fact into the relevant section with its tag
2. **Remove the item from §Open questions**, or narrow it to whatever remains unresolved

An open question that stays open after being answered is how a source of truth rots.

**If the fact retires a claim** that appears in LinkedIn, an old CV, or a past draft, add a row to the
file's §0 `Do NOT say` table: the retired claim, where it lives, and the accurate version.

**If the fact changes a technology's real depth**, move it between DEEP / WORKING / EXPOSURE rather
than adding it twice.

---

## Step 5: Decide whether it reaches the summary layer

Most facts stay in `experience/` only. A fact goes up to `01-candidate-profile.md` — and to
`CLAUDE.md`'s Candidate Profile section — when it is one of:

- A new employer, role, title, or date change
- A new certification, award, publication, or language
- A headline-grade achievement or metric that belongs in the profile's role summary
- A skill genuinely new to the profile, not a detail of an existing one
- A correction to anything already in either file

Otherwise leave it in `experience/`. The summary layer stays a summary; that is what makes the
retrieval in `/apply` Step 2 worth doing.

**If it does go up**, edit all the places it lives, in the same turn. `01-candidate-profile.md` and
`CLAUDE.md` disagreeing with each other trips `/apply`'s profile-consistency warning on the next run.

---

## Step 6: Show the diff, then write

Present what you intend to change **before** writing:

```
## Proposed

**experience/<file>.md**
  §<section> — <new | enriched | resolved>: <the text you will add>, tagged `[<tag>]`
  §Open questions — removing item <N> (now answered)

**01-candidate-profile.md** *(if applicable)*
  <what changes and why it qualifies for the summary layer>

Apply?
```

Wait for confirmation. Then apply with the Edit tool — **targeted edits only, never a file rewrite.**

---

## Step 7: Report

State what changed, per file. If the fact was left out of the summary layer, say so and why — the user
should know the difference between "recorded in depth" and "will show up on a CV".

If the fact is `[to-confirm]`, close by naming what would confirm it. That is usually a document the
user already has.

---

## Design Principles

- **Placement over appending.** The value of these files is their structure. A fact in the wrong
  section is worth less than no fact, because it will not be found when a posting needs it.
- **Contradictions go to the user.** Never silently pick a winner, and never pick the newer statement
  by default over an evidence-backed one.
- **Open questions are a closed loop.** Answering one means deleting it, in the same turn.
- **The summary layer stays summary.** Not everything goes up. Deciding is part of the job.
- **`[attested]` is the honest default.** A remembered fact is a remembered fact — that is perfectly
  usable, and mislabelling it as evidence costs credibility in the one place it matters, an interview.
