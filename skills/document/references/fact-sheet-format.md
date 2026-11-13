# Fact sheets and scout tasks

A fact sheet is the evidence a guide is written from. Every entry carries a citation, so that a sentence in a guide can always be traced back to a line of code.

## Citation style

`path/from/repo/root.ext:LINE` and, where it helps, the symbol: `src/orders/service.ts:42 (createOrder)`. Quote user-visible text exactly, in double quotes, with its citation.

## Scout task: module mode

Spawn `repo-documenter:scout` with this task. Fill the brackets and send nothing else: no conversation history and no guesses about what the module does, because a guess in the task comes back as a "fact" in the sheet.

```text
Mode: MODULE
Repository root: [absolute path]
Your part: [folder or list of folders/files]
Product context: [one sentence: product type and what it is for, from the README]
Neighbouring parts (other scouts cover these; name them when your part calls them, do not explore them): [list]

Read your part and return a module fact sheet in the format defined in
[absolute path]/references/fact-sheet-format.md, section "Module fact sheet".
Read that file first.
```

## Scout task: flow mode

```text
Mode: FLOW
Repository root: [absolute path]
Flow to trace: [name, e.g. "A visitor signs up"]
Starting point: [file:line of the trigger: route, button handler, command, job]
Known waypoints: [citations from module fact sheets, or "none"]

Follow the real call path from the starting point to the final outcome and return a
flow trace in the format defined in
[absolute path]/references/fact-sheet-format.md, section "Flow trace".
Read that file first.
```

## Module fact sheet

Return exactly these headings. Under a heading with nothing to report, write `None found`. Keep the sheet under about 150 lines: list what matters to someone who must understand or change this part, not every helper.

```markdown
# Fact sheet: <part>

## Purpose
One to three sentences on what this part is responsible for. Cite the file that shows it.

## Entry points
| What starts it | Symbol | Citation |
|----------------|--------|----------|
(routes, pages, commands, event handlers, scheduled jobs, exported functions)

## Interface to other parts
What other parts call or import from here, and what this part exposes outward
(HTTP routes with method and path, CLI commands with flags, exported components, events). Cited.

## Data
Entities, tables, collections, files or stores this part defines or owns, with their main fields. Cited.

## Depends on
Internal parts it calls, external services, and notable packages. Cite the import or call.

## Side effects
Network calls, database writes, files written, messages sent, emails, caches. Cited.

## Configuration
| Name | Read at | Default | Effect |
|------|---------|---------|--------|
(environment variables, flags, config keys)

## User-visible behavior
What a person using the product sees or does because of this part: screens, pages, commands,
labels, messages, error texts, statuses. Quote the exact strings. Cited.
This section feeds the user guide, so describe it the way a user would experience it.

## Call chains seen
Ordered chains you actually followed, one per line: `a.ts:10 (handle) -> b.ts:33 (save) -> db`.

## Not verified
What you could not confirm, and questions the code does not answer.
```

## Flow trace

```markdown
# Flow: <name>

## Trigger
Who or what starts it, and where the code receives it. Cited.

## Participants
The actors and components involved, in order of first appearance, each with a plain-language
name a user would understand and its technical name:
| Plain name | Technical name | Citation |

## Steps
Numbered. One action per step, each cited. Say what data moves.
1. ...

## Branches and failures
Conditions that change the path, validation failures, error handling, retries. Cited.
Include what the user sees in each case, quoted exactly.

## Data read and written
Stores, entities and fields touched, and when.

## Outcome
The final state of the system and what the user sees.

## Not verified
Steps you could not follow to the end, and why.
```

## Rules for whoever fills a sheet

- Cite or leave out. A file or folder name tells you where to look; it is not proof of what the code does. If you inferred something without reading it, put it under "Not verified".
- Check imports before you attribute behavior to a local file: the code may live in a package or another part.
- Read contracts first (schemas, route tables, type definitions, exported interfaces), then entry points, then the rest.
- Ignore test files as a source of behavior, but note the test command and where tests live.
- Report configuration by name only. Never copy the value of a secret, token or password into a sheet.
