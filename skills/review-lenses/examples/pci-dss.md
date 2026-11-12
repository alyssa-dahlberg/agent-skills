---
name: pci-dss
concern: Handling of payment card data against PCI DSS expectations — no storage of sensitive auth data, PAN protected in transit and at rest, no leakage into logs.
triggers:
  - "**/*payment*/**"
  - "**/*checkout*/**"
  - "**/*card*/**"
  - "**/*billing*/**"
level: broad
model: deep   # reads an external standard and judges a whole surface — needs real understanding
---

> **This is an example lens** showing a **compliance** concern reviewed against an *external standard*:
> it points at the standard by URL and the reviewer fetches the authoritative text at review time,
> rather than trusting a paraphrase that drifts as the standard is revised. The *Context* is invented —
> replace it, and pin the specific standard version and your own scoping doc, before using this.
>
> It is an illustrative starting point, **not compliance advice or a certification.** A real PCI DSS
> assessment is done by a QSA against your entire cardholder-data environment; this lens catches the
> obvious, expensive mistakes early in review — it does not make a change "PCI compliant."

**Context.** We deliberately keep our PCI scope as small as we can: card entry goes through our
provider's **hosted fields / tokenization**, so a raw PAN should **never** touch our servers, logs, or
database — we work with tokens. That makes the highest-value thing this lens can do **catch anything
that pulls raw card data back into scope**: a new endpoint that accepts a PAN, a log line that could
capture one, a "temporary" store of card details. When you see cardholder data somewhere it shouldn't
be, that's not a nit — it's the finding. We would rather redesign a feature than widen scope.

Read the references first, then review the change against them and the scope-minimising stance above.
Flag as **BLOCKING** anything that stores prohibited data or exposes a PAN.

References — read every one first (the full PCI DSS standard sits behind acceptance/registration at the
PCI SSC library, so if the exact document won't fetch, search for the current "PCI DSS Quick Reference
Guide" and cite that instead — and pin the specific standard + version for real use):
- https://www.pcisecuritystandards.org/document_library/
- https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html

**Look for the following — a *floor, not a gate*.** These are the mistakes that hurt most; also flag
anything else that risks cardholder data or widens PCI scope, even if it isn't listed.

- **Sensitive authentication data stored — ever.** Full track data, the card verification value
  (CVV/CVC/CID), or the PIN/PIN block persisted to a database, cache, file, or queue. Prohibited
  post-authorization even encrypted. The single most important thing to catch.
- **PAN (card number) in the clear.** A full PAN written to logs, error messages, analytics, URLs, or a
  non-encrypted store. If it's displayed, is it masked (first-six/last-four at most)? Encrypted or
  tokenised at rest?
- **Scope creep — our top concern.** Does this change pull a system *into* PCI scope that was out of it
  — a new service that now touches raw PAN, a log sink that now receives it, a form that posts card
  data to our origin instead of the provider? Prefer the hosted field / tokenised path so raw card data
  never reaches us. Flag a design that needlessly widens scope, and say how to keep it narrow.
- **Card data crossing a boundary in the clear.** PAN sent over plain HTTP, to a third party without
  TLS, or into a log/trace pipeline. Verify TLS on every hop carrying cardholder data.
- **Logging leakage specifically** (OWASP reference): request/response body logging, exception dumps, or
  debug traces on a payment path that would capture PAN or auth data. Assume verbose logging is on in
  *some* environment.
- **Access & secrets.** Broad, non-least-privilege access to whatever card data does exist; payment
  processor keys or gateway credentials committed, logged, or shared across environments.
