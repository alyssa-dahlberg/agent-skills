---
name: csharp-conventions
concern: Idiomatic, safe, modern C# — held to our house style first and the .NET guidelines behind it.
triggers:
  - "**/*.cs"
  - "**/*.csproj"
level: detail
model: standard   # line-by-line against a style guide — mid tier is plenty
---

> **This is an example lens.** The *Context* paragraph below is invented to show the shape of a good
> lens: it names who the team is, what they run, and what they actually value, so the reviewer reviews
> with the right frame instead of a generic checklist. Rewrite it for your own project before using
> this — the specifics are the point, and yours will differ.

**Context.** We're a small team — four engineers — on a .NET 9 backend: an ASP.NET Core web API plus a
couple of worker services, EF Core over Postgres, shipped as containers. We favour **boring, obvious
code over clever abstractions**, prefer the framework's defaults to bespoke infrastructure, and treat
"a new hire can follow this in six months" as the bar. We're strict about **null-safety and async
correctness** specifically, because that's where our production incidents have actually come from — a
finding there lands harder than a style nit. We're relaxed about the cosmetic style the analyzer already
enforces: don't spend review budget on what `dotnet format` fixes on save. When you weigh a finding, ask
whether it points *toward* code this team can safely change a year from now.

Read the references first, then review the change against them **and** the context above. Cite the
specific guideline in each finding.

References — read every one first:
- https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/coding-conventions
- https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/

**Look for the following — but this list is a *floor, not a gate*.** It names the things that bite this
team most; it does not fence off the concern. Flag anything that works against safe, idiomatic, readable
C# even if it isn't listed here, and skip a listed item that plainly doesn't apply.

- **Nullability suppression.** `!` (null-forgiving) or `#nullable disable` used to silence the compiler
  instead of modelling the null. This is a top-of-list smell for us — flag it unless there's a
  documented, unavoidable reason, and say what the honest model would be.
- **Async correctness.** `async void` outside event handlers; sync-over-async (`.Result`, `.Wait()`,
  `GetAwaiter().GetResult()`) risking deadlock; missing `CancellationToken` on I/O; `ConfigureAwait`
  discipline for the project type. Same weight as nullability — this is where we get paged.
- **Business logic in the wrong place.** Fat controllers/handlers doing work that belongs in a service;
  EF queries scattered through the HTTP layer. Thin adapters, logic in one obvious place.
- **Disposal & lifetime.** `IDisposable`/`IAsyncDisposable` created without `using`; a field holding a
  disposable with no disposal path; disposing something owned by the DI container or the caller.
- **Exceptions.** Swallowed exceptions (empty `catch`), catching `Exception` broadly, throwing bare
  `Exception`, or exceptions used for ordinary control flow.
- **Naming & clarity.** PascalCase types/methods, camelCase locals, `I`-prefixed interfaces; names that
  say what a thing *does*. A meaningless `Async` suffix, or a name that needs a comment to decode.
- **Cleverness that costs readability.** A generic abstraction with one implementation, reflection where
  a plain call would do, an "extensible" seam nobody asked for — measured against the boring-code value
  above, not against what's theoretically elegant.
- **API surface.** Public members without XML `/// <summary>` docs; mutable public fields where a
  property belongs; internal types leaking across an assembly boundary.

Don't flag what `dotnet format` / the analyzers already handle (spacing, `var` vs. explicit, ordering) —
that's noise here, not review.
