---
name: engineering-standards
description: Engineering standard for substantial code work in any language, covering clear structure and responsibilities, explicit types wherever the language allows, readable maintainable code, and consistency with the existing codebase. Use this for new features, multi-file changes, refactors, and plan-driven builds, even if the user does not mention quality or standards. Skip it for small one-off edits and quick fixes.
---

# Engineering Standards

Guidelines for code that stays readable and easy to change. They apply in any language; where a rule names a mechanism (a type annotation, an interface), use the nearest equivalent in the language at hand.

These are defaults for judgment, not quotas. Scale them to the task, and never add structure, types, or abstraction the code does not need.

## Stay consistent with the codebase

Follow the conventions already in the project: naming, layout, error handling, tooling, how types are declared. A consistent codebase is easier to navigate than one where each file follows a different "better" style. Depart from an existing pattern only when it cannot do the job, and say so when you do. The one standing exception is typing, which takes priority (see Types).

If you notice an existing pattern that is poor (error-prone, hard to maintain, or at odds with the standards below), still stay consistent in your own changes, but flag it to the user in your final message: what the pattern is, where it appears, and why it is a problem. Do not silently copy it without comment, and do not silently refactor it away outside the scope of the task.

## Structure and responsibilities

- Give each file, module, and class a clear, cohesive purpose, and keep code that changes together close together. Split a unit when it mixes unrelated concerns or becomes hard to follow. Do not split just to make pieces smaller: scattering tightly related logic across many tiny units hurts readability as much as one oversized file.
- Group code by what it is for (a feature or domain concept) rather than by technical type. Names like `utils`, `helpers`, and `common` often mean a home has not been decided yet.
- Keep dependencies pointing one way: core logic should not depend on I/O, UI, or framework layers. Put boundaries (network, disk, database, CLI) at the edges.
- Make the layout predictable, so someone new to the project can guess where a piece of behavior lives.

## Types

Use explicit types wherever the language supports them, because a type is documentation that the compiler or checker keeps honest.

- Declare types on function signatures, public interfaces, data structures, and module boundaries. Let inference handle obvious local variables.
- Model the domain with named types instead of loose primitives or untyped maps and dictionaries. A `UserId` and an `OrderId` are not interchangeable even if both are strings.
- Make invalid states unrepresentable where you can: use enums or unions for a closed set of options, and optional or nullable types only when absence is genuinely meaningful.
- Avoid escape hatches (`any`, untyped `object`, unchecked casts, blanket suppression comments). If one is unavoidable, keep it at the smallest possible scope and comment why.
- In languages with optional or gradual typing, turn on the strictest checking the project tolerates and annotate new code fully. In languages without a static type system, get the same benefit with validated data shapes at boundaries and clear documented contracts.
- Validate data where it enters the system (user input, network, files), then trust the types inside.
- Types win over consistency. If the surrounding code is untyped or loosely typed, still fully type what you write or change, following the project's existing type conventions where there are any. Flag the untyped areas to the user, as described under consistency, instead of silently matching them.

## Readability

- Name things for what they mean, not how they are implemented. A longer clear name beats a short cryptic one.
- Prefer clarity. Sophisticated or compact solutions are welcome when they earn their place and a reader can follow them; where the reason is not obvious, add a short comment.
- Prefer early returns over deep nesting, and a well-named helper over an explanatory comment.
- Use blank lines to separate the logical steps inside a function (setup, validation, the main work, the result) and between declarations, so the code reads in paragraphs. Do not pack a whole function into one unbroken block, and do not put a blank line after every statement either.
- Comment the why: a constraint, a trade-off, a non-obvious decision. Do not narrate what the code plainly says.
- Do not leave dead code, commented-out blocks, unused imports, or stray debug output.
- Replace magic numbers and repeated string literals with named constants.

## Abstraction and duplication

Use judgment in both directions. When duplicated code expresses the same concept and has to change together, combine it into a shared abstraction instead of leaving copies to drift apart. When code only looks similar but represents different things, leave it separate, because forcing it together creates coupling and awkward parameters. Not every repetition is a problem, and not everything should be abstracted.

## Errors and edge cases

- Fail loudly and early with specific, actionable messages. Do not swallow errors or return silent defaults that hide a problem.
- Handle errors at the layer that can do something about them, and let them propagate otherwise.
- Keep configuration and secrets out of scattered code; centralize configuration and read it in one place.

## Git history

Keep the main branch's history clean. Squash-merge a PR that has one commit, or whose commits have no value on their own. Use a merge commit only when the PR has several commits that each stand alone and make sense to keep seperate. Never add a merge commit that just wraps a single commit.
