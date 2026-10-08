<!--
Sync Impact Report
Version change: unratified template → 1.0.0 (initial establishment)
Modified principles: none; five principles established from the template slots
Added sections: Engineering Quality Standards; Development and Review Workflow
Removed sections: none
Follow-up TODOs: Confirm the original ratification date and replace its TODO.
-->
# spec-kit-week2 Constitution

## Core Principles

### I. Readable, Focused Code
Code MUST follow the repository's established conventions and use clear names,
small cohesive units, and explicit interfaces. Comments MUST explain intent or
non-obvious constraints rather than restate code. Reviewers MUST be able to
understand a change without relying on undocumented assumptions.

### II. Tests Protect Behavior
Every behavior change MUST include automated tests appropriate to its scope.
Tests MUST cover expected behavior and relevant failure or boundary cases;
changes to integrations or contracts MUST include tests at those boundaries.
The applicable test suite MUST pass before a change is accepted. Defects MUST
include a regression test when practical.

### III. Design for Maintainability
Changes MUST preserve clear module responsibilities and avoid unnecessary
coupling, duplication, and speculative abstractions. Contributors MUST update
or remove obsolete code when changing behavior and MUST keep changes limited to
the requested scope. Any added complexity MUST have a documented, reviewable
rationale.

### IV. Make Contracts and Compatibility Explicit
Public interfaces, persisted data, and cross-component contracts MUST have
their behavior and compatibility impact documented in code, tests, or user
documentation. Breaking changes MUST be explicitly identified, justified, and
accompanied by migration guidance before acceptance.

### V. Deliver Reviewable Changes
Each change MUST be understandable and verifiable in review. Relevant setup,
usage, and behavior documentation MUST be updated with the change. Automated
quality checks and tests MUST pass before acceptance; exceptions MUST be
recorded with an owner and a plan to resolve them.

## Engineering Quality Standards

The implementation MUST use the project's existing toolchain and conventions
unless a reviewed change establishes a replacement. Static analysis, formatting,
and other configured quality checks MUST pass for changed code. Dependencies
MUST be necessary for the change and compatible with the project's supported
environment. Quality exceptions MUST state their scope, rationale, owner, and
resolution plan.

## Development and Review Workflow

Every change MUST receive peer review before integration. Review MUST consider
correctness, test coverage, maintainability, compatibility, and documentation.
The author MUST provide enough context to explain the change and how it was
verified. Required checks MUST pass before merge; any approved exception MUST
be documented and tracked to resolution.

## Governance

This constitution governs engineering work in the project. Amendments MUST be
proposed in writing, reviewed by project maintainers, and approved before they
take effect. Every amendment MUST update the version and last-amended date and
include a migration plan when it changes existing obligations or compatibility
expectations.

Versioning follows semantic versioning: MAJOR for incompatible governance
changes or principle removals/redefinitions, MINOR for new principles, sections,
or materially expanded obligations, and PATCH for clarifications and non-semantic
edits. Maintainers MUST review changes for compliance with this constitution
during proposal review and before merge; non-compliance MUST be corrected or
approved as a documented exception under the quality standards above.

**Version**: 1.0.0 | **Ratified**: TODO(RATIFICATION_DATE): original adoption date unknown | **Last Amended**: 2026-10-05
