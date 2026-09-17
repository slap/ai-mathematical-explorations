# Contributing

Two audiences: mathematicians who want to check something, and the maintainer of the archive.

## Reviewing an exploration

Open an [issue](../../issues/new/choose). The templates ask for what a later reader needs:
which exploration, which claim, what you did, what you concluded.

Useful contributions include, in rough order of how much they change an exploration's status:

- a complete check of the argument, step by step;
- a check of one step, one lemma or one special case;
- a counterexample, or an error with the line where it occurs;
- a reference showing the result, or a stronger one, is already known;
- a formalisation in a proof assistant;
- an improvement, simplification or generalisation of the argument.

Partial and negative results are worth reporting. "I checked Section 2 and stopped at the
dimension count, which I could not follow" is more useful to the next reader than silence.

There is no review process behind this, no editor and no queue. Issues are the record; the
exploration page is updated to point at them.

## Verification status

| Status | What it takes |
| --- | --- |
| 🟠 Unverified | The default. The material is published as generated. |
| 🟡 Partially verified | A documented check covers part of the argument, or the claim holds under extra hypotheses. The page says which part, and what remains open. |
| 🟢 Verified | A documented, complete mathematical check of the main claim, signed by a named reviewer, or a machine-checked formalisation. |
| 🔴 Refuted | A documented error that invalidates the main claim, or an explicit counterexample. |
| ⚪ Superseded | A later exploration replaces this one. Both pages link to each other. |

Three things that do **not** move an exploration to *Verified*:

- the maintainer reading it and finding it plausible;
- computational evidence in small cases, including checks run by the AI itself;
- the absence of objections.

Every status other than *Unverified* must cite the issue, document or formalisation that
supports it, in the *Verification record* table of the exploration page. Status can move in
both directions; the table keeps the history.

## Adding an exploration (maintainer)

1. Copy [`explorations/_template/`](explorations/_template/) to
   `explorations/NNN-short-slug/`, with `NNN` the next number.
2. Drop in `exploration.pdf`, `source.tex` and `ai-output.md`. `ai-output.md` holds the AI
   output as produced, plus the prompts and the context of the conversation. Do not edit it
   silently: editorial corrections belong in `source.tex`, and the header of that file lists
   them. Remove nothing without saying so in the file.
3. Fill `metadata.yml` and write the page body of `README.md` — summary, claim, context.
4. Run `python tools/build_index.py`. It rewrites the index in the main README and the
   header block of every exploration page from the metadata, then checks that local links
   and expected files exist. No dependencies beyond the standard library.
5. Commit. One exploration, one commit.

Before publishing anything, check it carries no private material: unrelated conversation,
unpublished work of third parties, personal data, credentials, file paths from a private
machine.

### Updating a status

Edit `status:` in `metadata.yml`, add a line to the *Verification record* table of the
exploration page, and run `python tools/build_index.py` again. Nothing else changes.

### Later versions

A revised version of an exploration is a new exploration with a new number, linked with
`supersedes:`/`superseded_by:` in the metadata of both. The old one stays: it is part of the
record. Small editorial fixes are just commits.

## Releases and archiving

The repository is meant to be archivable on Zenodo and to receive a DOI. Tag a release when
a batch of explorations is added or a status changes materially; `CITATION.cff` carries the
version and date of that release. Nothing in the repository depends on an external service
being alive.
