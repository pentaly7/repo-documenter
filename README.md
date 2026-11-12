# Repo Documenter

A Claude Code plugin that documents a whole repository with Mermaid diagrams. One
run produces three Markdown files:

| File | For | Contains |
|---|---|---|
| `docs/REPOSITORY_GUIDE.md` | Developers, and anyone reading only its first sections | Big picture, architecture, every important flow traced through the code with file references, data model, configuration, run and deploy |
| `docs/operator/APP_FLOW.md` | Operations staff | The running parts, connections, startup and shutdown, the normal operating cycle, scheduled jobs, signs of health, what to check when something looks wrong |
| `docs/operator/TRANSACTION_FLOW.md` | Operations staff | Each transaction type step by step, statuses, timeouts and retries, failure situations, result codes |

The two operator guides contain no file paths, function names, line numbers or
code. They keep what an operator can actually see: log messages, statuses, codes,
service names and setting names.

To be fast on large repositories it splits the work across parallel subagents: a
lead surveys and plans, workers each read one part in depth, and two reviewers who
have seen none of the work check the result.

## Install

From a local copy of this folder:

```sh
claude plugin marketplace add pentaly7/repo-documenter
claude plugin install repo-documenter@repo-documenter
```

Or try it for one session without installing:

```sh
claude --plugin-dir ./repo-documenter
```

If you push this folder to a Git repository, teammates can add it with
`claude plugin marketplace add <owner>/<repo>`.

## Use

Open the repository you want documented and run:

```text
/repo-documenter:document
```

Or just ask, for example "document this repo" or "explain how this service works
with diagrams". Optional directions work in plain words: "focus on the payment
flow", "write it in Indonesian", "only the operator guides", "only the repository
guide", "save them under docs/handover/".

Small repositories are documented directly; larger ones use the agents below. If
a plan needs more than about 12 agents, it asks before starting.

## What is inside

| Path | What it is |
|---|---|
| `skills/document/SKILL.md` | The lead's workflow: survey, plan, dispatch, assemble, review, deliver |
| `skills/document/references/` | Repository guide template, operator guide rules and templates, Mermaid rules, rules shared by all workers |
| `agents/module-scout.md` | Reads one code area in depth |
| `agents/flow-tracer.md` | Traces one flow end to end, with a sequence diagram |
| `agents/data-scout.md` | Data model, lifecycles, data movement |
| `agents/ops-scout.md` | Configuration, run, test, build, deploy |
| `agents/accuracy-reviewer.md` | Checks the finished guide against the code |
| `agents/plain-reader.md` | Reads the non-technical sections as a non-technical person |
| `agents/operator-writer.md` | Writes one operator guide from the workers' findings, without code references |
| `agents/operator-reader.md` | Reads the operator guides as an operator on shift and reports what they could not answer |

## Notes

- Workers write only to a temporary scratch folder; the only files added to your
  repository are the three documents.
- Secret values are never copied into the documents, only setting names.
- Optional: if the Mermaid CLI (`mmdc`) is installed, diagrams are render-checked.
- The lead-and-fresh-reviewers design follows the Elephant-Goldfish Model
  (https://github.com/google/elephant-goldfish-model).

## Disclaimer
this repository build using fable 5.2 medium (https://claude.ai/share/111a0c2e-5d86-44f4-909f-84f91fe65c2c)
