# Goldfish review protocol

How the Elephant (the main agent) gets both guides reviewed by Goldfish (fresh-context subagents) and what it does with the findings.

## Why the reviewers start from nothing

You wrote the guides with the whole repository in your head. Where a sentence is vague, you fill the gap without noticing. A reviewer that shares your context does the same, and agrees with your mistakes. A reviewer with only the guide in front of it must rely on what the page says, which is the position of the real reader.

So each reviewer is a **new** subagent, and its task contains only the paths below. Do not include your fact sheets, your repo map, a summary of the project, or a hint about what you are unsure of.

## The three reviewers

Spawn all three in one turn so they run in parallel. Use absolute paths.

### Accuracy: `repo-documenter:goldfish-accuracy`

```text
Review these two guides against the repository.
Developer guide: [absolute path]/DEVELOPER_GUIDE.md
User guide: [absolute path]/USER_GUIDE.md
Repository root: [absolute path]
Standards: [skill dir]/references/developer-guide-standard.md
           [skill dir]/references/user-guide-standard.md
           [skill dir]/references/mermaid-rules.md
Settled findings (do not raise again): [list, or "none"]
```

### New developer: `repo-documenter:goldfish-new-developer`

```text
Review this developer guide as an engineer who is new to the project.
Developer guide: [absolute path]/DEVELOPER_GUIDE.md
Repository root: [absolute path]
Standard: [skill dir]/references/developer-guide-standard.md
Settled findings (do not raise again): [list, or "none"]
```

### App user: `repo-documenter:goldfish-app-user`

```text
Review this user guide as a person who uses the product.
User guide: [absolute path]/USER_GUIDE.md
Standard: [skill dir]/references/user-guide-standard.md
Settled findings (do not raise again): [list, or "none"]
```

The app-user reviewer gets no repository path on purpose. A real user cannot look at the code to work out what a sentence meant.

## Findings

Each reviewer returns findings in this form and ends with a status line:

```markdown
### F1 · Blocker · <short title>
- Guide: DEVELOPER_GUIDE.md
- Where: <section heading> (line N)
- Problem: <what is wrong or missing>
- Evidence: <file:line and what it shows, or the quoted sentence from the guide>
- Suggested fix: <the corrected statement, or what to add>

REVIEW STATUS: complete
```

Give each finding a stable id when you collect it: `<reviewer>-<round>-<n>`, for example `accuracy-1-3`. Keep the list in `review-log.md` in the work directory, with the decision you take for each.

## Triage: verify before you fix

A Goldfish can be wrong: it may miss a file, or misread a guide sentence. For each finding:

1. **Check it** against the code or the guide text.
2. **Confirmed** → fix the guide. If the same mistake could occur elsewhere (a renamed folder, a wrong command), search both guides and fix every place.
3. **Not confirmed** → contest it. Record the evidence that the guide is right. If the reviewer misunderstood because the sentence was unclear, that is still a finding: rewrite the sentence.
4. **Needs a human** → the code cannot settle it (intended behavior, business rules, who the audience is). Add it to the open items for the final message and to "Known gaps" in the guide. Do not guess.

A finding from the app-user reviewer about confusion is confirmed by definition: the reader was confused. Fix the wording. Check any factual change you make in response against the code, because that reviewer could not.

Fix findings yourself. You hold the context needed to judge them, and a subagent that edits the guide would do so without it.

## Rounds and when to stop

- **Settled**: a finding you contested with evidence, or passed to the user as an open item. Send the settled list to later reviewers so they do not raise the same point again.
- **Fixed is not settled.** If a later reviewer raises the same issue in the same place, the fix did not work. Open it again.
- **Clean round**: no reviewer raised a Blocker or Major finding that is not settled. Nits do not count.
- **Next round**: after fixing the findings of a round that was not clean, run `check_guides.py` again, then spawn three new reviewers. New reviewers, not the earlier ones resumed: an earlier reviewer remembers the old text.
- **Stop** at the first clean round, or after 3 rounds. Fresh reviewers read differently each time, so a round with zero findings is rare; do not chase one.
- **At the cap** with Blockers or Majors still open: list them by severity in the final message and let the user choose whether to accept, continue, or redirect.
- **Churn**: if a new finding exists only because of a fix from the round before, and undoing that fix would resolve it, stop and put both versions to the user.

## Reviewers that did not run

A reviewer that fails, times out, returns nothing, or ends with `REVIEW STATUS: incomplete` did not review. Retry it once with a new subagent. If it fails again, record it as **not run**. A reviewer that did not run is never counted as a reviewer with no findings, and a round with a reviewer not run is not clean.

## Review status in the guides

Set the "Review" field of each guide's status block from what happened:

| What happened | Status text |
|---------------|-------------|
| Ended on a clean round | `Reviewed by fresh-context reviewers, N rounds` |
| Stopped at the cap with open findings | `Reviewed, N rounds, open findings listed in Known gaps` |
| A reviewer could not run | `Partly reviewed (<reviewer> did not run)` |
| No subagents available | `Not reviewed` |

Report the truth here. A reader decides how far to trust the guide from this line.
