---
name: strong-types
concern: Code in any language. Focuses on how data is typed as it moves through the system. Parsing
 at the edges, strong types inside, and data models that cannot represent invalid states.
triggers:
  - "**/*"
level: broad
model: deep
---

# Context

A type system is a design tool. Strong types let the compiler or type checker enforce rules that
would otherwise need validation code, comments and tests. Code that receives a value of a strong
type has nothing left to check.

Default to this shape:

- Parse untrusted data into strong types at the edges of the system.
- Pass those types inward. The inner code works only with them.
- Keep side effects at the edges too, around a core of pure functions.

Bad data causes much of a system's accidental complexity. A model that allows invalid states forces
all code that uses it to defend against them. Fix the model and that defensive code goes away.

The ideas apply in any language with types or type hints: C#, TypeScript, Python, Haskell, Rust and
others. The examples use C#. Translate them to the language under review and use its own idioms.

This lens relies on judgement. The sections below are a starting point.


# Scope

Start from what the caller asked you to review. Then follow the data:

- Where it enters. HTTP handlers, deserializers, config binding, command-line arguments, database
  reads, message consumers and files are all edges.
- Where it is converted or checked.
- Where it is used.

Look at the types defined in the target. Also look at the types its code accepts and returns. Read enough of the
project to know its type tools and conventions. Focus on code.


# Look for

## Parse, don't validate

A validator checks a value and returns it unchanged. Every later reader has to trust that the check
happened. A parser turns the raw value into a new type, or returns an error. The type is the proof.

- Inner code that takes a raw primitive and checks it. Example: a domain service that calls
  `int.TryParse`, checks an email format or checks that a string is a valid enum value. That work
  belongs at the edge.
- A check that returns `bool` and leaves the value as it was.
- The same check repeated in several places. One parse at the edge makes the others redundant.
- An edge parser that fails silently, or returns an unclear error to the caller.


## Strong types inside

- Primitive obsession. An email address, user ID, money amount or file path passed as a bare string
  or number. A dedicated type stops values being mixed up, and holds its own rules. Tools for this
  include C# records or Vogen value objects, TypeScript branded types, Python `NewType` and Haskell or
  Rust newtypes.
- Two values with the same representation and different meanings. They get different types.
- Weak types leaking inward, such as `object`, `dynamic`, `any`, `dict[str, Any]` or untyped JSON.
- A hand-rolled type where a library models the domain well. Example: NodaTime gives `Instant`,
  `LocalDate` and `Duration` in place of `DateTime`. Each type states what the value means.


## Invalid states unrepresentable

- Several booleans or nullable fields that only make sense in some combinations. Model the states
  directly with a sum type. Examples are TypeScript discriminated unions, Haskell and Rust algebraic
  data types, and a sealed record hierarchy or OneOf in C#.
- A lifecycle inferred from scattered flags. Model the lifecycle as states on the owning type.
- A constructor or factory that can build an invalid object. Make it enforce the rules.
- A `null` that can mean several things. Give each meaning its own state.
- A persisted model that allows contradictions. A database constraint could prevent them.


## Conversion at the edges

- Conversion code belongs at the edges. ORM mappings, model binders, JSON converters and config
  binding are the expected places.
- Inner code that converts between representations. For example, store each moment as an
  `Instant`. Convert to the user's time zone only for display. Convert from the user's time zone
  only when reading user input. The inner code never handles a zoned value.
- I/O mixed into business rules. Pull the rule out as a pure function. The service at the edge does
  the I/O and calls the rule. Pure rules are easier to test.


## Pit of success

The easy way to use a type or API should be the correct way. Misuse should take effort.

- Several parameters of the same type in a row, which callers can swap by mistake.
- An API that needs its callers to remember a step, such as calling `Validate()` or `Init()` first.
- A type whose invalid use compiles. Ask whether the type system could reject it.


## Proportion

- A type for every string is too much. Add one where a mixed-up or invalid value would cause a real
  bug, or where the same rule is checked in many places.
- Leave framework-owned types alone.
- Work with the language's strength. In a dynamic language, parse at the edges with a schema
  library. Fully typing the inner code may not be worth the cost.
- Respect the project's established conventions. If the whole project leans on primitives, raise one
  broad finding. Do not flag every file.


# Findings

- `what` names the value or type, where it enters, and where it is checked or used.
- `fix` names the type to introduce or change, where the parse happens, and the checks it removes.
- Use `BLOCKING` when unparsed untrusted input reaches security-sensitive code, such as auth,
  queries or file paths.
- Use `ATTENTION` when other unparsed untrusted input reaches inner code, or when a persisted model
  allows invalid states.
- Use `SUGGESTION` for smaller type improvements.
- If you cannot tell where the edge of the system is, report `UNRESOLVED` and say what you would need
  to know.
