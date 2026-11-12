# Operator guides

Two documents for the people who run the system: operations staff, support,
shift operators. They know the business and the surrounding systems well. They
do not read code and should not need to. Each document must let them answer
"what is the app doing, and why?" on their own.

## Rules for both documents

**No code references.** No file paths, no function, class or method names, no
line numbers, no code snippets, no package or module names. The reader cannot
open the code, so a reference to it is noise at best and a dead end at worst.

**Keep everything an operator can see or type, exactly as it appears.** These
are not code references; they are the operator's evidence:

- Log messages, quoted literally, with their level
- Status values a transaction or job can have
- Response, result or error codes
- Names of running services, processes, containers, queues and topics
- Health check addresses and ports
- Settings an operator can change, by their real name
- The identifier that follows a transaction (reference number, trace ID)

**Name parts by what they do.** Use the human name from the canonical names
table ("the order checker"), never the code name. Where a running service has a
real name the operator sees on a server or dashboard, give both once: "the
payment gateway (runs as `pay-gw`)".

**Describe behaviour, with numbers.** "If the bank does not answer within 30
seconds, the app cancels the request and sends a reversal. It tries the reversal
up to 3 times, 10 seconds apart." Not "the request times out".

**Every step says what can be observed.** If a step leaves no trace an operator
can see, say "nothing visible at this step". An empty cell hides the fact that
there is nothing to look for.

**Say what the system does by itself, then what is left for a person.** An
operator's first question in an incident is whether to wait or to act.

**Do not invent.** Anything not established by the source material goes in the
last section as a question for the development team. A confident guess in an
operator guide becomes a wrong action at 3 a.m.

**Diagrams** follow the Mermaid rules in the brief, with these differences:

- Participants and boxes are people and systems ("Customer", "Our app", "Bank",
  "Core banking"), never classes or functions. Show this app as one participant,
  or as its separately running parts if an operator can tell them apart.
- At most 6 participants in a sequence diagram; split a longer story in two.
- Labels are plain sentences. Put the code or message type an operator would
  recognise in brackets: "Sends payment request (0200)".
- Put one sentence above each diagram saying what it shows, and after the first
  diagram of each kind a short "How to read this diagram" note.

## Template: application flow

````markdown
# <App name> - How the application works

> **For:** operations staff · **Generated:** <date> · **Version described:** <commit or release>
> **Related:** [Transaction flows](TRANSACTION_FLOW.md)

## 1. What this application does
*Three to six sentences: its job, who depends on it, what stops working for the
business if it stops.*

## 2. The parts that run
*Flowchart: the running parts of this app and the outside systems around them.*

| Part | What it does | Runs as | If it stops |
|---|---|---|---|

## 3. What it connects to
| System | Why we talk to it | Who starts the conversation | What you will see if it is unavailable |
|---|---|---|---|

## 4. Starting and stopping
*Flowchart or sequence of the startup order. Then: how long it normally takes,
the sign that it is ready, what it does if something it needs is missing at
start. The same for a normal stop: what it finishes first, what is safe to
interrupt.*

## 5. A normal day
*Flowchart of the operating cycle: what the app does continuously, what it does
only when something arrives, what it does on a schedule.*

| Scheduled job | When | What it does | If it fails or is missed |
|---|---|---|---|

## 6. How to tell it is healthy
*Signs of normal operation: health checks, the log lines that appear when all is
well, normal volumes or rhythms if the source material gives them.*

## 7. When something looks wrong
| What you see | Likely cause | What the app does on its own | What to check |
|---|---|---|---|

## 8. Settings that change behaviour
| Setting | What it controls | Effect of changing it |
|---|---|---|

*Names only. Never the value of a password, key or token.*

## 9. Glossary
| Term | Meaning |
|---|---|

## 10. Not covered here
*What this guide does not describe, and open questions for the development
team, each as a specific question.*
````

## Template: transaction flow

````markdown
# <App name> - Transaction flows

> **For:** operations staff · **Generated:** <date> · **Version described:** <commit or release>
> **Related:** [How the application works](APP_FLOW.md)

## 1. Transactions at a glance
| Transaction | What it is for | Who starts it | Normal result |
|---|---|---|---|

*One flowchart showing how the transaction types relate, if they do (for
example a payment that can later be reversed or refunded).*

## 2. Following one transaction
*The identifier that follows a transaction end to end, where it appears (logs,
database status, messages to partners), and how to use it to find out what
happened to a specific transaction.*

## 3. <Transaction name>
*Repeat this section for each transaction type.*

### In plain words
*Three to five sentences telling the whole story, including the usual way it
ends and the usual way it fails.*

### Who is involved
*Each person and system taking part, one line each.*

### Step by step
*Sequence diagram with people and systems as participants, the normal path
first and the main failure shown with alt / else.*

| Step | What happens | Who does it | What you can see |
|---|---|---|---|

### Statuses
*State diagram of the statuses this transaction moves through.*

| Status | Meaning | Normal next step | How long it can stay here |
|---|---|---|---|

### Timing
| Wait | How long | What happens when it runs out |
|---|---|---|

*Timeouts, retries with their count and spacing, cut-off times.*

### When it goes wrong
| Situation | What the system does on its own | Final result for the customer or caller | What you can check |
|---|---|---|---|

*Cover at least: bad or incomplete request, each outside system not answering,
an answer that arrives too late, the same request arriving twice, the app
stopping in the middle.*

## 4. Codes you will see
| Code | Meaning | Usual cause |
|---|---|---|

## 5. Glossary
| Term | Meaning |
|---|---|

## 6. Not covered here
*Transaction types that exist but are not described, and open questions for the
development team, each as a specific question.*
````

## Example of the right level

Written for a developer (does not belong in an operator guide):

> `PaymentHandler.Create` calls `BankClient.Transfer` with a 30 s context
> deadline from `BANK_TIMEOUT`; on `ErrTimeout` it enqueues a reversal job.

Written for an operator:

> The app sends the payment request to the bank and waits up to 30 seconds
> (setting `BANK_TIMEOUT`). If no answer arrives, it marks the transaction
> `TIMEOUT`, writes the log line `bank timeout, scheduling reversal ref=<ref>`
> at WARN level, and sends a reversal to the bank. Nothing needs to be done by
> hand unless the reversal also fails, which is covered in the next row.
