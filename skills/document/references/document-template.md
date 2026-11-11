# Document template

Use this structure. Keep the section order, since the document deliberately runs
from least to most technical. Drop a section only when it truly does not apply
(no database means no data model section), and say so in one line instead of
leaving a silent gap. Text in *italics* is guidance to replace.

````markdown
# <Project name> - Repository Guide

> **Generated:** <date> · **Commit:** <short hash or "not a git repo"> ·
> **Coverage:** <what was read in depth / skimmed / skipped>

**How to read this:** Sections 1-3 are for everyone. Sections 4 onward are for
people who will work on the code.

## Table of contents

## 1. At a glance
*Five to eight bullets in plain language: what it is, who uses it, the main things
it does, what it depends on, what it is built with (one line), current state.*

## 2. The big picture
### 2.1 What this is and why it exists
*Two or three short paragraphs, no jargon. One everyday analogy if it clarifies.*

### 2.2 Who and what is involved
*System context diagram: people and outside systems around this app as one box.*

### 2.3 How it works, in one picture
*High-level flowchart of the main journey in plain-language labels, 5-9 boxes,
followed by a numbered walk-through in sentences.*

### 2.4 What it can do
*Table: Capability | What it means for the user | Detailed in section.*

## 3. Glossary
*Table: Term | Plain meaning | Where it shows up. Business terms and technical
terms both.*

## 4. Architecture
### 4.1 Technology stack
*Table: Layer | Technology | Version | Why it is here / what it does.*

### 4.2 Components
*Component diagram of the real modules and how they talk, then a table:
Component | Responsibility | Location | Depends on.*

### 4.3 Directory map
*Tree of the meaningful folders, one line each on what lives there.*

### 4.4 Entry points
*Table: Entry point | Type (HTTP, CLI, job, consumer...) | File | What it starts.*

## 5. Flows in detail
*One subsection per flow, each in this shape:*

### 5.x <Flow name>
**In plain words:** *two or three sentences anyone can follow.*

**Trigger:** *what starts it* · **Outcome:** *what is true when it ends*

*Sequence diagram with real component names.*

| Step | What happens | Where in the code | Data in → out |
|---|---|---|---|
| 1 | | `path/file.ext` · `functionName` | |

**When things go wrong:** *table: failure → what the code does → what the user or
caller sees.*

**Worth knowing:** *non-obvious rules, ordering constraints, timeouts, retries.*

## 6. Data
### 6.1 Data model
*ER diagram of the main entities, then a table: Entity | Meaning in plain words |
Stored in | Key fields.*

### 6.2 Lifecycle of the main entity
*State diagram when something moves through statuses (order, transaction, job).*

### 6.3 How data moves
*Where data enters, where it is transformed, where it rests, what leaves.*

## 7. Interfaces and integrations
*Exposed API: Method/command | Path/name | Purpose | Handler file.
Outside systems: System | Why we call it | How (protocol) | Where in code | What
happens if it is down.*

## 8. Configuration
*Table: Setting | Purpose | Default | Required? | Read in. Names only for secrets.*

## 9. Running it
*Prerequisites, install, run locally, run tests, build - the exact commands from
the repo's own scripts, each with one line on what it does.*

## 10. Build and deployment
*Flowchart from commit to running system, environments, how releases happen.*

## 11. Cross-cutting concerns
*Short subsections as they apply: authentication and authorisation, error
handling strategy, logging and monitoring, performance and scaling, security.*

## 12. Changing the code
*"If you want to do X, start in Y" table for the most likely changes, plus the
conventions the code follows and the traps to avoid.*

## 13. Risks, unknowns and open questions
*Things that look fragile or surprising, with evidence. Then everything that could
not be determined from the repo and where it was looked for.*

## Appendix A. File reference
*Table of the important files: File | Role | Mentioned in section.*
````
