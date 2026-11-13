# Developer guide standard

The standard that `DEVELOPER_GUIDE.md` is written to and reviewed against.

## The reader

An engineer who can read the language but has never seen this repository. After reading, they can explain the architecture, find the code behind a behavior, run the project, and make a typical change without asking the previous owner.

## Status block

Directly under the title:

```markdown
> **Source:** `<repo name>` at commit `<short sha or "no git">` · **Generated:** <YYYY-MM-DD>
> **Review:** <Reviewed by fresh-context reviewers, N rounds | Not reviewed> · **Companion:** [User guide](USER_GUIDE.md)
```

The commit tells a later reader how far the code may have moved since the guide was written.

## Required sections, in this order

Keep a section even when it is short. If one does not apply, keep the heading and say why in one line (for example "This project stores no data"), so the reader knows it was considered and not forgotten.

| # | Section | What it must contain |
|---|---------|----------------------|
| 1 | **Overview** | What the project is and who uses it, in a short paragraph. Technology stack as a table (layer, technology, version where pinned, where it is declared). |
| 2 | **High-level architecture** | The main components, the external systems, and how they talk. One architecture diagram. Then one paragraph per component. |
| 3 | **Repository map** | Table of top-level folders and important files: path, what it holds, when a developer touches it. |
| 4 | **Getting started** | Prerequisites, install, configure, run, test, build, with the exact commands from the manifests. Mark any command you did not execute. |
| 5 | **Core concepts and data model** | The domain terms and the entities, their fields and relations. A data diagram when the project stores or models data. |
| 6 | **Application lifecycle** | What happens from start-up to a handled request or a rendered page: boot order, middleware, routing, rendering. One diagram. |
| 7 | **Detailed flows** | One subsection per key flow (normally 3 to 7). See "Flow subsection" below. |
| 8 | **Modules in depth** | One subsection per module: responsibility, entry points, key files, what it depends on, what depends on it, things that surprise people. |
| 9 | **Configuration** | Table of environment variables, flags and config files: name, where it is read, default, effect. Names only, never secret values. |
| 10 | **External integrations** | Each outside service or API: what it is used for, where the call is made, what happens when it fails. |
| 11 | **Build, test and deployment** | How the project is built, tested and shipped, from CI and deployment files. A pipeline diagram when CI or deployment configuration exists. |
| 12 | **How to make common changes** | 3 to 6 short recipes for the changes this codebase invites ("add a page", "add an endpoint", "add a translation"), each listing the files to touch in order. |
| 13 | **Known gaps and risks** | What could not be verified from the code, questions for the owner, and risks you saw (missing tests, dead code, inconsistent patterns). |
| 14 | **Glossary** | Project-specific terms and abbreviations. |

Add a table of contents after the status block.

## Flow subsection

Each flow in section 7 has the same five parts, so that a reader can compare flows:

1. **Purpose**: one sentence on what the flow achieves and who starts it.
2. **Trigger**: the route, event, command or schedule, with its citation.
3. **Diagram**: a `sequenceDiagram` with the real components as participants.
4. **Step by step**: a numbered list that matches the diagram's messages one to one, each step citing the file and symbol.
5. **Failure paths**: what happens on invalid input, a failed dependency, or a missing permission.

## Diagrams

Minimum set. Draw more wherever a picture answers a question faster than a paragraph.

| Diagram | Type | Required |
|---------|------|----------|
| System architecture | `flowchart` | Always |
| Application lifecycle | `flowchart` or `sequenceDiagram` | Always |
| One per key flow | `sequenceDiagram` | Always, at least 2 |
| Data model | `erDiagram` or `classDiagram` | When data is stored or modelled |
| Entity or process states | `stateDiagram-v2` | When something has a status that changes |
| Build and deployment pipeline | `flowchart` | When CI or deployment configuration exists |

Every diagram has one sentence before it that says what it shows. Follow `mermaid-rules.md`.

## Grounding and citations

- Name code in backticks with its path from the repository root: `src/orders/service.ts`, and the symbol where useful: `createOrder()` in `src/orders/service.ts`.
- Every path written in the guide must exist in the repository.
- A node or arrow in a diagram stands for something in the code. Do not add a component "that such systems usually have".
- State versions, counts and names as the repository states them. Do not round or modernize them.
- When sources disagree (README says one thing, code another), report what the code does and note the disagreement under "Known gaps and risks".

## Depth

Detailed means specific, not long. Prefer "`POST /api/orders` validates the body with `orderSchema` and returns 422 on failure" to a paragraph about validation in general. Cut sentences that would be true of any project.

## Severity guide for reviewers

| Severity | Meaning | Examples |
|----------|---------|----------|
| **Blocker** | A reader who acts on it is wrong or stuck | A path, command, route or component that does not exist; a flow step that contradicts the code; a required section or required diagram missing; a diagram that will not render |
| **Major** | A real gap or likely misunderstanding | An important module or flow not covered; a failure path omitted; a diagram that disagrees with its step list; a term used before it is explained |
| **Nit** | Polish | Wording, ordering, a minor inconsistency in naming |
