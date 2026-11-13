# User guide standard

The standard that `USER_GUIDE.md` is written to and reviewed against.

## The reader

A person who uses the finished product. Assume they are capable and busy, and that they have never seen the code and do not want to. After reading, they know what the product is for, how to complete their main tasks, what each status or message means, and what to do when something goes wrong.

Who that person is depends on the product:

| Product type | The "app user" is | Their "screens" are | Their "journeys" are |
|--------------|-------------------|---------------------|----------------------|
| Web or mobile app | A person using the interface | Pages and screens | Tasks they complete in the interface |
| API service | A person or team that integrates with it | Endpoints, as named in the public documentation | Calls made to get an outcome |
| Command-line tool | A person typing commands | Commands and their options | Tasks done with one or more commands |
| Library or SDK | A developer who installs and calls it | The public functions and types | Things they build with it |
| Documentation or content site | A reader, and often a content contributor | Sections and pages of the site | Finding, reading, and contributing content |
| Data pipeline or batch job | The person who runs it or consumes its output | Inputs, schedules, outputs, reports | Running it, and using what it produces |

For a command-line tool, library or API, commands and public names are the user's interface, so they belong in this guide. Internal file names and internal functions still do not.

If a product has several kinds of user (for example a customer and an administrator), say so at the start and mark which sections serve which role.

## Status block

Directly under the title:

```markdown
> **About this guide:** describes `<product name>` as of <YYYY-MM-DD>.
> **Review:** <Reviewed by fresh-context reviewers, N rounds | Not reviewed> · **For developers:** [Developer guide](DEVELOPER_GUIDE.md)
```

## Required sections, in this order

Keep every heading. If one does not apply, say why in one line.

| # | Section | What it must contain |
|---|---------|----------------------|
| 1 | **What this is** | What the product does and who it is for, in a few sentences a newcomer understands. |
| 2 | **What you can do with it** | The main capabilities as a short list, each phrased as something the user achieves. |
| 3 | **Before you start** | What the user needs: an account, access, a device or browser, installed software, information to have at hand. |
| 4 | **The app at a glance** | The main areas of the product and how the user moves between them. One map diagram, then a short description of each area. |
| 5 | **How the app works, from start to finish** | The overall flow from arriving to getting the outcome, including the decisions along the way. One flow diagram, then a walk-through. |
| 6 | **Step-by-step guides** | One subsection per key task (normally 3 to 7). See "Task subsection" below. |
| 7 | **What happens behind the scenes** | A simple account of what the product does with the user's action or data, where it goes, and what is kept. No internal names. One diagram. |
| 8 | **Statuses and messages** | What each status, label or notification means and what happens next. A state diagram when something moves through statuses. |
| 9 | **When something goes wrong** | A table: what you see, what it means, what to do. Use the product's real messages. |
| 10 | **Roles and permissions** | Who can do what, when the product has more than one kind of user. |
| 11 | **Questions and answers** | The questions a new user would ask, answered briefly. |
| 12 | **Words used in this guide** | Each term the product uses that an outsider would not know. |

## Task subsection

Each task in section 6 has the same parts:

1. **Goal**: what the user will have achieved at the end.
2. **You need**: anything required first.
3. **Steps**: numbered, one action per step, saying what the user does and what they then see.
4. **Diagram**: a `flowchart` of the task with its decisions (for example "Is the form valid?").
5. **Result**: how the user knows it worked, and what they can do next.

## Language rules

- Write to the reader as "you". Use the present tense and short sentences.
- Use the product's own words. Write labels, button names, menu items and messages exactly as the product shows them, in bold: select **Save changes**. These come from the text in the source, so they can be checked.
- No file paths, function names, class names, database table names or framework names. If the user never sees it, it does not belong here. Exception: for a command-line tool, library or API, the public commands and names are what the user sees.
- Explain a term the first time it appears, and add it to section 12.
- Describe behavior the code confirms. If you do not know how long something takes or who can see it, do not invent a number or a rule; leave it out or say that it depends on how the product is set up.
- Do not promise what the product does not do. A guide that describes a missing feature sends the user looking for it.

## Diagrams

Minimum set. Add more where a picture is clearer than a paragraph.

| Diagram | Type | Required |
|---------|------|----------|
| The app at a glance | `flowchart` | Always |
| Overall flow from start to finish | `flowchart` | Always |
| One per key task | `flowchart` | Always, at least 1 |
| Behind the scenes | `sequenceDiagram` or `flowchart` | Always |
| Statuses | `stateDiagram-v2` | When something has a status that changes |

Rules for these diagrams:

- Name every box and participant in the user's words: "You", "The app", "Payment provider", "Your email". Not "AuthController" or "Redis".
- Keep each diagram small enough to take in at a glance: about 12 boxes at most. Split a larger one.
- After every diagram, give the same information in words: a numbered walk-through or a short paragraph. Some readers cannot see or render the diagram, and the text must stand on its own.

Follow `mermaid-rules.md` for syntax.

## Severity guide for reviewers

| Severity | Meaning | Examples |
|----------|---------|----------|
| **Blocker** | The user would be misled or stuck | A step that does not match what the product does; a button or message that does not exist; a described feature the product lacks; a required section or diagram missing; a diagram that will not render |
| **Major** | The user would be confused or left without an answer | Unexplained jargon or internal names; a main task with no guide; a status or common error not explained; a diagram with no text walk-through |
| **Nit** | Polish | Wording, order, tone |
