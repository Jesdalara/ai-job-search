# Experience — Source of Truth

One file per role — or per continuous engagement, where a single narrative spans a promotion and
splitting it would fragment the story. Each file holds the **full, unsummarised account** of what
happened there. Nothing here is written to be read by an employer. It is written so that a drafting session
with a job posting in hand can find the two or three things that actually match, in the candidate's
own detail, instead of reshuffling five generic bullets.

**Never tracked by git once populated.** This template ships `README.md`, `INDEX.md` (a placeholder
router) and `00-example-role.md` (a worked example) so a fresh clone shows what the layer looks like.
`.gitignore` ignores everything else you add under `experience/` — real role files, a real `INDEX.md`
you write over the placeholder, a real `experience_raw/` folder — because they carry former-employer
internals and the candidate's unpolished account of their own work. Keep it that way.

---

## Why this exists

`/apply` grounds every factual claim against a fixed set of sources and strips anything it cannot
find there. Before this folder, that set was a ~2 KB summary: three to five bullets per role. Detail
that never made it into those bullets was, by the framework's own rules, unusable — the drafter
either wrote something bland or wrote something true that the reviewer then deleted as a
fabrication.

The compression from "everything that happened" down to "what fits on two pages" has to happen
**at draft time, when the posting is known** — not once at setup time, blind. This folder is the
uncompressed side of that.

`01-candidate-profile.md` stays as the index and the quick-reference summary. These files are the
detail behind it. Both are sources of truth; they must not contradict each other.

---

## Getting started

`/setup` does not populate this folder — it writes `01-candidate-profile.md` and the other summary
files, but nothing in it currently generates an `experience/NN-*.md` file. These files are written by
hand, or added later via `/recall`:

1. Write role files using the **File skeleton** below — one `NN-<employer>-<role>.md` per role, most
   senior detail first.
2. Replace `INDEX.md`'s placeholder rows and keyword-router table with real entries pointing at your
   files and sections.
3. From then on, use `/recall` to add a remembered fact without degrading the files — see
   `.claude/commands/recall.md`.
4. Delete or rewrite `00-example-role.md` once you have real files of your own; it exists only to show
   the shape.

---

## Source precedence — read this before writing any file

If you keep raw material behind these files — old dossiers, evidence exports, past CVs — it is
**not** of uniform quality, and the noise tends to flow in one direction: a LinkedIn profile and
recent tailored CVs are often themselves written *from* earlier, more careful accounts, and they
escalate along the way. Synthesising all sources as equals launders those escalations into the
source of truth, where everything downstream then inherits them as "verified".

**The rule: evidence outranks self-description, and self-description outranks a tailored CV.
Never the reverse.**

| Tier | Source (example) | Authoritative for | Treat with care |
|------|--------|-------------------|-----------------|
| 1 | An evidence dossier built from commits, tickets, PRs, or reports, with an explicit "could NOT confirm" convention | Everything it covers | — |
| 1 | Artifact-level notes (repos, projects, deliverables) | Depth calibration (owned vs. touched) | — |
| 2 | An older self-written CV | The only decent record of an earlier period | Self-reported, unevidenced, and it may *undersell* as easily as it inflates |
| 3 | A current LinkedIn export | Dates, employer names, job titles — the public record an employer will cross-check | A marketing surface. Noisy on scope and impact |
| 3 | Recent tailored CVs | **Structure and tone only. Never a source of facts** | A tailored output, not a source. Carries the escalated version of nearly every claim |

The last row is the framework's own rule, not a new one: `/setup` Path A already warns that archived
drafts are "tailored outputs, not source documents… a tailored draft that drifted must never become
a template future applications start from."

---

## Provenance tags — every claim carries one

- **`[evidence]`** — traceable to an artifact: a commit, a work item, a PR, a document, a report.
  Safe to put on a CV as stated.
- **`[attested]`** — the candidate states it and it is credible, but nothing outside their account
  supports it. Usually true; usually non-code work (leadership, culture, influence). Safe to use,
  but expect to be asked for specifics in an interview.
- **`[to-confirm]`** — a number, date, or scope that no source pins down, or where sources
  disagree. **Do not put a `[to-confirm]` claim on a CV until it is resolved.** Resolve it and
  re-tag it; do not quietly promote it.

A claim with no tag is a bug in the file.

## Technology depth — three levels, not a flat list

A flat skills list is what makes CVs interchangeable. Rate each technology by what the evidence
actually supports:

- **DEEP** — owned it, sustained, hands-on, would defend a design decision in it under questioning.
- **WORKING** — shipped real work in it, not the primary tool.
- **EXPOSURE** — read it, debugged around it, understand the boundary. **Never claim more.**

---

## File skeleton

Each `NN-<employer>-<role>.md` follows this structure:

```markdown
# <Role> — <Employer> (<start> – <end>)

## 0. Do NOT say
Claims that appear in older CVs, LinkedIn, or past drafts that this file
supersedes — with the accurate version and why the other one is wrong.
The single most important section in the file: it is what stops a retired
exaggeration from reappearing in the next application.

## 1. Context and scope
The business, the product, the team, the working model, where this role sat.

## 2. Systems owned
What the candidate was actually responsible for, and the boundary of it.

## 3. Projects and problems
The narrative core. Per item: what the situation was, what was hard about it,
what was actually done, what happened as a result, and what it is evidence of.
Explicit and long. This is the section that must not be summarised.

## 4. Technology
Grouped DEEP / WORKING / EXPOSURE, each with what it was used for.

## 5. Metrics
Every number, each with its provenance tag and what it does and does not mean.

## 6. People and influence
Mentoring, leadership, cross-team work, standards set. Mostly [attested].

## 7. Open questions
What the candidate still needs to pin down before this material is CV-ready.
```

See `00-example-role.md` for this skeleton filled in with a worked (fictional) example.

---

## How this reaches a CV

`/apply` Step 1 extracts the posting's requirements. Step 2 then reads `INDEX.md`, resolves which
one or two experience files are relevant, and reads only those — not the whole folder. Reading every
file on every run is not the goal and would defeat the purpose: a model given 40 KB of narrative
writes vaguer bullets than one given the right 4 KB.

These files are named in the `/apply` grounding contract, so material drawn from them survives the
Factual Grounding Audit instead of being stripped.

---

## Maintenance

When a fact surfaces in an interview, a conversation, or a `/apply` run — a metric recalled, a scope
corrected, a project remembered — it goes in the relevant file here **in the same turn**, tagged.
The framework's standing rule ("a fact that exists only in chat will be treated as unsupported by a
later session") applies to this folder exactly as it applies to `01-candidate-profile.md`.
